import redis
from flask import render_template, Blueprint, jsonify, request, current_app
from rq import Queue, Connection, Retry

from project.server.main.utils.db import db_fetch, db_insert, job_success, job_failure
from project.server.main.tasks.daily import daily
from project.server.main.tasks.db import trigger_error_queue
from project.server.main.tasks.marketcap import marketcap
from project.server.main.tasks.portfolio import portfolio
from project.server.main.utils.utils import get_worker_stats

main_blueprint = Blueprint("main", __name__, )


@main_blueprint.route("/", methods=["GET"])
def home():
    return render_template("main/home.html")


@main_blueprint.route("/worker", methods=["GET"])
def worker():
    return jsonify(get_worker_stats(), 200)


@main_blueprint.route("/up", methods=["GET"])
def up():
    redis.from_url(current_app.config["REDIS_URL"]).ping()
    db_fetch("SELECT 1")
    return ""


@main_blueprint.route("/tasks", methods=["POST"])
def run_task():
    task_type = request.form["type"]
    with Connection(redis.from_url(current_app.config["REDIS_URL"])):
        q = Queue()
        if task_type == "portfolio":
            task = q.enqueue(portfolio, job_id="portfolio",
                             retry=Retry(max=2, interval=[30, 60]),
                             on_success=job_success,
                             on_failure=job_failure)
        elif task_type == "marketcap":
            task = q.enqueue(marketcap, job_id="marketcap",
                             on_success=job_success,
                             on_failure=job_failure)
        elif task_type == "daily":
            task = q.enqueue(daily, job_id="daily",
                             retry=Retry(max=2, interval=[30, 60]),
                             on_success=job_success,
                             on_failure=job_failure)
        else:
            response_object = {"status": "error", "error": "wrong task_type"}
            return jsonify(response_object), 400

    response_object = {
        "status": "success",
        "data": {
            "task_id": task.get_id()
        }
    }
    return jsonify(response_object), 202


@main_blueprint.route("/tasks/<task_id>", methods=["GET"])
def get_status(task_id):
    with Connection(redis.from_url(current_app.config["REDIS_URL"])):
        q = Queue()
        task = q.fetch_job(task_id)
    if task:
        response_object = {
            "status": "success",
            "data": {
                "task_id": task.get_id(),
                "task_status": task.get_status(),
                "task_result": task.result,
            },
        }
    else:
        response_object = {"status": "error"}
    return jsonify(response_object)


@main_blueprint.route("/debug-sentry", methods=["GET"])
def trigger_error():
    division_by_zero = 1 / 0


# @main_blueprint.route("/portfolio.json-logging", methods=["GET"])
# def test_logging():
#     logging.debug("I am ignored")
#     logging.info("I am a breadcrumb")
#     logging.error("I am an event", extra=dict(bar=43))
#     logging.exception("An exception happened")


@main_blueprint.route("/debug-sentry-rq", methods=["GET"])
def trigger_error_rq():
    with Connection(redis.from_url(current_app.config["REDIS_URL"])):
        q = Queue()
        task = q.enqueue(trigger_error_queue)
    response_object = {
        "status": "success",
        "data": {
            "task_id": task.get_id()
        }
    }
    return jsonify(response_object), 202


@main_blueprint.route("/test_db", methods=["GET"])
def test_records():
    test_db = db_fetch("SELECT * FROM db.test")
    return jsonify(test_db), 200


@main_blueprint.route("/test_db_insert", methods=["GET"])
def test_db_insert():
    test_db = db_insert("test", {"val": "99"})
    return jsonify(test_db), 200

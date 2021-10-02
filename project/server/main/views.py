# project/server/main/views.py
import logging

import redis
from flask import render_template, Blueprint, jsonify, request, current_app
from prometheus_client import Counter
from rq import Queue, Connection

from project.server.main.tasks.daily import daily
from project.server.main.tasks.db import trigger_error_queue
from project.server.main.tasks.marketcap import marketcap
from project.server.main.tasks.portfolio import portfolio

main_blueprint = Blueprint("main", __name__, )


@main_blueprint.route("/", methods=["GET"])
def home():
    return render_template("main/home.html")


c = Counter('my_failures', 'Description of counter')


@main_blueprint.route("/tasks", methods=["POST"])
def run_task():
    task_type = request.form["type"]
    c.inc()  # Increment by 1
    with Connection(redis.from_url(current_app.config["REDIS_URL"])):
        q = Queue()

        if task_type == "portfolio":
            task = q.enqueue(portfolio)
        elif task_type == "marketcap":
            task = q.enqueue(marketcap)
        elif task_type == "daily":
            task = q.enqueue(daily)
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


# Decorate function with metric.


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


@main_blueprint.route("/test-logging", methods=["GET"])
def test_logging():
    logging.debug("I am ignored")
    logging.info("I am a breadcrumb")
    logging.error("I am an event", extra=dict(bar=43))
    logging.exception("An exception happened")


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

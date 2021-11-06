import logging
from datetime import datetime

import mysql.connector as mysql
# import the new JSON method from psycopg2
from psycopg2.extras import Json

from project.server.main.utils.utils import os_get


def db_connect():
    try:
        db = mysql.connect(**{
            'host': 'db',
            'port': 3306,
            'user': os_get("DB_USER"),
            'password': os_get("DB_PASSWORD"),
            'database': os_get("DB_DATABASE"),
        })
        return db
    except Exception as e:
        logging.exception("Can't connect to database")
        print("Can't connect to database")


def db_fetch(sql):
    db = db_connect()
    cur = db.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    db.close()
    return data


def db_aggregate():
    db = db_connect()
    cur = db.cursor()
    cur.execute(
        # "DELETE FROM portfolio WHERE ((MINUTE(timestamp) != 0 and timestamp < UTC_TIMESTAMP() - INTERVAL 1 WEEK ));"
        "DELETE FROM db.portfolio WHERE ((MINUTE(timestamp) != 0 and timestamp < UTC_TIMESTAMP() - INTERVAL 1 DAY ));"
    )
    db.commit()
    db.close()


def db_insert(table, obj):
    db = db_connect()
    cur = db.cursor()
    sql_string = "INSERT INTO %s (%s) VALUES %s" % (
        table,
        ', '.join(obj.keys()),
        json_to_values_string(obj)
    )
    sql_string = sql_string[:-2] + ";"
    cur.execute(sql_string)
    db.commit()
    db.close()
    return


def db_insert_test(table, obj):
    sql_string = "INSERT INTO %s (%s) VALUES %s" % (
        table,
        ', '.join(obj.keys()),
        json_to_values_string(obj)
    )
    sql_string = sql_string[:-2] + ";"
    print(sql_string)
    return sql_string


def db_insert_many(table, records):
    db = db_connect()
    cur = db.cursor()
    if table == "binance_orders":
        cur.execute("TRUNCATE TABLE db.binance_orders")
    if table == "binance_balances":
        cur.execute("TRUNCATE TABLE db.binance_balances")
    if table == "marketcap":
        cur.execute("TRUNCATE TABLE db.marketcap")
    sql_string = "INSERT INTO %s (%s) VALUES %s" % (
        table,
        ', '.join([list(x.keys()) for x in records][0]),
        json_to_values_string_many(records)
    )
    sql_string = sql_string[:-2] + ";"
    cur.execute(sql_string)
    db.commit()
    db.close()
    return


def db_insert_many_test(table, records):
    sql_string = "INSERT INTO %s (%s) VALUES %s" % (
        table,
        ', '.join([list(x.keys()) for x in records][0]),
        json_to_values_string_many(records)
    )
    sql_string = sql_string[:-2] + ";"
    print(sql_string)
    return sql_string


def json_to_values_string(obj):
    # create a nested list of the records' values
    # value string for the SQL string
    values_str = ""
    # declare empty list for values
    val_list = []

    # append each value to a new list of values
    for v, val in enumerate(obj):
        # if isinstance(obj[val], list):
        #     val_list.append("'" + str(Json(obj[val])).replace('"', '') + "'")
        if type(obj[val]) == str:
            val_list.append(str(Json(obj[val])).replace('"', ''))
        elif obj[val] is None:
            val_list.append("NULL")
        else:
            val_list.append(str(obj[val]))

    # put parenthesis around each record string
    values_str += "(" + ', '.join(val_list) + "), "

    return values_str


def json_to_values_string_many(records):
    values_str = ""
    for i, obj in enumerate(records):
        values_str += json_to_values_string(obj)

    return values_str


def job_success(*args):
    print(datetime.utcnow() - args[0].enqueued_at)
    save_job_result(
        args[0].id,
        str(args[0].enqueued_at),
        1,
        str(datetime.utcnow() - args[0].enqueued_at),
        None
    )


def job_failure(*args):
    error = str(args[3])
    error = error if len(error) < 150 else "error message too long"
    save_job_result(
        args[0].id,
        str(args[0].enqueued_at),
        0,
        str(datetime.utcnow() - args[0].enqueued_at),
        error
    )


def save_job_result(job, timestamp, success, duration, error):
    job_result = {
        'timestamp': timestamp,
        'job': job,
        'success': success,
        'duration': duration,
        'error': error
    }
    db_insert('job', job_result)

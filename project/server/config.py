# project/server/config.py
import logging
import os

import mysql.connector as mariadb
# import the new JSON method from psycopg2
from psycopg2.extras import Json

# import Python's JSON lib

basedir = os.path.abspath(os.path.dirname(__file__))


def os_get(var):
    return os.environ.get(var)


class BaseConfig(object):
    """Base configuration."""
    NOMICS_KEY = os_get("NOMICS_KEY")
    WTF_CSRF_ENABLED = True
    REDIS_URL = "redis://redis:6379/0"
    QUEUES = ["default"]
    # Exchanges
    # BINANCE_KEY = os_get("BINANCE_KEY")
    # BINANCE_SECRET = os_get("BINANCE_SECRET")
    # BITMEX_KEY = os_get("BITMEX_KEY")
    # BITMEX_SECRET = os_get("BITMEX_SECRET")
    # Database
    # SQLALCHEMY_DATABASE_URI = os_get("SQLALCHEMY_DATABASE_URI")
    # SQLALCHEMY_ECHO = False
    # SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    WTF_CSRF_ENABLED = False


class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False


def db_connect():
    try:
        db = mariadb.connect(**{
            'host': 'mariadb',
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
        "DELETE FROM portfolio WHERE ((MINUTE(timestamp) != 0 and timestamp < UTC_TIMESTAMP() - INTERVAL 1 DAY ));"
    )
    db.commit()
    db.close()


def db_insert(table, obj):
    db = db_connect()
    cur = db.cursor()
    # if table == "portfolio_current":
    #     cur.execute("TRUNCATE TABLE portfolio_current")
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
        cur.execute("TRUNCATE TABLE binance_orders")
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

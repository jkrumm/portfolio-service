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


def db_insert(table, obj):
    db = db_connect()
    cur = db.cursor()
    sql_string = "INSERT INTO %s (%s)\nVALUES %s" % (
        table,
        ', '.join(obj.keys()),
        json_to_values_string(obj)
    )
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
            val = str(Json(obj[val])).replace('"', '')
        val_list += [str(val)]

    # put parenthesis around each record string
    values_str += "(" + ', '.join(val_list) + "),\n"

    # remove the last comma and end SQL with a semicolon
    return values_str[:-2] + ";"


def json_to_values_string_old(obj):
    # create a nested list of the records' values
    values = [list(x.values()) for x in obj]
    # value string for the SQL string
    values_str = ""

    # enumerate over the records' values
    for i, record in enumerate(values):

        # declare empty list for values
        val_list = []

        # append each value to a new list of values
        for v, val in enumerate(record):
            if type(val) == str:
                val = str(Json(val)).replace('"', '')
            val_list += [str(val)]

        # put parenthesis around each record string
        values_str += "(" + ', '.join(val_list) + "),\n"

    # remove the last comma and end SQL with a semicolon
    return values_str[:-2] + ";"

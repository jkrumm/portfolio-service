# project/server/config.py

import os

import mysql.connector as mariadb

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Base configuration."""
    NOMICS_KEY = os.environ.get("NOMICS_KEY")
    WTF_CSRF_ENABLED = True
    REDIS_URL = "redis://redis:6379/0"
    QUEUES = ["default"]
    # Exchanges
    # BINANCE_KEY = os.environ.get("BINANCE_KEY")
    # BINANCE_SECRET = os.environ.get("BINANCE_SECRET")
    # BITMEX_KEY = os.environ.get("BITMEX_KEY")
    # BITMEX_SECRET = os.environ.get("BITMEX_SECRET")
    # Database
    # SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
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


dbConfig = {
    'host': 'mariadb',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'database': 'db'
}


def fetchAll(sql):
    mariadb_connection = mariadb.connect(**dbConfig)
    cur = mariadb_connection.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    mariadb_connection.close()
    return data

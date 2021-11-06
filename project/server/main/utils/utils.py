import os
import datetime

import redis
import requests
from flask import current_app
from nomics import Nomics
from rq import Queue, Worker, Connection

basedir = os.path.abspath(os.path.dirname(__file__))


def os_get(var):
    return os.environ.get(var)


def get_worker_stats():
    redis_connection = redis.from_url(current_app.config["REDIS_URL"])
    with Connection(redis_connection):
        queue = Queue()
        workers = Worker.all(queue=queue)
        worker = workers[0]
        birth_date = worker.birth_date
        return {
            'birth_date': str(birth_date),
            'lifetime': str(datetime.datetime.utcnow() - birth_date),
            'successful_job_count': worker.successful_job_count,  # Number of jobs finished successfully
            'failed_job_count': worker.failed_job_count,  # Number of failed jobs processed by this worker
            'total_working_time': f(worker.total_working_time)  # Amount of time spent executing jobs (in seconds)
        }


def get_nomics():
    return Nomics(os_get('NOMICS_KEY'))


def percentage(one, two):
    if (one and two and float(one) > 0.0 and float(two) > 0.0):
        return round((float(one) / float(two) - 1) * 100, 2)
    else:
        return None


def integer(val):
    if val:
        return int(float(val))
    else:
        return None


def f(val):
    if val:
        f = float(val)
        if f > 100000:
            return int(f)
        elif 0 < f < 0.001:
            return round(f, 6)
        else:
            return round(f, 2)
    else:
        return None


def f_btc(val):
    if val:
        return round(float(val), 6)
    else:
        return None


def get_json(url):
    response = requests.get(url)
    response.raise_for_status()  # raises exception when not a 2xx response
    if response.status_code != 204:
        return list(response.json())


def get_time():
    ts = datetime.datetime.utcnow()
    return ts - datetime.timedelta(minutes=ts.minute % 5,
                                   seconds=ts.second,
                                   microseconds=ts.microsecond)


def transform_time(string):
    ts = datetime.datetime.strptime(string, "%Y-%m-%dT%H:%M:%SZ")
    return ts - datetime.timedelta(minutes=ts.minute % 5,
                                   seconds=ts.second,
                                   microseconds=ts.microsecond)


def transform_time_ccxt(string):
    ts = datetime.datetime.strptime(string, "%Y-%m-%dT%H:%M:%S.%fZ")
    return ts - datetime.timedelta(minutes=ts.minute % 5,
                                   seconds=ts.second,
                                   microseconds=ts.microsecond)


def transform_interval(n):
    if int(n) == 480:
        return '8H'
    if int(n) == 720:
        return '12H'
    if int(n) == 1:
        return '1D'


def drop_keys(obj, keys):
    for key in keys:
        obj.remove(key)
    return obj


def map_portfolio(records):
    result = []
    for i, obj in enumerate(records):
        result.append(
            {
                "id": obj[0],
                "timestamp": obj[1],
                "btc_usd": obj[2],
                "eth_usd": obj[3],
                "current": obj[4],
                "current_btc": obj[5],
                "current_24h": obj[6],
                "current_1w": obj[7],
                "current_btc_24h": obj[8],
                "current_btc_1w": obj[9],
                "current_percentage": obj[10],
                "total": obj[11],
                "total_btc": obj[12],
                "total_24h": obj[13],
                "total_1w": obj[14],
                "total_btc_24h": obj[15],
                "total_btc_1w": obj[16],
                "binance_total": obj[17],
                "binance_total_btc": obj[18],
                "binance_total_24h": obj[19],
                "binance_total_1w": obj[20],
                "binance_count": obj[21],
                "bitmex_total": obj[22],
                "bitmex_total_btc": obj[23],
                "bitmex_total_24h": obj[24],
                "bitmex_total_1w": obj[25],
                "bitmex_margin": obj[26],
                "bitmex_margin_24h": obj[27],
                "bitmex_margin_1w": obj[28],
                "bitmex_margin_btc": obj[29],
                "bitmex_margin_percent": obj[30],
                "bitmex_margin_leverage": obj[31],
                "bitmex_available_margin": obj[32],
                "bitmex_available_margin_btc": obj[33],
                "bitmex_unrealised": obj[34],
                "bitmex_unrealised_24h": obj[35],
                "bitmex_unrealised_1w": obj[36],
                "bitmex_unrealised_btc": obj[37],
                "bitmex_unrealised_percentage": obj[38],
                "bitmex_withdraw": obj[39],
                "bitmex_withdraw_btc": obj[40],
                "bitmex_btc_position": obj[41],
                "bitmex_btc_position_btc": obj[42],
                "bitmex_btc_position_24h": obj[43],
                "bitmex_btc_position_percentage": obj[44],
                "bitmex_btc_position_type": obj[45],
                "bitmex_btc_position_leverage": obj[46],
                "bitmex_btc_position_opening": obj[47],
                "bitmex_btc_position_opening_date": obj[48],
                "bitmex_eth_position": obj[49],
                "bitmex_eth_position_btc": obj[50],
                "bitmex_eth_position_24h": obj[51],
                "bitmex_eth_position_percentage": obj[52],
                "bitmex_eth_position_type": obj[53],
                "bitmex_eth_position_leverage": obj[54],
                "bitmex_eth_position_opening": obj[55],
                "bitmex_eth_position_opening_date": obj[56],
            })
        return result

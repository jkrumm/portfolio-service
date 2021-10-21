import datetime
import os

import requests
from nomics import Nomics


def get_nomics():
    return Nomics(os.environ.get('NOMICS_KEY'))


def percentage(one, two):
    if (one and two and float(one) > 0.0 and float(two) > 0.0):
        return round((float(one) / float(two) - 1) * 100, 2)
    else:
        return None


def f(string):
    if string:
        f = float(string)
        if f > 100000:
            return int(f)
        else:
            return round(f, 2)
    else:
        return None


def get_json(url):
    response = requests.get(url)
    response.raise_for_status()  # raises exception when not a 2xx response
    if response.status_code != 204:
        return list(response.json())


def get_time():
    ts = datetime.datetime.now()
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

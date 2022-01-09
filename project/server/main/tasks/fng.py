import time
import logging

import requests
import json
import datetime

from project.server.main.utils.db import db_insert_many
from project.server.main.utils.utils import f


def fng():
    start = time.perf_counter()
    print("TASK: fng started")
    logging.info("TASK: fng started")

    url = ("https://api.alternative.me/fng/?limit=99999999")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    output = json.loads(response.content)

    fng = []

    for d in output['data']:
        fng.append({
            'timestamp': str(datetime.datetime.fromtimestamp(int(d['timestamp'])).date()),
            'value': d['value'],
            'value_classification': d['value_classification'],
        })

    db_insert_many("fng", fng)

    end = time.perf_counter()
    print("TASK: fng completed in " + str(f(end - start)) + "s")
    logging.info("TASK: fng completed in " + str(f(end - start)) + "s")
    return True

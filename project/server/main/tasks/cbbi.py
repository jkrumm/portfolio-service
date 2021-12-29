import time
import logging

import requests
import json
import datetime

from project.server.main.utils.db import db_insert_many
from project.server.main.utils.utils import f


def cbbi():
    start = time.perf_counter()
    print("TASK: cbbi started")
    logging.info("TASK: cbbi started")

    url = ("https://colintalkscrypto.com/cbbi/data/latest.json")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    output = json.loads(response.content)

    data = {
        'price': output['Price'],
        'confidence': output['Confidence'],
        'puell': output['Puell'],
        'mvrv': output['MVRV'],
        'rhodl': output['RHODL'],
    }

    cbbi = []

    for key in data['confidence']:
        cbbi.append({
            'timestamp': str(datetime.datetime.fromtimestamp(int(key)).date()),
            'price': f(data['price'][key]),
            'confidence': f(data['confidence'][key] * 100),
            'puell': f(data['puell'][key] * 100),
            'mvrv': f(data['mvrv'][key] * 100),
            'rhodl': f(data['rhodl'][key] * 100),
        })

    db_insert_many("cbbi", cbbi)

    end = time.perf_counter()
    print("TASK: cbbi completed in " + str(f(end - start)) + "s")
    logging.info("TASK: cbbi completed in " + str(f(end - start)) + "s")
    return True

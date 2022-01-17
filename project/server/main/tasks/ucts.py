import time

import logging

from project.server.main.utils.db import db_insert
from project.server.main.utils.utils import f, os_get, get_time

from bs4 import BeautifulSoup
from datetime import datetime
import requests


def ucts():
    start = time.perf_counter()
    print("TASK: ucts started")
    logging.info("TASK: ucts started")

    ucts = {}
    with requests.session() as s:
        # get token
        s.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'})
        get_token = s.get('https://cryptobot.azurewebsites.net/Account/Login')
        soup = BeautifulSoup(get_token.text, features="html.parser")
        token = soup.find('input', {'name': '__RequestVerificationToken'}).get('value')

        # post login
        post_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'Email': os_get('UCTS_MAIL'), 'Password': os_get('UCTS_PW'), '__RequestVerificationToken': token}
        s.post("https://cryptobot.azurewebsites.net/Account/Login", data=data, headers=post_headers, cookies=s.cookies)

        # get dashboard and map data
        dashboard = s.get('https://cryptobot.azurewebsites.net/Dashboard', cookies=s.cookies)
        soup = BeautifulSoup(dashboard.text, features="html.parser")
        data = []
        rows = soup.find('table').find('tbody').find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        btc = data[0]
        eth = data[1]
        ucts = {
            'timestamp': str(get_time()),
            'btc_2h_side': btc[0].split()[0],
            'btc_2h_date': str(datetime.strptime(btc[0].split()[1], '%m/%d/%Y').date()),
            'btc_4h_side': btc[1].split()[0],
            'btc_4h_date': str(datetime.strptime(btc[1].split()[1], '%m/%d/%Y').date()),
            'btc_8h_side': btc[2].split()[0],
            'btc_8h_date': str(datetime.strptime(btc[2].split()[1], '%m/%d/%Y').date()),
            'btc_12h_side': btc[3].split()[0],
            'btc_12h_date': str(datetime.strptime(btc[3].split()[1], '%m/%d/%Y').date()),
            'btc_1d_side': btc[4].split()[0],
            'btc_1d_date': str(datetime.strptime(btc[4].split()[1], '%m/%d/%Y').date()),
            'eth_2h_side': eth[0].split()[0],
            'eth_2h_date': str(datetime.strptime(eth[0].split()[1], '%m/%d/%Y').date()),
            'eth_4h_side': eth[1].split()[0],
            'eth_4h_date': str(datetime.strptime(eth[1].split()[1], '%m/%d/%Y').date()),
            'eth_8h_side': eth[2].split()[0],
            'eth_8h_date': str(datetime.strptime(eth[2].split()[1], '%m/%d/%Y').date()),
            'eth_12h_side': eth[3].split()[0],
            'eth_12h_date': str(datetime.strptime(eth[3].split()[1], '%m/%d/%Y').date()),
            'eth_1d_side': eth[4].split()[0],
            'eth_1d_date': str(datetime.strptime(eth[4].split()[1], '%m/%d/%Y').date()),
        }
    print(ucts)

    db_insert('ucts', ucts)

    end = time.perf_counter()
    print("TASK: ucts completed in " + str(f(end - start)) + "s")
    logging.info("TASK: ucts completed in " + str(f(end - start)) + "s")
    return True

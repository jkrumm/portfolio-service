import logging
import time
from datetime import datetime, timedelta
from pprint import pprint

import ccxt
import pandas as pd

from project.server.main.utils.db import db_insert, db_insert_many, db_fetch, db_aggregate, db_insert_test
from project.server.main.utils.utils import f, get_time, transform_time_ccxt, get_json, f_btc, percentage, \
    map_portfolio, os_get, integer


def pnl():
    start = time.perf_counter()
    print("TASK: pnl started")
    logging.info("TASK: pnl started")

    portfolio_24h = db_fetch("SELECT * FROM db.portfolio WHERE timestamp > '%s' ORDER BY timestamp ASC LIMIT 1;" % str(
        datetime.utcnow() - timedelta(hours=24)))
    portfolio_24h = map_portfolio(portfolio_24h)[0] if portfolio_24h else None

    portfolio_recent = db_fetch("SELECT * FROM db.portfolio ORDER BY timestamp DESC LIMIT 1;")
    portfolio_recent = map_portfolio(portfolio_recent)[0] if portfolio_recent else None

    pnl_24h = db_fetch("SELECT * FROM db.pnl WHERE timestamp > '%s' ORDER BY timestamp ASC LIMIT 1;" % str(
        datetime.utcnow() - timedelta(hours=24)))
    # pprint(map_portfolio(portfolio_24h))
    #
    # portfolio_1w = db_fetch("SELECT * FROM db.portfolio WHERE timestamp > '%s' ORDER BY timestamp DESC LIMIT 1;" % str(
    #     datetime.utcnow() - timedelta(days=7)))
    # portfolio_1w = map_portfolio(portfolio_1w)[0] if portfolio_1w else None

    pnl = {}
    pnl['timestamp'] = str(get_time())

    pnl['current'] = portfolio_recent['current'] if portfolio_recent else None
    pnl['current_btc'] = portfolio_recent['current_btc'] if portfolio_recent else None
    pnl['current_24h'] = portfolio_recent['current_24h'] if portfolio_recent else None
    pnl['current_btc_24h'] = portfolio_recent['current_btc_24h'] if portfolio_recent else None

    pnl['binance_total'] = portfolio_recent['binance_total'] if portfolio_recent else None
    pnl['binance_total_24h'] = portfolio_recent['binance_total_24h'] if portfolio_recent else None
    pnl['binance_total_btc'] = portfolio_recent['binance_total_btc'] if portfolio_recent else None

    pnl['bitmex_total'] = portfolio_recent['bitmex_total'] if portfolio_recent else None
    pnl['bitmex_total_btc'] = portfolio_recent['bitmex_total_btc'] if portfolio_recent else None
    pnl['bitmex_total_24h'] = portfolio_recent['bitmex_total_24h'] if portfolio_recent else None

    pnl['pnl'] = f(
        f(portfolio_recent['current']) - f(portfolio_24h['current'])) if portfolio_24h and portfolio_recent else None
    pnl['pnl_binance'] = f(f(portfolio_recent['binance_total']) - f(
        portfolio_24h['binance_total'])) if portfolio_24h and portfolio_recent else None
    pnl['pnl_bitmex'] = f(f(portfolio_recent['bitmex_total']) - f(
        portfolio_24h['bitmex_total'])) if portfolio_24h and portfolio_recent else None

    pnl['pnl_cum'] = f(f(portfolio_recent['current_24h']) + f(pnl_24h[0][4])) if len(
        pnl_24h) > 0 and pnl_24h[0][4] and portfolio_recent and portfolio_recent['current_24h'] else None

    db_insert('pnl', pnl)

    end = time.perf_counter()
    print("TASK: pnl completed in " + str(f(end - start)) + "s")
    logging.info("TASK: pnl completed in " + str(f(end - start)) + "s")

    return True

import time

import logging

from project.server.main.utils.db import db_fetch
from project.server.main.utils.notifications import pushover
from project.server.main.utils.utils import f, get_worker_stats, map_portfolio


# import pprint as pp


def daily_push():
    start = time.perf_counter()
    print("TASK: daily_push started")
    logging.info("TASK: daily_push started")

    portfolio = db_fetch("SELECT * FROM portfolio ORDER BY timestamp DESC LIMIT 1;")
    portfolio = map_portfolio(portfolio)[0] if portfolio else None
    # pnl = db_fetch("SELECT * FROM pnl ORDER BY timestamp DESC LIMIT 1;")[0]
    cbbi = db_fetch("SELECT confidence FROM cbbi ORDER BY timestamp DESC LIMIT 1;")[0][0]
    fng = db_fetch("SELECT * FROM fng LIMIT 1;")[0]
    orders = db_fetch("SELECT * FROM binance_orders ORDER BY market_percentage ASC LIMIT 3;")

    worker_stats = get_worker_stats()
    failures = \
        db_fetch(
            "SELECT COUNT(success) as failures FROM job WHERE (success = 0 AND timestamp > UTC_TIMESTAMP() - INTERVAL 1 DAY);")[
            0][0]
    successful = \
        db_fetch(
            "SELECT COUNT(success) as successful FROM job WHERE (success = 1 AND timestamp > UTC_TIMESTAMP() - INTERVAL 1 DAY);")[
            0][0]

    html = f'<b>Global</b><br/>BTC:&nbsp;{int(portfolio["btc_usd"])}$<br/>ETH:&nbsp;{int(portfolio["eth_usd"])}$<br/>CBBI:&nbsp;{int(cbbi)}%<br/>FNG:&nbsp;{fng[2]}%&nbsp;/&nbsp;{fng[3]}<br/><br/><b>Portfolio</b><br/>Total:&nbsp;{int(portfolio["current"])}$&nbsp;/&nbsp;{portfolio["current_24h"]}%<br/>Binance:&nbsp;{int(portfolio["binance_total"])}$&nbsp;/&nbsp;{portfolio["binance_total_24h"]}%<br/>Bitmex:&nbsp;{int(portfolio["bitmex_total"])}$&nbsp;/&nbsp;{portfolio["bitmex_total_24h"]}%<br/><br/><b>Orders</b><br/>{orders[0][2]}&nbsp;/&nbsp;{orders[0][3]}&nbsp;/&nbsp;{orders[0][7]}%<br/>{orders[1][2]}&nbsp;/&nbsp;{orders[1][3]}&nbsp;/&nbsp;{orders[1][7]}%<br/>{orders[2][2]}&nbsp;/&nbsp;{orders[2][3]}&nbsp;/&nbsp;{orders[2][7]}%<br/><br/><b>Jobs</b><br/>Successful:&nbsp;{successful}<br/>Failures:&nbsp;{failures}<br/>Lifetime:&nbsp;{worker_stats["lifetime"]}<br/>Working time:&nbsp;{worker_stats["working_time"]}<br/>'

    pushover('Daily', html, '-1', '1')

    end = time.perf_counter()
    print("TASK: daily_push completed in " + str(f(end - start)) + "s")
    logging.info("TASK: daily_push completed in " + str(f(end - start)) + "s")
    return True

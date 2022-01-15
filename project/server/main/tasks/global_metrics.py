import time
import logging

import requests
import json

from project.server.main.utils.db import db_insert
from project.server.main.utils.utils import f, os_get, get_time


def global_metrics():
    start = time.perf_counter()
    print("TASK: global started")
    logging.info("TASK: global started")

    url = ("https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest")
    headers = {'X-CMC_PRO_API_KEY': os_get("COINMARKETCAP_KEY")}
    response = requests.get(url, headers=headers)
    output = json.loads(response.content)["data"]

    obj = {
        "timestamp": str(get_time()),
        "btc_dominance": f(output["btc_dominance"]),
        "eth_dominance": f(output["eth_dominance"]),
        "total_market_cap": f(output["quote"]["USD"]["total_market_cap"]),
        "total_volume_24h": f(output["quote"]["USD"]["total_volume_24h"]),
        "altcoin_volume_24h": f(output["quote"]["USD"]["altcoin_volume_24h"]),
        "altcoin_market_cap": f(output["quote"]["USD"]["altcoin_market_cap"]),
        "defi_volume_24h": f(output["quote"]["USD"]["defi_volume_24h"]),
        "defi_market_cap": f(output["quote"]["USD"]["defi_market_cap"]),
        "stablecoin_volume_24h": f(output["quote"]["USD"]["stablecoin_volume_24h"]),
        "stablecoin_market_cap": f(output["quote"]["USD"]["stablecoin_market_cap"]),
        "derivatives_volume_24h": f(output["quote"]["USD"]["derivatives_volume_24h"]),
    }

    db_insert("global", obj)

    end = time.perf_counter()
    print("TASK: global completed in " + str(f(end - start)) + "s")
    logging.info("TASK: global completed in " + str(f(end - start)) + "s")
    return True

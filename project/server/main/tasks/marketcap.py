import logging
import os
import time
from datetime import datetime

from project.server.main.utils.utils import percentage, get_json


def marketcap():
    print("TASK: marketcap")
    return True


def marketcap_current():
    start = time.perf_counter()
    print("TASK: marketcap_current")
    logging.info("TASK: marketcap_current")

    ########################
    # Get Dashboard
    ########################
    dashboard_fetched = get_json("https://api.nomics.com/v1/currencies/ticker?key=" + os.environ.get(
        'NOMICS_KEY') + "&interval=1d,30d,7d&convert=USD&sort=rank")[:250]
    print(len(dashboard_fetched))
    print(dashboard_fetched[0:2])

    # TOD Cache query
    # cryptocurrencies = requests.get(
    #     'https://raw.githubusercontent.com/crypti/cryptocurrencies/master/cryptocurrencies.json').json()

    dashboard = []
    ids = []

    for i in dashboard_fetched:
        ids.append(i.get('id'))
        dashboard.append({
            "currency": "BTC",
            "name": i.get('name'),  # not
            "logo_url": i.get('logo_url'),  # not
            "price": i.get('price'),
            # "price_date": i.get('id'),
            "price_timestamp": datetime.strptime(i.get('price_timestamp'), "%Y-%m-%dT%H:%M:%SZ") if i.get(
                'high_timestamp') else None,
            "circulating_supply": i.get('circulating_supply'),  # not
            "max_supply": i.get('max_supply'),  # not
            "market_cap": i.get('market_cap'),
            "market_cap_dominance": i.get('market_cap_dominance'),
            "first_trade": datetime.strptime(i.get('first_trade'), "%Y-%m-%dT%H:%M:%SZ") if i.get(
                'first_trade') else None,  # not
            "rank": i.get('rank'),
            "rank_delta": i.get('rank_delta'),  # not
            "high": i.get('high'),  # not
            "high_percentage": percentage(i.get('price'), i.get('high')),  # not
            "high_timestamp": datetime.strptime(i.get('high_timestamp'), "%Y-%m-%dT%H:%M:%SZ") if i.get(
                'high_timestamp') else None,  # not
            "1d_volume": i.get('1d').get('volume'),
            "1d_volume_change_pct": i.get('1d').get('volume_change_pct'),
            "1d_price_change": i.get('1d').get('price_change'),  # not
            "1d_price_change_pct": i.get('1d').get('price_change_pct'),  # not
            "7d_volume": i.get('7d').get('volume'),
            "7d_volume_change_pct": i.get('7d').get('volume_change_pct'),
            "7d_price_change": i.get('7d').get('price_change'),  # not
            "7d_price_change_pct": i.get('7d').get('price_change_pct'),  # not
            "30d_volume": i.get('30d').get('volume'),
            "30d_volume_change_pct": i.get('30d').get('volume_change_pct'),
            "30d_price_change": i.get('30d').get('price_change'),  # not
            "30d_price_change_pct": i.get('30d').get('price_change_pct'),  # not
        })

    # dashboard = sorted(dashboard, key=lambda k: k['marketcap'])[::-1][:200]

    ########################
    # Add Sparklines
    ########################

    sparklines_fetched = get_json(
        "https://api.nomics.com/v1/currencies/sparkline?key=" + os.environ.get('NOMICS_KEY') + "&ids=" + str(ids)[
                                                                                                         1:-1].replace(
            " ", "").replace("'", "") + "&start=2018-04-14T00%3A00%3A00Z&end=2018-05-14T00%3A00%3A00Z")

    for idx, val in enumerate(dashboard):
        for i in sparklines_fetched:
            if val['currency'] == i['currency']:
                dashboard[idx]['sparkline_timestamps'] = i['timestamps']
                dashboard[idx]['sparkline_prices'] = i['prices']

    print(len(dashboard))
    print(dashboard[0:2])

    end = time.perf_counter()
    print(f"ELAPSED TIME: {end - start:0.2f} seconds")
    return True

import datetime
import logging
import time

from project.server.main.utils.db import db_insert_many
from project.server.main.utils.utils import percentage, get_json, f, get_time, transform_time, os_get, mil


def marketcap():
    start = time.perf_counter()
    print("TASK: marketcap started")
    logging.info("TASK: marketcap started")

    ########################
    # Get Dashboard
    ########################
    dashboard_fetched = get_json("https://api.nomics.com/v1/currencies/ticker?key=" + os_get(
        'NOMICS_KEY') + "&interval=1d,30d,7d&convert=USD&sort=rank")[:101]
    # print(len(dashboard_fetched))
    # print(dashboard_fetched[0:2])

    dashboard = []
    ids = []

    for i in dashboard_fetched:
        if len(ids) <= 100:
            ids.append(i.get('id'))
        dashboard.append({
            "timestamp": str(get_time()),
            "symbol": i.get('currency'),
            "name": i.get('name'),
            "price": f(i.get('price')),
            "marketcap": mil(i.get('market_cap')),
            "marketcap_dominance": f(float(i.get('market_cap_dominance')) * 100) if i.get(
                'market_cap_dominance') else None,
            "rank_delta": i.get('rank_delta'),
            "high": f(i.get('high')),
            "high_percentage": f(percentage(i.get('price'), i.get('high')) * 100),
            "high_timestamp": str(transform_time(i.get('high_timestamp')) if i.get('high_timestamp') else None),
            "1d_volume": mil(i.get('1d').get('volume')) if i.get('1d') else None,
            "1d_price_change": f(i.get('1d').get('price_change')) if i.get('1d') else None,
            "1d_price_change_pct": f(float(i.get('1d').get('price_change_pct')) * 100) if i.get('1d') and i.get(
                '1d').get('price_change_pct') else None,
            "1d_volume_change_pct": f(float(i.get('1d').get('volume_change_pct')) * 100) if i.get('1d') and i.get(
                '1d').get('volume_change_pct') else None,
            "7d_volume": mil(i.get('7d').get('volume')) if i.get('7d') else None,
            "7d_volume_change_pct": f(float(i.get('7d').get('volume_change_pct')) * 100) if i.get('7d') and i.get(
                '7d').get('volume_change_pct') else None,
            "7d_price_change": f(i.get('7d').get('price_change')) if i.get('7d') and i.get('7d').get(
                'price_change') else None,
            "7d_price_change_pct": f(float(i.get('7d').get('price_change_pct')) * 100) if i.get('7d') and i.get(
                '7d').get('price_change_pct') else None,
            "30d_volume": mil(i.get('30d').get('volume')) if i.get('30d') else None,
            "30d_volume_change_pct": f(float(i.get('7d').get('price_change_pct')) * 100) if i.get('30d') and i.get(
                '30d').get('price_change_pct') else None,
            "30d_price_change": f(i.get('30d').get('price_change')) if i.get('30d') and i.get('30d').get(
                'price_change') else None,
            "30d_price_change_pct": f(float(i.get('30d').get('price_change_pct')) * 100) if i.get('30d') and i.get(
                '30d').get('price_change_pct') else None,
        })

    dashboard[:] = [d for d in dashboard if d.get('symbol') != 'HEX']

    dashboard = sorted(dashboard, key=lambda k: k['marketcap'])[::-1][:100]

    ########################
    # Add Sparklines
    ########################

    url = "https://api.nomics.com/v1/currencies/sparkline?key=" + os_get('NOMICS_KEY')
    url += "&ids=" + str(ids)[1:-1].replace(" ", "").replace("'", "")
    url += "&end=" + datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    url += "&start=" + (datetime.datetime.utcnow() - datetime.timedelta(days=42)).strftime("%Y-%m-%dT%H:%M:%SZ")

    sparklines_fetched = get_json(url)

    for idx, val in enumerate(dashboard):
        for i in sparklines_fetched:
            if val['symbol'] == i['currency']:
                prices = []
                for p in i['prices']:
                    prices.append(f(p))
                dashboard[idx]['sparkline'] = str(prices)

    # print(len(dashboard))
    # pprint(dashboard[0:2])

    db_insert_many("marketcap", dashboard)

    end = time.perf_counter()
    print("TASK: marketcap completed in " + str(f(end - start)) + "s")
    logging.info("TASK: marketcap completed in " + str(f(end - start)) + "s")

    return True

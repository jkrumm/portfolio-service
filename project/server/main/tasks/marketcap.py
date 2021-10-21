import datetime
import logging
import os
import time

from project.server.main.utils.utils import percentage, get_json, f, get_time, transform_time


def marketcap():
    print("TASK: marketcap")
    return True


def marketcap_current():
    start = time.perf_counter()
    print("TASK: marketcap_current started")
    logging.info("TASK: marketcap_current started")

    ########################
    # Get Dashboard
    ########################
    dashboard_fetched = get_json("https://api.nomics.com/v1/currencies/ticker?key=" + os.environ.get(
        'NOMICS_KEY') + "&interval=1d,30d,7d&convert=USD&sort=rank")[:100]
    print(len(dashboard_fetched))
    print(dashboard_fetched[0:2])

    # TOD Cache query
    # cryptocurrencies = requests.get(
    #     'https://raw.githubusercontent.com/crypti/cryptocurrencies/master/cryptocurrencies.json').json()

    dashboard = []
    ids = []

    for i in dashboard_fetched:
        if len(ids) <= 100:
            ids.append(i.get('id'))
        dashboard.append({
            "currency": "BTC",
            "name": i.get('name'),  # not
            "price": f(i.get('price')),
            "time": str(get_time()),
            "logo_url": i.get('logo_url'),  # not
            "circulating_supply": f(i.get('circulating_supply')),  # not
            "max_supply": f(i.get('max_supply')),  # not
            "market_cap": f(i.get('market_cap')),
            "market_cap_dominance": f(float(i.get('market_cap_dominance')) * 100) if i.get(
                'market_cap_dominance') else None,
            "first_trade": str(transform_time(i.get('first_trade')) if i.get('first_trade') else None),  # not
            "rank": i.get('rank'),
            "rank_delta": i.get('rank_delta'),  # not
            "high": f(i.get('high')),  # not
            "high_percentage": f(percentage(i.get('price'), i.get('high')) * 100),  # not
            "high_timestamp": str(transform_time(i.get('high_timestamp')) if i.get('high_timestamp') else None),  # not
            "1d_volume": f(i.get('1d').get('volume')) if i.get('1d') else None,
            "1d_price_change": f(i.get('1d').get('price_change')) if i.get('1d') else None,  # not
            "1d_price_change_pct": f(float(i.get('1d').get('price_change_pct')) * 100) if i.get('1d') and i.get(
                '1d').get('price_change_pct') else None,  # not
            "7d_volume": f(i.get('7d').get('volume')) if i.get('7d') else None,
            "7d_volume_change_pct": f(float(i.get('7d').get('volume_change_pct')) * 100) if i.get('7d') and i.get(
                '7d').get('volume_change_pct') else None,
            "7d_price_change": f(i.get('7d').get('price_change')) if i.get('7d') and i.get('7d').get(
                'price_change') else None,  # not
            "7d_price_change_pct": f(float(i.get('7d').get('price_change_pct')) * 100) if i.get('7d') and i.get(
                '7d').get('price_change_pct') else None,  # not
            "30d_volume": f(i.get('30d').get('volume')) if i.get('30d') else None,
            "30d_volume_change_pct": f(float(i.get('7d').get('price_change_pct')) * 100) if i.get('30d') and i.get(
                '30d').get('price_change_pct') else None,
            "30d_price_change": f(i.get('30d').get('price_change')) if i.get('30d') and i.get('30d').get(
                'price_change') else None,  # not
            "30d_price_change_pct": f(float(i.get('30d').get('price_change_pct')) * 100) if i.get('30d') and i.get(
                '30d').get('price_change_pct') else None,  # not
        })

    # dashboard = sorted(dashboard, key=lambda k: k['marketcap'])[::-1][:200]

    ########################
    # Add Sparklines
    ########################

    url = "https://api.nomics.com/v1/currencies/sparkline?key=" + os.environ.get('NOMICS_KEY')
    url += "&ids=" + str(ids)[1:-1].replace(" ", "").replace("'", "")
    url += "&end=" + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    url += "&start=" + (datetime.datetime.now() - datetime.timedelta(days=44)).strftime("%Y-%m-%dT%H:%M:%SZ")

    sparklines_fetched = get_json(url)

    for idx, val in enumerate(dashboard):
        for i in sparklines_fetched:
            if val['currency'] == i['currency']:
                dashboard[idx]['sparkline_timestamps'] = i['timestamps']
                dashboard[idx]['sparkline_prices'] = i[
                    'prices']

    print(len(dashboard))
    print(dashboard[0:2])

    end = time.perf_counter()
    print("TASK: marketcap_current completed in " + str(f(end - start)) + "s")
    logging.info("TASK: marketcap_current completed in " + str(f(end - start)) + "s")
    return True

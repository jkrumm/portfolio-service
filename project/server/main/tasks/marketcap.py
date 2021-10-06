import datetime
import logging
import os
import time

from project.server.main.utils.utils import percentage, get_json, f


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
        if len(ids) <= 50:
            ids.append(i.get('id'))
        dashboard.append({
            "currency": "BTC",
            "name": i.get('name'),  # not
            "logo_url": i.get('logo_url'),  # not
            "price": f(i.get('price')),
            # "price_date": i.get('id'),
            "price_timestamp": str(datetime.datetime.strptime(i.get('price_timestamp'), "%Y-%m-%dT%H:%M:%SZ") if i.get(
                'high_timestamp') else None),
            "circulating_supply": f(i.get('circulating_supply')),  # not
            "max_supply": f(i.get('max_supply')),  # not
            "market_cap": f(i.get('market_cap')),
            "market_cap_dominance": f(float(i.get('market_cap_dominance')) * 100) if i.get(
                'market_cap_dominance') else None,
            "first_trade": str(datetime.datetime.strptime(i.get('first_trade'), "%Y-%m-%dT%H:%M:%SZ") if i.get(
                'first_trade') else None),  # not
            "rank": i.get('rank'),
            "rank_delta": i.get('rank_delta'),  # not
            "high": f(i.get('high')),  # not
            "high_percentage": f(percentage(i.get('price'), i.get('high')) * 100),  # not
            "high_timestamp": str(datetime.datetime.strptime(i.get('high_timestamp'), "%Y-%m-%dT%H:%M:%SZ") if i.get(
                'high_timestamp') else None),  # not
            "1d_volume": f(i.get('1d').get('volume')),
            "1d_price_change": f(i.get('1d').get('price_change')),  # not
            "1d_price_change_pct": f(float(i.get('1d').get('price_change_pct')) * 100) if i.get('1d').get(
                'price_change_pct') else None,  # not
            "7d_volume": f(i.get('7d').get('volume')),
            "7d_volume_change_pct": f(float(i.get('7d').get('volume_change_pct')) * 100) if i.get('7d').get(
                'volume_change_pct') else None,
            "7d_price_change": f(i.get('7d').get('price_change')),  # not
            "7d_price_change_pct": f(float(i.get('7d').get('price_change_pct')) * 100) if i.get('7d').get(
                'price_change_pct') else None,  # not
            "30d_volume": f(i.get('30d').get('volume')),
            "30d_volume_change_pct": f(float(i.get('7d').get('price_change_pct')) * 100) if i.get('7d').get(
                'price_change_pct') else None,
            "30d_price_change": f(i.get('30d').get('price_change')),  # not
            "30d_price_change_pct": f(float(i.get('30d').get('price_change_pct')) * 100) if i.get('30d').get(
                'price_change_pct') else None,  # not
        })

    # dashboard = sorted(dashboard, key=lambda k: k['marketcap'])[::-1][:200]

    ########################
    # Add Sparklines
    ########################

    # url = "https://api.nomics.com/v1/currencies/sparkline?key=" + os.environ.get('NOMICS_KEY')
    # url += "&ids=" + str(ids)[1:-1].replace(" ", "").replace("'", "")
    # url += "&end=" + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    # url += "&start=" + (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    #
    # sparklines_fetched = get_json(url)
    #
    # for idx, val in enumerate(dashboard):
    #     for i in sparklines_fetched:
    #         if val['currency'] == i['currency']:
    #             dashboard[idx]['sparkline_timestamps'] = i['timestamps']
    #             dashboard[idx]['sparkline_prices'] = i['prices'] , 'sparkline_timestamps': ['test'], 'sparkline_prices': ['test','test']}

    # print(url)

    print(len(dashboard))
    print(dashboard[0])

    end = time.perf_counter()
    print(f"ELAPSED TIME: {end - start:0.2f} seconds")
    return True

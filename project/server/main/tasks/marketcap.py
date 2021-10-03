import logging
import time
from datetime import datetime

import requests

from project.server.main.utils.utils import get_nomics, percentage, f


def marketcap():
    print("TASK: marketcap")
    return True


def marketcap_current():
    start = time.perf_counter()
    print("TASK: marketcap_current")
    logging.info("TASK: marketcap_current")
    nomics = get_nomics()
    print(nomics.get_url('dashboard'))
    # TODO: async await wrap
    dashboard_fetched = list(requests.get(nomics.get_url('dashboard')).json())
    print(len(dashboard_fetched))
    print(dashboard_fetched[0])

    # TODO: Cache query
    cryptocurrencies = requests.get(
        'https://raw.githubusercontent.com/crypti/cryptocurrencies/master/cryptocurrencies.json').json()

    dashboard = []

    for i in dashboard_fetched:
        close = i.get('close')
        availableSupply = i.get('availableSupply')
        if (close and availableSupply
                and f(close) > 0.0 and f(availableSupply) > 0.0
                and f(close) * f(availableSupply) > 200000000.0):
            dashboard.append({
                "currency": i.get('currency'),
                "name": cryptocurrencies.get(i.get('currency')),
                "price": f(close),
                "marketcap": f(f(close) * f(availableSupply)),
                "supply": f(availableSupply),
                "maxSupply": f(i.get('maxSupply')),
                "volumeDay": f(i.get('dayVolume')),
                "volumeWeek": f(i.get('weekVolume')),
                "volumeMonth": f(i.get('monthVolume')),
                "volumeYear": f(i.get('yearVolume')),
                "volumeDayToMonth": f((f(i.get('monthVolume')) / 30.0 / f(i.get('dayVolume'))) * 100) if i.get(
                    'monthVolume') and i.get('dayVolume') else None,
                "ath_price": f(i.get('high')),
                "ath_percentage": percentage(close, i.get('high')),
                "ath_time": datetime.strptime(i.get('highTimestamp'), "%Y-%m-%dT%H:%M:%SZ") if i.get(
                    'highTimestamp') else None,
                "percentageDay": percentage(close, i.get('dayOpen')),
                "percentageWeek": percentage(close, i.get('weekOpen')),
                "percentageMonth": percentage(close, i.get('monthOpen')),
                "percentageYear": percentage(close, i.get('yearOpen')),
            })

    dashboard = sorted(dashboard, key=lambda k: k['marketcap'])[::-1][:200]

    print(len(dashboard))
    print(dashboard[0])

    end = time.perf_counter()
    print(f"ELAPSED TIME: {end - start:0.2f} seconds")
    return True

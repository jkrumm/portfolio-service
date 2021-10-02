# project/server/main/portfolio.py
import logging
import os

from nomics import Nomics


def marketcap():
    print("TASK: marketcap")
    return True


def marketcap_current():
    print("TASK: marketcap_current")
    logging.info("TASK: marketcap_current")
    nomics = Nomics(os.environ.get('NOMICS_KEY'))
    print(nomics.Markets.get_markets(exchange='binance'))
    return True

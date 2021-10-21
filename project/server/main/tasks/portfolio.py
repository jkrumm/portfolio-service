import logging
import os
import time
from datetime import datetime
from pprint import pprint

import ccxt
import pandas as pd

from project.server.main.utils.utils import f, get_time, transform_time_ccxt


def transform_interval(n):
    if int(n) == 480:
        return '8H'
    if int(n) == 720:
        return '12H'
    if int(n) == 1:
        return '1D'


def portfolio():
    start = time.perf_counter()
    print("TASK: portfolio started")
    logging.info("TASK: portfolio started")

    binance = ccxt.binance({
        "apiKey": os.environ.get("BINANCE_KEY"),
        "secret": os.environ.get("BINANCE_SECRET"),
        'enableRateLimit': True,
    })
    binance.load_markets()
    bitmex = ccxt.bitmex({
        "apiKey": os.environ.get("BITMEX_KEY"),
        "secret": os.environ.get("BITMEX_SECRET"),
        'enableRateLimit': True,
    })
    binance.load_markets()
    bitmex.load_markets()

    def get_price(exchange, curr: str) -> float:
        if curr == 'USDT':
            return 1.0
        else:
            tick = exchange.fetchTicker(curr + '/USDT')
            mid_point = tick['bid']
            return round(float(mid_point), 2)

    def get_price_btc(exchange, curr: str) -> float:
        if curr == 'BTC':
            return 1.0
        else:
            try:
                tick = exchange.fetchTicker(curr + '/BTC')
                mid_point = tick['bid']
                return mid_point
            except:
                return None

    BTC_USD = binance.fetchTicker('BTC/USDT')['bid']
    print(BTC_USD)
    ETH_USD = binance.fetchTicker('ETH/USDT')['bid']
    print(ETH_USD)

    def get_percentage(start, end):
        return round(float(end / start * 100 - 100), 2)

    print(get_percentage(12, 13))

    def r_usd(n):
        return round(float(n), 2)

    def r_btc(n):
        return round(float(n), 6)

    print(r_usd(0.1235))
    print(r_btc(0.000216235))

    ##################################################################################################################
    # BINANCE
    ##################################################################################################################

    def get_binance_balances(exchange):
        binance_balance = exchange.fetch_balance()

        balances = []
        for symbol, value in binance_balance['total'].items():
            if value > 0.0:
                bid_price = get_price(exchange, symbol);
                if round(bid_price * value, 2) > 10.0:
                    # get the bid price from the ticker price
                    bid_price = get_price(exchange, symbol);
                    bid_price_btc = get_price_btc(exchange, symbol);
                    balance_24h = {}
                    # for b in portfolio_24h['binance_balances']:
                    #     if symbol == b['asset']:
                    #         balance_24h = b
                    balance_1w = {}
                    # for b in portfolio_1w['binance_balances']:
                    #     if symbol == b['asset']:
                    #         balance_1w = b
                    # load a list of dictionary entries for easy dataframe creation
                    datum = {}
                    datum["time"] = str(get_time())
                    datum['asset'] = symbol
                    datum['total'] = r_usd(value)
                    datum['price'] = r_usd(bid_price)
                    datum['price_btc'] = r_btc(bid_price_btc)
                    datum['balance'] = r_usd(bid_price * datum['total'])
                    datum['balance_btc'] = r_btc((bid_price * datum['total']) / BTC_USD)
                    if balance_24h and balance_1w:
                        datum['price_24h'] = get_percentage(datum['price'], balance_24h['price'])
                        datum['price_1w'] = get_percentage(datum['price'], balance_1w['price'])
                        datum['price_btc_24h'] = get_percentage(datum['price_btc'], balance_24h['price_btc'])
                        datum['price_btc_1w'] = get_percentage(datum['price_btc'], balance_1w['price_btc'])
                        datum['balance_24h'] = get_percentage(datum['balance'], balance_24h['balance'])
                        datum['balance_1w'] = get_percentage(datum['balance'], balance_1w['balance'])
                        datum['balance_btc_24h'] = get_percentage(datum['balance_btc'], balance_24h['balance_btc'])
                        datum['balance_btc_1w'] = get_percentage(datum['balance_btc'], balance_1w['balance_btc'])
                    # else:
                    # datum['price_24h'] = None
                    # datum['price_1w'] = None
                    # datum['price_btc_24h'] = None
                    # datum['price_btc_1w'] = None
                    # datum['balance_24h'] = None
                    # datum['balance_1w'] = None
                    # datum['balance_btc_24h'] = None
                    # datum['balance_btc_1w'] = None
                    balances.append(datum)

        # print(balances)
        df = pd.DataFrame(balances)
        return df

    # In[54]:

    binance_balances = get_binance_balances(binance)
    binance_balances_total = {}
    binance_balances = binance_balances.sort_values('balance', ascending=False).reset_index(drop=True)
    binance_balances_total['total'] = r_usd(binance_balances.balance.sum())
    binance_balances_total['total_btc'] = r_btc(binance_balances.balance_btc.sum())
    binance_balances_total['count'] = len(binance_balances.index)
    binance_balances_total['assets'] = binance_balances['asset'].tolist()
    print(binance_balances_total)
    pprint(binance_balances)

    ##################################################################################################################
    # BITMEX
    ##################################################################################################################

    def bitmex_to_btc(n):
        return r_btc(int(n) / 100000000)

    def bitmex_to_usd(n):
        return r_usd((bitmex_to_btc(n) * BTC_USD))

    bitmex_balances = bitmex.fetch_balance()['info'][0]
    pprint(bitmex_balances)

    b_p = bitmex.fetchPositions()
    b_p_0 = bitmex.fetchPositions()[0]
    b_p_1 = bitmex.fetchPositions()[1]
    if b_p_0['symbol'] == 'XBTUSD':
        bitmex_btc_position = b_p_0
        bitmex_eth_position = b_p_1
    else:
        bitmex_eth_position = b_p_0
        bitmex_btc_position = b_p_1

    bitmex_trades_btc = bitmex.fetch_my_trades(symbol='BTC/USD',
                                               since=bitmex.parse8601(datetime.today() - pd.DateOffset(months=3)),
                                               limit=None)
    bitmex_last_trade_btc = bitmex_trades_btc[len(bitmex_trades_btc) - 1]
    # pprint(bitmex_last_trade)
    bitmex_trades_eth = bitmex.fetch_my_trades(symbol='ETH/USD',
                                               since=bitmex.parse8601(datetime.today() - pd.DateOffset(months=3)),
                                               limit=None)
    bitmex_last_trade_eth = bitmex_trades_eth[len(bitmex_trades_eth) - 1]

    # pprint(bitmex_last_trade_eth)
    # def utc_to_berlin(n):
    #     return datetime.strptime(n, "%Y-%m-%dT%H:%M:%S.%fZ")
    #
    # print(utc_to_berlin("2021-07-07T04:00:00.002Z"))

    pm = {}

    pm['timestamp'] = str(get_time())
    pm['btc_usd'] = r_usd(BTC_USD)
    pm['eth_usd'] = r_usd(ETH_USD)

    pm['binance_total'] = r_usd(binance_balances_total['total'])
    # pm['binance_total_24h'] = get_percentage(pm['binance_total'], portfolio_24h['binance_total'])
    # pm['binance_total_1w'] = get_percentage(pm['binance_total'], portfolio_1w['binance_total'])
    pm['bitmex_total'] = r_usd(bitmex_to_usd(bitmex_balances['walletBalance']))
    # pm['bitmex_total_24h'] = get_percentage(pm['bitmex_total'], portfolio_24h['bitmex_total'])
    # pm['bitmex_total_1w'] = get_percentage(pm['bitmex_total'], portfolio_1w['bitmex_total'])
    pm['total'] = r_usd(pm['binance_total'] + pm['bitmex_total'])
    # pm['total_24h'] = get_percentage(pm['total'], portfolio_24h['total'])
    # pm['total_1w'] = get_percentage(pm['total'], portfolio_1w['total'])
    pm['binance_total_btc'] = r_btc(binance_balances_total['total_btc'])
    pm['bitmex_total_btc'] = r_btc(bitmex_to_btc(bitmex_balances['walletBalance']))
    pm['total_btc'] = r_btc(pm['binance_total_btc'] + pm['bitmex_total_btc'])
    # pm['total_btc_24h'] = get_percentage(pm['total_btc'], portfolio_24h['total_btc'])
    # pm['total_btc_1w'] = get_percentage(pm['total_btc'], portfolio_1w['total_btc'])

    pm['binance_count'] = binance_balances_total['count']
    pm['binance_assets'] = binance_balances_total['assets']
    # pm['binance_balances'] = json.loads(binance_balances.to_json(orient="records"))

    pm['bitmex_margin'] = r_usd(bitmex_to_usd(bitmex_balances['marginBalance']))
    # pm['bitmex_margin_24h'] = get_percentage(pm['bitmex_margin'], portfolio_24h['bitmex_margin'])
    # pm['bitmex_margin_1w'] = get_percentage(pm['bitmex_margin'], portfolio_1w['bitmex_margin'])
    pm['bitmex_margin_btc'] = r_btc(bitmex_to_btc(bitmex_balances['marginBalance']))
    pm['bitmex_margin_percent'] = round(float(bitmex_balances['marginBalancePcnt']), 2) * 100
    pm['bitmex_margin_leverage'] = r_usd(bitmex_balances['marginLeverage'])
    pm['bitmex_available_margin'] = r_usd(bitmex_to_usd(bitmex_balances['availableMargin']))
    pm['bitmex_available_margin_btc'] = r_btc(bitmex_to_btc(bitmex_balances['availableMargin']))
    pm['bitmex_unrealised'] = r_usd(bitmex_to_usd(bitmex_balances['unrealisedPnl']))
    # pm['bitmex_unrealised_24h'] = get_percentage(pm['bitmex_unrealised'], portfolio_24h['bitmex_unrealised'])
    # pm['bitmex_unrealised_1w'] = get_percentage(pm['bitmex_unrealised'], portfolio_1w['bitmex_unrealised'])
    pm['bitmex_unrealised_btc'] = r_btc(bitmex_to_btc(bitmex_balances['unrealisedPnl']))
    pm['bitmex_unrealised_percentage'] = round(pm['bitmex_margin'] / pm['bitmex_total'] * 100 - 100, 2)
    pm['bitmex_withdraw'] = r_usd(bitmex_to_usd(bitmex_balances['unrealisedPnl']))
    pm['bitmex_withdraw_btc'] = r_btc(bitmex_to_btc(bitmex_balances['withdrawableMargin']))

    pm['bitmex_btc_position'] = r_usd(bitmex_to_usd(bitmex_btc_position['unrealisedPnl']))
    # pm['bitmex_btc_position_24h'] = get_percentage(pm['bitmex_btc_position'], portfolio_24h['bitmex_btc_position'])
    pm['bitmex_btc_position_btc'] = r_btc(bitmex_to_btc(bitmex_btc_position['unrealisedPnl']))
    pm['bitmex_btc_position_percentage'] = round(float(bitmex_btc_position['unrealisedRoePcnt']), 2) * 100
    if (float(bitmex_btc_position['bankruptPrice']) < float(bitmex_btc_position['breakEvenPrice'])):
        pm['bitmex_btc_position_type'] = 'LONG'
    else:
        pm['bitmex_btc_position_type'] = 'SHORT'
    pm['bitmex_btc_position_leverage'] = r_usd(bitmex_btc_position['leverage'])
    pm['bitmex_btc_position_opening'] = r_usd(bitmex_last_trade_btc['price'])
    pm['bitmex_btc_position_opening_date'] = str(transform_time_ccxt(bitmex_last_trade_btc['datetime']))

    pm['bitmex_eth_position'] = r_btc(bitmex_to_usd(bitmex_eth_position['unrealisedPnl']))
    # pm['bitmex_eth_position_24h'] = get_percentage(pm['bitmex_eth_position'], portfolio_24h['bitmex_eth_position'])
    pm['bitmex_eth_position_btc'] = r_btc(bitmex_to_btc(bitmex_eth_position['unrealisedPnl']))
    pm['bitmex_eth_position_percentage'] = round(float(bitmex_eth_position['unrealisedRoePcnt']), 2) * 100
    if (float(bitmex_eth_position['bankruptPrice']) < float(bitmex_eth_position['breakEvenPrice'])):
        pm['bitmex_eth_position_type'] = 'LONG'
    else:
        pm['bitmex_eth_position_type'] = 'SHORT'
    pm['bitmex_eth_position_leverage'] = r_usd(bitmex_eth_position['leverage'])
    pm['bitmex_eth_position_opening'] = r_usd(bitmex_last_trade_eth['price'])
    pm['bitmex_eth_position_opening_date'] = str(transform_time_ccxt(bitmex_last_trade_eth['datetime']))

    pm['current'] = r_usd(pm['total'] + pm['bitmex_unrealised'])
    # pm['current_24h'] = get_percentage(pm['current'], portfolio_24h['current'])
    # pm['current_1w'] = get_percentage(pm['current'], portfolio_1w['current'])
    pm['current_btc'] = r_btc(pm['total_btc'] + pm['bitmex_unrealised_btc'])
    # pm['current_btc_24h'] = get_percentage(pm['current_btc'], portfolio_24h['current_btc'])
    # pm['current_btc_1w'] = get_percentage(pm['current_btc'], portfolio_1w['current_btc'])
    # pm['bitmex_eth_position_24h'] = get_percentage(pm['bitmex_eth_position'], portfolio_24h['bitmex_eth_position'])
    # pm['bitmex_eth_position_1w'] = get_percentage(pm['bitmex_eth_position'], portfolio_1w['bitmex_eth_position'])
    pm['current_percentage'] = round(pm['current'] / pm['total'] * 100 - 100, 2)

    # pm = {key: value for key, value in sorted(pm.items())}

    pprint(pm)

    # Todo fetch watchlist from github
    all_assets = []
    for item in binance_balances_total['assets']:
        if item not in all_assets:
            all_assets.append(item)
    print(all_assets)

    # In[70]:

    boo = []
    for asset in all_assets:
        try:
            a = binance.fetchOpenOrders(asset + '/USDT')
            if (len(a) > 0):
                for aa in a:
                    boo.append(aa)
            b = binance.fetchOpenOrders(asset + '/BTC')
            if (len(b) > 0):
                for bb in b:
                    boo.append(bb)
        except:
            pass

    binance_open_orders = []

    for o in boo:
        a = {}
        a['symbol'] = o['symbol']
        a['amount'] = r_usd(o['amount'])
        a['timestamp'] = str(get_time())
        if (o['symbol'][-1] == 'C'):
            a['price'] = r_btc(float(o['price']))
            current = r_btc(binance.fetchTicker(a['symbol'])['bid'])
            a['market'] = current
            a['market_percentage'] = get_percentage(current, a['price'])
        else:
            a['price'] = r_usd(round(float(o['price']), 2))
            current = binance.fetchTicker(a['symbol'])['bid']
            a['market'] = r_usd(current)
            a['market_percentage'] = get_percentage(current, a['price'])
        a['side'] = o['side']
        binance_open_orders.append(a)

    binance_open_orders_pd = pd.DataFrame(binance_open_orders)
    binance_open_orders_pd = binance_open_orders_pd.sort_values('market_percentage').reset_index(drop=True)
    pprint(binance_open_orders_pd.head(15))

    end = time.perf_counter()
    print("TASK: portfolio completed in " + str(f(end - start)) + "s")
    logging.info("TASK: portfolio completed in " + str(f(end - start)) + "s")

    return True

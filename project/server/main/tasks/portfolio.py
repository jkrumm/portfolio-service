import logging
import time
from datetime import datetime
from pprint import pprint

import ccxt
import pandas as pd

from project.server.config import os_get
from project.server.main.utils.utils import f, get_time, transform_time_ccxt, get_json, f_btc, percentage


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
        "apiKey": os_get("BINANCE_KEY"),
        "secret": os_get("BINANCE_SECRET"),
        'enableRateLimit': True,
    })
    binance.load_markets()
    bitmex = ccxt.bitmex({
        "apiKey": os_get("BITMEX_KEY"),
        "secret": os_get("BITMEX_SECRET"),
        'enableRateLimit': True,
    })
    binance.load_markets()
    bitmex.load_markets()

    portfolio_24h = None
    portfolio_1w = None

    # yesterday = datetime.now(pytz.timezone('Europe/Berlin')) - timedelta(hours=24)
    # portfolio_24h = list(portfolioDB.find({"timestamp": {"$gte": yesterday.replace(microsecond=0).isoformat()}}).limit(1))[0]
    # one_week = datetime.now(pytz.timezone('Europe/Berlin')) - timedelta(days=7)
    # portfolio_1w = list(portfolioDB.find({"timestamp": {"$gte": one_week.replace(microsecond=0).isoformat()}}).limit(1))[0]

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

    # def get_percentage(start, end):
    #     return round(float(end / start * 100 - 100), 2)
    #
    # print(get_percentage(12, 13))

    # def f(n):
    #     return round(float(n), 2)

    # def r_btc(n):
    #     return round(float(n), 6)
    #
    # print(f(0.1235))
    # print(f_btc(0.000216235))

    ##################################################################################################################
    # BINANCE
    ##################################################################################################################

    def get_binance_balances(exchange):
        binance_balance = exchange.fetch_balance()

        balances = []
        for symbol, value in binance_balance['total'].items():
            if value > 0.0:
                bid_price = get_price(exchange, symbol)
                if round(bid_price * value, 2) > 10.0:
                    # get the bid price from the ticker price
                    bid_price = get_price(exchange, symbol)
                    bid_price_btc = get_price_btc(exchange, symbol)
                    # balance_24h = {}
                    # for b in portfolio_24h['binance_balances']:
                    #     if symbol == b['asset']:
                    #         balance_24h = b
                    # balance_1w = {}
                    # for b in portfolio_1w['binance_balances']:
                    #     if symbol == b['asset']:
                    #         balance_1w = b
                    balance = {}
                    balance["time"] = str(get_time())
                    balance['asset'] = symbol
                    balance['total'] = f(value)
                    balance['price'] = f(bid_price)
                    balance['price_btc'] = f_btc(bid_price_btc)
                    balance['balance'] = f(bid_price * balance['total'])
                    balance['balance_btc'] = f_btc((bid_price * balance['total']) / BTC_USD)
                    # if balance_24h and balance_1w:
                    #     balance['price_24h'] = percentage(balance['price'], balance_24h['price'])
                    #     balance['price_1w'] = percentage(balance['price'], balance_1w['price'])
                    #     balance['price_btc_24h'] = percentage(balance['price_btc'], balance_24h['price_btc'])
                    #     balance['price_btc_1w'] = percentage(balance['price_btc'], balance_1w['price_btc'])
                    #     balance['balance_24h'] = percentage(balance['balance'], balance_24h['balance'])
                    #     balance['balance_1w'] = percentage(balance['balance'], balance_1w['balance'])
                    #     balance['balance_btc_24h'] = percentage(balance['balance_btc'], balance_24h['balance_btc'])
                    #     balance['balance_btc_1w'] = percentage(balance['balance_btc'], balance_1w['balance_btc'])
                    # else:
                    #     balance['price_24h'] = None
                    #     balance['price_1w'] = None
                    #     balance['price_btc_24h'] = None
                    #     balance['price_btc_1w'] = None
                    #     balance['balance_24h'] = None
                    #     balance['balance_1w'] = None
                    #     balance['balance_btc_24h'] = None
                    #     balance['balance_btc_1w'] = None
                    balances.append(balance)

        # print(balances)
        df = pd.DataFrame(balances)
        return df

    binance_balances = get_binance_balances(binance)
    binance_balances_total = {}
    binance_balances = binance_balances.sort_values('balance', ascending=False).reset_index(drop=True)
    binance_balances_total['total'] = f(binance_balances.balance.sum())
    binance_balances_total['total_btc'] = f_btc(binance_balances.balance_btc.sum())
    binance_balances_total['count'] = len(binance_balances.index)
    binance_balances_total['assets'] = binance_balances['asset'].tolist()
    print(binance_balances_total)
    pprint(binance_balances)

    ##################################################################################################################
    # BITMEX
    ##################################################################################################################

    def bitmex_to_btc(n):
        return f_btc(int(n) / 100000000)

    def bitmex_to_usd(n):
        return f((bitmex_to_btc(n) * BTC_USD))

    bitmex_balances = bitmex.fetch_balance()['info'][0]
    # pprint(bitmex_balances)

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
    # pprint(bitmex_trades_btc[0:2])
    bitmex_last_trade_btc = bitmex_trades_btc[len(bitmex_trades_btc) - 1]
    bitmex_trades_eth = bitmex.fetch_my_trades(symbol='ETH/USD',
                                               since=bitmex.parse8601(datetime.today() - pd.DateOffset(months=3)),
                                               limit=None)
    # pprint(bitmex_trades_eth[0:2])
    bitmex_last_trade_eth = bitmex_trades_eth[len(bitmex_trades_eth) - 1]

    # Map Portfolio

    pm = {}

    pm['timestamp'] = str(get_time())
    pm['btc_usd'] = f(BTC_USD)
    pm['eth_usd'] = f(ETH_USD)

    pm['binance_total'] = f(binance_balances_total['total'])
    pm['binance_total_24h'] = percentage(pm['binance_total'],
                                         portfolio_24h['binance_total']) if portfolio_24h else None
    pm['binance_total_1w'] = percentage(pm['binance_total'],
                                        portfolio_1w['binance_total']) if portfolio_1w else None
    pm['bitmex_total'] = f(bitmex_to_usd(bitmex_balances['walletBalance']))
    pm['bitmex_total_24h'] = percentage(pm['bitmex_total'],
                                        portfolio_24h['bitmex_total']) if portfolio_24h else None
    pm['bitmex_total_1w'] = percentage(pm['bitmex_total'], portfolio_1w['bitmex_total']) if portfolio_1w else None
    pm['total'] = f(pm['binance_total'] + pm['bitmex_total'])
    pm['total_24h'] = percentage(pm['total'], portfolio_24h['total']) if portfolio_24h else None
    pm['total_1w'] = percentage(pm['total'], portfolio_1w['total']) if portfolio_1w else None
    pm['binance_total_btc'] = f_btc(binance_balances_total['total_btc'])
    pm['bitmex_total_btc'] = f_btc(bitmex_to_btc(bitmex_balances['walletBalance']))
    pm['total_btc'] = f_btc(pm['binance_total_btc'] + pm['bitmex_total_btc'])
    pm['total_btc_24h'] = percentage(pm['total_btc'], portfolio_24h['total_btc']) if portfolio_24h else None
    pm['total_btc_1w'] = percentage(pm['total_btc'], portfolio_1w['total_btc']) if portfolio_1w else None

    pm['binance_count'] = binance_balances_total['count']
    # pm['binance_assets'] = binance_balances_total['assets']
    # pm['binance_balances'] = json.loads(binance_balances.to_json(orient="records"))

    pm['bitmex_margin'] = f(bitmex_to_usd(bitmex_balances['marginBalance']))
    pm['bitmex_margin_24h'] = percentage(pm['bitmex_margin'],
                                         portfolio_24h['bitmex_margin']) if portfolio_24h else None
    pm['bitmex_margin_1w'] = percentage(pm['bitmex_margin'],
                                        portfolio_1w['bitmex_margin']) if portfolio_1w else None
    pm['bitmex_margin_btc'] = f_btc(bitmex_to_btc(bitmex_balances['marginBalance']))
    pm['bitmex_margin_percent'] = round(float(bitmex_balances['marginBalancePcnt']), 2) * 100
    pm['bitmex_margin_leverage'] = f(bitmex_balances['marginLeverage'])
    pm['bitmex_available_margin'] = f(bitmex_to_usd(bitmex_balances['availableMargin']))
    pm['bitmex_available_margin_btc'] = f_btc(bitmex_to_btc(bitmex_balances['availableMargin']))
    pm['bitmex_unrealised'] = f(bitmex_to_usd(bitmex_balances['unrealisedPnl']))
    pm['bitmex_unrealised_24h'] = percentage(pm['bitmex_unrealised'],
                                             portfolio_24h['bitmex_unrealised']) if portfolio_24h else None
    pm['bitmex_unrealised_1w'] = percentage(pm['bitmex_unrealised'],
                                            portfolio_1w['bitmex_unrealised']) if portfolio_1w else None
    pm['bitmex_unrealised_btc'] = f_btc(bitmex_to_btc(bitmex_balances['unrealisedPnl']))
    pm['bitmex_unrealised_percentage'] = round(float(pm['bitmex_margin']) / float(pm['bitmex_total']) * 100 - 100, 2)
    pm['bitmex_withdraw'] = f(bitmex_to_usd(bitmex_balances['unrealisedPnl']))
    pm['bitmex_withdraw_btc'] = f_btc(bitmex_to_btc(bitmex_balances['withdrawableMargin']))

    pm['bitmex_btc_position'] = f(bitmex_to_usd(bitmex_btc_position['unrealisedPnl']))
    pm['bitmex_btc_position_24h'] = percentage(pm['bitmex_btc_position'],
                                               portfolio_24h['bitmex_btc_position']) if portfolio_24h else None
    pm['bitmex_btc_position_btc'] = f_btc(bitmex_to_btc(bitmex_btc_position['unrealisedPnl']))
    pm['bitmex_btc_position_percentage'] = round(float(bitmex_btc_position['unrealisedRoePcnt']), 2) * 100
    if (float(bitmex_btc_position['bankruptPrice']) < float(bitmex_btc_position['breakEvenPrice'])):
        pm['bitmex_btc_position_type'] = 'LONG'
    else:
        pm['bitmex_btc_position_type'] = 'SHORT'
    pm['bitmex_btc_position_leverage'] = f(bitmex_btc_position['leverage'])
    pm['bitmex_btc_position_opening'] = f(bitmex_last_trade_btc['price'])
    pm['bitmex_btc_position_opening_date'] = str(transform_time_ccxt(bitmex_last_trade_btc['datetime']))

    pm['bitmex_eth_position'] = f(bitmex_to_usd(bitmex_eth_position['unrealisedPnl']))
    pm['bitmex_eth_position_24h'] = percentage(pm['bitmex_eth_position'],
                                               portfolio_24h['bitmex_eth_position']) if portfolio_24h else None
    pm['bitmex_eth_position_btc'] = f_btc(bitmex_to_btc(bitmex_eth_position['unrealisedPnl']))
    pm['bitmex_eth_position_percentage'] = round(float(bitmex_eth_position['unrealisedRoePcnt']), 2) * 100
    if (float(bitmex_eth_position['bankruptPrice']) < float(bitmex_eth_position['breakEvenPrice'])):
        pm['bitmex_eth_position_type'] = 'LONG'
    else:
        pm['bitmex_eth_position_type'] = 'SHORT'
    pm['bitmex_eth_position_leverage'] = f(bitmex_eth_position['leverage'])
    pm['bitmex_eth_position_opening'] = f(bitmex_last_trade_eth['price'])
    pm['bitmex_eth_position_opening_date'] = str(transform_time_ccxt(bitmex_last_trade_eth['datetime']))

    pm['current'] = f(pm['total'] + pm['bitmex_unrealised'])
    pm['current_24h'] = percentage(pm['current'], portfolio_24h['current']) if portfolio_24h else None
    pm['current_1w'] = percentage(pm['current'], portfolio_1w['current']) if portfolio_1w else None
    pm['current_btc'] = f_btc(pm['total_btc'] + pm['bitmex_unrealised_btc'])
    pm['current_btc_24h'] = percentage(pm['current_btc'], portfolio_24h['current_btc']) if portfolio_24h else None
    pm['current_btc_1w'] = percentage(pm['current_btc'], portfolio_1w['current_btc']) if portfolio_1w else None
    pm['current_percentage'] = round(pm['current'] / pm['total'] * 100 - 100, 2)

    # pm = {key: value for key, value in sorted(pm.items())}

    pprint(pm)

    all_assets = get_json(os_get("WATCHLIST_GITHUB"))
    for item in binance_balances_total['assets']:
        if item not in all_assets:
            all_assets.append(item)
    print(all_assets)

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
        a['amount'] = f(o['amount'])
        a['timestamp'] = str(get_time())
        if (o['symbol'][-1] == 'C'):
            a['price'] = f_btc(float(o['price']))
            current = f_btc(binance.fetchTicker(a['symbol'])['bid'])
            a['market'] = current
            a['market_percentage'] = percentage(current, a['price'])
        else:
            a['price'] = f(round(float(o['price']), 2))
            current = binance.fetchTicker(a['symbol'])['bid']
            a['market'] = f(current)
            a['market_percentage'] = percentage(current, a['price'])
        a['side'] = o['side']
        binance_open_orders.append(a)

    binance_open_orders_pd = pd.DataFrame(binance_open_orders)
    binance_open_orders_pd = binance_open_orders_pd.sort_values('market_percentage').reset_index(drop=True)
    pprint(binance_open_orders_pd.head(15))

    end = time.perf_counter()
    print("TASK: portfolio completed in " + str(f(end - start)) + "s")
    logging.info("TASK: portfolio completed in " + str(f(end - start)) + "s")

    return True

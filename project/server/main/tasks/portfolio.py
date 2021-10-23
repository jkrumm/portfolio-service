import logging
import time
from datetime import datetime, timedelta

import ccxt
import pandas as pd

from project.server.config import os_get, db_insert, db_insert_many, db_fetch, db_aggregate
from project.server.main.utils.utils import f, get_time, transform_time_ccxt, get_json, f_btc, percentage, \
    map_portfolio


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

    portfolio_24h = db_fetch("SELECT * FROM portfolio WHERE timestamp > '%s' ORDER BY timestamp DESC LIMIT 1;" % str(
        datetime.utcnow() - timedelta(hours=24)))
    portfolio_24h = map_portfolio(portfolio_24h)[0]
    # pprint(map_portfolio(portfolio_24h))

    portfolio_1w = db_fetch("SELECT * FROM portfolio WHERE timestamp > '%s' ORDER BY timestamp DESC LIMIT 1;" % str(
        datetime.utcnow() - timedelta(days=7)))
    portfolio_1w = map_portfolio(portfolio_1w)[0]

    # pprint(list(portfolio_1w))
    # pprint(map_portfolio(portfolio_1w))

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
    ETH_USD = binance.fetchTicker('ETH/USDT')['bid']

    ##################################################################################################################
    # BINANCE
    ##################################################################################################################

    def get_binance_balances(exchange):
        binance_balance = exchange.fetch_balance()['info']['balances']
        balances = []
        for i, obj in enumerate(binance_balance):
            used = f(obj['locked'])
            used = used if (used > 0.001 and obj['asset'] != "BTC") else 0.0
            free = f(obj['free'])
            free = free if (free > 0.001 and obj['asset'] != "BTC") else 0.0
            total = f(used + free)
            if total and total > 0.0:
                bid_price = get_price(exchange, obj['asset'])
                if round(bid_price * total, 2) > 10.0:
                    bid_price_btc = get_price_btc(exchange, obj['asset'])
                    balance = {
                        'timestamp': str(get_time()),
                        'currency': obj['asset'],
                        'amount': total,
                        'price': f(bid_price),
                        'price_btc': f_btc(bid_price_btc),
                        'balance': f(bid_price * total),
                        'balance_btc': f_btc((bid_price * total) / BTC_USD),
                        'used': used,
                        'free': free
                    }
                    used_percentage = percentage(free, total) * -1 if free != 0 else 100
                    used_percentage = 100 if 100 > used_percentage > 98 else used_percentage
                    balance['used_percentage'] = used_percentage
                    balances.append(balance)
        return balances

    binance_balances = get_binance_balances(binance)
    binance_balances = sorted(binance_balances, key=lambda d: d['balance'], reverse=True)
    # pprint(binance_balances)
    db_insert_many('binance_balances', binance_balances)

    get_binance_balances_df = pd.DataFrame(binance_balances)
    binance_balances_total = {
        'total': f(get_binance_balances_df.balance.sum()),
        'total_btc': f_btc(get_binance_balances_df.balance_btc.sum()),
        'count': len(get_binance_balances_df.index),
        'assets': get_binance_balances_df['currency'].tolist()
    }

    # get_binance_balances_df = get_binance_balances_df.sort_values('balance', ascending=False).reset_index(drop=True)
    # print(binance_balances_total)

    ##################################################################################################################
    # BITMEX
    ##################################################################################################################

    def bitmex_to_btc(n):
        return f_btc(int(n) / 100000000)

    def bitmex_to_usd(n):
        return f((bitmex_to_btc(n) * BTC_USD))

    bitmex_balances = bitmex.fetch_balance()['info'][0]
    # pprint(bitmex_balances)

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
    if float(bitmex_btc_position['bankruptPrice']) < float(bitmex_btc_position['breakEvenPrice']):
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
    if float(bitmex_eth_position['bankruptPrice']) < float(bitmex_eth_position['breakEvenPrice']):
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

    # db_insert_test('portfolio_current', pm)
    db_insert('portfolio', pm)
    db_aggregate()

    # pprint(pm)

    all_assets = get_json(os_get("WATCHLIST_GITHUB"))
    for item in binance_balances_total['assets']:
        if item not in all_assets:
            all_assets.append(item)
    print(all_assets)

    boo = []
    for asset in all_assets:
        try:
            a = binance.fetchOpenOrders(asset + '/USDT')
            if len(a) > 0:
                for aa in a:
                    boo.append(aa)
            b = binance.fetchOpenOrders(asset + '/BTC')
            if len(b) > 0:
                for bb in b:
                    boo.append(bb)
        except:
            pass

    binance_open_orders = []

    # drop table if exists portfolio_current;

    for o in boo:
        a = {
            'symbol': o['symbol'],
            'amount': f(o['amount']),
            'timestamp': str(get_time())
        }
        if o['symbol'][-1] == 'C':
            a['price'] = f_btc(float(o['price']))
            current = f_btc(binance.fetchTicker(a['symbol'])['bid'])
            a['market'] = current
            a['market_percentage'] = percentage(current, a['price']) * -1
        else:
            a['price'] = f(o['price'])
            current = binance.fetchTicker(a['symbol'])['bid']
            a['market'] = f(current)
            a['market_percentage'] = percentage(current, a['price']) * -1
        a['side'] = o['side']
        binance_open_orders.append(a)

    # binance_open_orders_pd = pd.DataFrame(binance_open_orders)
    # binance_open_orders_pd = binance_open_orders_pd.sort_values('market_percentage').reset_index(drop=True)
    # pprint(binance_open_orders_pd.head(15))
    # print(list(binance_open_orders_pd))
    # binance_open_orders_dict = binance_open_orders_pd.to_dict('records')
    # pprint(binance_open_orders[0:2])

    # result = binance_open_orders_pd.to_json(orient="records")
    # parsed = json.loads(result)
    # print(json.dumps(parsed, indent=4))

    binance_open_orders = sorted(binance_open_orders, key=lambda d: d['market_percentage'])

    # db_insert_many_test("binance_orders", binance_open_orders)
    db_insert_many("binance_orders", binance_open_orders)

    end = time.perf_counter()
    print("TASK: portfolio completed in " + str(f(end - start)) + "s")
    logging.info("TASK: portfolio completed in " + str(f(end - start)) + "s")

    return True

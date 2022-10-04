import json
import time

import ccxt

import constants


def fetch_balance(exchange, coin_names):
    print("---------------------------------- fetch_balance -----------------------------------")
    balance_info = exchange.fetch_balance()
    for coin_name in coin_names:
        if coin_name in balance_info:
            print(f'free {coin_name}: {balance_info[coin_name]["free"]}')
            print(f'used {coin_name}: {balance_info[coin_name]["used"]}')
            print(f'total {coin_name}: {balance_info[coin_name]["total"]}')
            print("------------------------------")


def print_open_orders(exchange, symbol):
    print("---------------------------------- open_orders -----------------------------------")
    open_orders = exchange.fetch_open_orders(symbol)
    print(json.dumps(open_orders, indent=4))


def create_new_order(exchange, symbol, type, side, amount, price):
    print("---------------------------------- create_new_order -----------------------------------")
    try:
        order = exchange.create_order(symbol, type, side, amount, price)
        print(json.dumps(order, indent=4))
        return order
    except ccxt.InsufficientFunds as e:
        print("ERROR: Insufficient Funds")
        return None


def make_orders(exchange, coin_buy, coin_sell, symbol):
    coin_list = [coin_buy, coin_sell]
    symbol_list = [symbol]

    print(f"---------------------------------- fetch_tickers -----------------------------------")
    print(json.dumps(exchange.fetch_tickers(symbols=symbol_list), indent=4))
    fetch_balance(exchange, coin_list)

    order1_for_cancel = create_new_order(exchange, symbol, "limit", "buy", amount=0.01, price=constants.ETH_PRICE_LOW)
    order2 = create_new_order(exchange, symbol, "limit", "sell", amount=0.05, price=constants.ETH_PRICE_HIGH)
    print_open_orders(exchange, symbol)

    print(f"---------------------------------- cancel_order {order1_for_cancel['id']} --------------------------")
    exchange.cancel_order(order1_for_cancel['id'], symbol)
    print_open_orders(exchange, symbol)

    specific_order = exchange.fetch_order(order1_for_cancel['id'], symbol)
    print(json.dumps(specific_order, indent=4))

    order_no_funds = create_new_order(exchange, symbol, "limit", "sell", 101.0, constants.ETH_PRICE_HIGH)

    fetch_balance(exchange, coin_list)

    print(f"---------------------------------- cancel_all_orders -----------------------------------")
    exchange.cancel_all_orders(symbol)
    print_open_orders(exchange, symbol)
    fetch_balance(exchange, coin_list)


def test_rate_limit(exchange, symbol):
    i = 0
    start_time = time.time()
    exchange.rateLimit = 300
    while i < 1000:
        try:
            ticker = exchange.fetch_ticker(symbol)
            end_time = time.time()
            print(i, end_time - start_time)
            start_time = end_time
            i += 1
        except Exception as e:
            print('Got Exception :| ', e)


async def test_orders(exchange):
    try:
        print(exchange.id)
        markets = exchange.load_markets()
        coin_buy = "ETH"
        coin_sell = "USDT"
        symbol = coin_buy + "/" + coin_sell

        # print(json.dumps(markets[symbol], indent=4))

        make_orders(exchange, coin_buy, coin_sell, symbol)
        test_rate_limit(exchange, symbol)

        return "success"

    except ccxt.BaseError as e:
        print(type(e).__name__, str(e), str(e.args))
        raise e

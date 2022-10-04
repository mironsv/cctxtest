import json
import time

import ccxt

import constants


async def fetch_balance(exchange, coin_names):
    print(f"-{exchange.id}-------------------------------- fetch_balance -----------------------------------")
    balance_info = await exchange.fetch_balance()
    for coin_name in coin_names:
        if coin_name in balance_info:
            print(f'free {coin_name}: {balance_info[coin_name]["free"]}')
            print(f'used {coin_name}: {balance_info[coin_name]["used"]}')
            print(f'total {coin_name}: {balance_info[coin_name]["total"]}')
            print("------------------------------")


async def print_open_orders(exchange, symbol):
    print(f"-{exchange.id}-------------------------------- open_orders -----------------------------------")
    open_orders = await exchange.fetch_open_orders(symbol)
    print(json.dumps(open_orders, indent=4))


async def create_new_order(exchange, symbol, type, side, amount, price):
    print(f"-{exchange.id}-------------------------------- create_new_order -----------------------------------")
    try:
        order = await exchange.create_order(symbol, type, side, amount, price)
        print(json.dumps(order, indent=4))
        return order
    except ccxt.InsufficientFunds as e:
        print("ERROR: Insufficient Funds")
        return None


async def make_orders(exchange, coin_buy, coin_sell, symbol):
    coin_list = [coin_buy, coin_sell]
    symbol_list = [symbol]

    print(f"-{exchange.id}--------------------------------- fetch_tickers -----------------------------------")
    print(json.dumps(await exchange.fetch_tickers(symbols=symbol_list), indent=4))
    await fetch_balance(exchange, coin_list)

    order1 = await create_new_order(exchange, symbol, "limit", "buy", amount=0.01, price=constants.ETH_PRICE_LOW)
    order2 = await create_new_order(exchange, symbol, "limit", "sell", amount=0.05, price=constants.ETH_PRICE_HIGH)
    await print_open_orders(exchange, symbol)

    print(f"-{exchange.id}--------------------------------- cancel_order {order1['id']} ------------------")
    await exchange.cancel_order(order1['id'], symbol)
    await print_open_orders(exchange, symbol)

    order1_fetched = await exchange.fetch_order(order1['id'], symbol)
    print(json.dumps(order1_fetched, indent=4))

    order_no_funds = await create_new_order(exchange, symbol, "limit", "sell", 101.0, constants.ETH_PRICE_HIGH)

    await fetch_balance(exchange, coin_list)

    print(f"-{exchange.id}------------------------------ cancel_all_orders -----------------------------------")
    await exchange.cancel_all_orders(symbol)
    await print_open_orders(exchange, symbol)
    await fetch_balance(exchange, coin_list)


async def test_rate_limit(exchange, symbol):
    i = 0
    start_time = time.time()
    exchange.rateLimit = 300
    while i < 10:
        try:
            ticker = await exchange.fetch_ticker(symbol)
            end_time = time.time()
            print(i, end_time - start_time)
            start_time = end_time
            i += 1
        except Exception as e:
            print('Got Exception :| ', e)


async def test_orders(exchange):
    try:
        print(exchange.id)
        markets = await exchange.load_markets()
        coin_buy = "ETH"
        coin_sell = "USDT"
        symbol = coin_buy + "/" + coin_sell

        # print(json.dumps(markets[symbol], indent=4))

        await make_orders(exchange, coin_buy, coin_sell, symbol)
        await test_rate_limit(exchange, symbol)

        return "success"

    except ccxt.BaseError as e:
        print(type(e).__name__, str(e), str(e.args))
        raise e

from pprint import pprint


async def place_delayed_order(exchange, symbol, amount, price):
    try:
        await exchange.sleep(5000)  # wait a bit
        order = await exchange.create_limit_buy_order(symbol, amount, price)
        print(exchange.iso8601(exchange.milliseconds()), 'place_delayed_order')
        pprint(order)
        print('---------------------------------------------------------------')
    except Exception as e:
        # break
        print(e)


async def watch_orders_loop(exchange, symbol):
    while True:
        try:
            orders = await exchange.watch_orders(symbol)
            print(exchange.iso8601(exchange.milliseconds()), 'watch_orders_loop', len(orders), ' last orders cached')
            print('---------------------------------------------------------------')
        except Exception as e:
            # break
            print(e)


async def watch_balance_loop(exchange):
    while True:
        try:
            balance = await exchange.watch_balance()
            print(exchange.iso8601(exchange.milliseconds()), 'watch_balance_loop')
            pprint(balance)
            print('---------------------------------------------------------------')
        except Exception as e:
            # break
            print(e)


async def symbol_loop(exchange, symbol):
    print('Starting the', exchange.id, 'symbol loop with', symbol)
    while True:
        try:
            orderbook = await exchange.watch_order_book(symbol)
            now = exchange.milliseconds()
            print(exchange.iso8601(now), exchange.id, symbol, orderbook['asks'][0], orderbook['bids'][0])
        except Exception as e:
            print(str(e))
            # raise e  # uncomment to break all loops in case of an error in any one of them
            break  # you can break just this one loop if it fails

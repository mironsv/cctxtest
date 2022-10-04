from asyncio import gather, run

import ccxt
import ccxt.pro as ccxtpro

import constants
import exchange_interface_rest_api
import exchange_interface_websocket


def run_websocket(exchange_test, symbol):
    amount = 0.03
    price = constants.ETH_PRICE_LOW
    return [exchange_interface_websocket.watch_orders_loop(exchange_test, symbol),
            exchange_interface_websocket.watch_balance_loop(exchange_test),
            exchange_interface_websocket.place_delayed_order(exchange_test, symbol, amount, price)]


async def main():
    print('CCXT Version:', ccxt.__version__)
    rate_limit_value = 1000
    exchange_binance = ccxtpro.binance({
        'apiKey': '',
        'secret': '',
        'rateLimit': rate_limit_value  # (ms)
    })
    exchange_binance.set_sandbox_mode(True)

    exchange_kucoin = ccxtpro.kucoin({
        'apiKey': '',
        'secret': '',
        'password': '',
        'rateLimit': rate_limit_value  # (ms)
    })
    exchange_kucoin.set_sandbox_mode(True)

    coin_buy = "ETH"
    coin_sell = "USDT"
    symbol = coin_buy + "/" + coin_sell
    exchange_test = exchange_kucoin

    # symbols = ['KDA/USDT', 'KDA/BTC', 'BTC/USDT']
    # loops = [exchange_interface_websocket.symbol_loop(exchange_test, symbol) for symbol in symbols]
    # await gather(*loops)

    loops_websocket = run_websocket(exchange_test, symbol)

    # more exchanges could be added in the list (parallel execution)
    loops_rest_api = [exchange_interface_rest_api.test_orders(exchange_test, coin_buy, coin_sell)]

    await gather(*loops_websocket, *loops_rest_api)

    await exchange_test.close()
    await exchange_binance.close()
    await exchange_kucoin.close()


run(main())

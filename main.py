import asyncio

import ccxt

import exchange_interface

if __name__ == '__main__':
    rate_limit_value = 1000
    exchange_binance = ccxt.binance({
        'apiKey': '',
        'secret': '',
        'rateLimit': rate_limit_value  # (ms)
    })
    exchange_binance.set_sandbox_mode(True)

    exchange_kucoin = ccxt.kucoin({
        'apiKey': '',
        'secret': '',
        'password': '',
        'rateLimit': rate_limit_value  # (ms)
    })
    exchange_kucoin.set_sandbox_mode(True)

    status = asyncio.run(exchange_interface.test_orders(exchange_binance))
    status = asyncio.run(exchange_interface.test_orders(exchange_kucoin))

    exchange_binance.session.close()
    exchange_kucoin.session.close()

import asyncio

import ccxt

import exchange_interface

if __name__ == '__main__':
    exchange_binance = ccxt.binance({
        'apiKey': '',
        'secret': ''
    })
    exchange_binance.set_sandbox_mode(True)

    exchange_kucoin = ccxt.kucoin({
        'apiKey': '',
        'secret': '',
        'password': ''
    })
    exchange_kucoin.set_sandbox_mode(True)

    # status = asyncio.run(exchange_interface.execute(exchange_binance))
    status = asyncio.run(exchange_interface.execute(exchange_kucoin))

    exchange_binance.session.close()
    exchange_kucoin.session.close()

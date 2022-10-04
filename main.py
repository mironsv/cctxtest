from asyncio import gather, run

import ccxt
import ccxt.pro as ccxtpro

import exchange_interface


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

    # status = asyncio.run(exchange_interface.test_orders(exchange_binance))
    # status = asyncio.run(exchange_interface.test_orders(exchange_kucoin))

    loops = [exchange_interface.test_orders(exchange_binance), exchange_interface.test_orders(exchange_kucoin)]
    await gather(*loops)

    await exchange_binance.close()
    await exchange_kucoin.close()


run(main())

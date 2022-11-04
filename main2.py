import asyncio

import ccxt.pro as ccxtpro


async def main():
    exchange_kucoin = ccxtpro.kucoin()
    await exchange_kucoin.load_markets()
    # exchange.verbose = True  # uncomment for debugging purposes
    market = exchange_kucoin.market('BTC/USDT')
    print(market)
    await exchange_kucoin.close()


if __name__ == '__main__':
    asyncio.run(main())

# -*- coding: utf-8 -*-

# import krakenex
# from pykrakenapi import KrakenAPI
# api = krakenex.API()
# k = KrakenAPI(api)
# ohlc, last = k.get_ohlc_data("ETHEUR")
# print(ohlc)

import crypy.euc
ccxt = crypy.euc.ccxt

from crypy.chart import plot

import configparser
config = configparser.ConfigParser()
config.optionxform = str
config.read('crypy.ini')

kraken = ccxt.kraken(dict(config.items('kraken.com')))


print(kraken.fetch_balance())
print(kraken.fetch_trading_fees())
print(kraken.fetch_ticker('BTC/USD'))


# each ohlcv candle is a list of [ timestamp, open, high, low, close, volume ]
index = 4  # use close price from each ohlcv candle


def print_chart(exchange, symbol, timeframe):

    print("\n" + exchange.name + ' ' + symbol + ' ' + timeframe + ' chart:')

    # get a list of ohlcv candles
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe)

    # get the ohlCv (closing price, index == 4)
    series = [x[index] for x in ohlcv]

    # print the chart
    print("\n" + plot(series[-120:], {'height': 20}))  # print the chart

    last = ohlcv[len(ohlcv) - 1][index]  # last closing price
    return last


last = print_chart(kraken, 'BTC/USD', '1h')
print("\n" + kraken.name + " ₿ = $" + str(last) + "\n")  # print last closing price



# -*- coding: utf-8 -*-

import os
import sys
import time

import crypy.euc
ccxt = crypy.euc.ccxt

import configparser
config = configparser.ConfigParser()
config.optionxform = str
config.read('crypy.ini')
bitmex = ccxt.bitmex(dict(config.items('testnet.bitmex.com')))

print(bitmex.fetch_balance())


# params:
symbol = 'BTC/USD'
timeframe = '1m'
limit = 100
params = {'partial': False}  # ←--------  no reversal

while True:

    # pay attention to since with respect to limit if you're doing it in a loop
    since = bitmex.milliseconds() - limit * 60 * 1000

    candles = bitmex.fetch_ohlcv(symbol, timeframe, since, limit, params)
    num_candles = len(candles)
    print('{}: O: {} H: {} L:{} C:{}'.format(
        bitmex.iso8601(candles[num_candles - 1][0]),
        candles[num_candles - 1][1],
        candles[num_candles - 1][2],
        candles[num_candles - 1][3],
        candles[num_candles - 1][4]))
    # * 5 to make distinct delay and to avoid too much load
    # / 1000 to convert milliseconds to fractional seconds
    time.sleep(bitmex.rateLimit * 5 / 1000)

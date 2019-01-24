# import krakenex
# from pykrakenapi import KrakenAPI
# api = krakenex.API()
# k = KrakenAPI(api)
# ohlc, last = k.get_ohlc_data("ETHEUR")
# print(ohlc)

import crypy.euc
ccxt = crypy.euc.ccxt

import configparser
config = configparser.ConfigParser()
config.optionxform = str
config.read('crypy.ini')

kraken = ccxt.kraken(dict(config.items('kraken.com')))


print(kraken.fetch_balance())
print(kraken.fetch_trading_fees())
print(kraken.fetch_ticker('BTC/USD'))

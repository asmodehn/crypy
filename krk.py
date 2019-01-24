# import krakenex
# from pykrakenapi import KrakenAPI
# api = krakenex.API()
# k = KrakenAPI(api)
# ohlc, last = k.get_ohlc_data("ETHEUR")
# print(ohlc)

import ccxt
import configparser
config = configparser.ConfigParser()
config.read('crypy.ini')
kraken = ccxt.kraken(config['kraken'])

print(kraken.fetch_balance())
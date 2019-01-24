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


kraken = ccxt.kraken({ 'apiKey': config['kraken']['apiKey'], 'secret': config['kraken']['secret']}) #, 'verbose': True })


print(kraken.fetch_balance())
print(kraken.fetch_trading_fees())
print(kraken.fetch_ticker('BTC/USD'))

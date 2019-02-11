#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 15:51:55 2019

@author: alexv
"""

import cryptocompare.cryptocompare as crcomp # https://github.com/lagerfeuer/cryptocompare


#print( crcomp.get_coin_list(format=True) )
#print( crcomp.get_exchanges() )

#print( crcomp.get_price())
#print( crcomp.get_price(['BTC', 'ETH'], ['USD', 'EUR'], 'Kraken' ) )
#print( crcomp.get_avg('XBTUSD', 'USD', 'Bitmex') )

#print( crcomp.get_historical_price_ts() )
#print( crcomp.get_historical_price_day() )
#print( crcomp.get_historical_price_hour() )
#print( crcomp.get_historical_price_minute() )



################################################################################################
#	name:	timeseries_OHLC_with_SMA.py
#	desc:	creates OHLC graph with overlay of simple moving averages
#	date:	2018-06-15
#	Author:	conquistadorjd
#   https://www.techtrekking.com/how-to-plot-simple-and-candlestick-chart-using-python-pandas-matplotlib/
################################################################################################
import time

import pandas
# import pandas_datareader as datareader
import matplotlib.pyplot as plt
import datetime
from mpl_finance.mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates

import json

import TechnicalIndicators.indicator.indicators as ti


##look into https://plot.ly/python/candlestick-charts/
#import plotly as py
#import plotly.graph_objs as go
#
#
#df = pandas.read_json( json.dumps( crcomp.get_historical_price_minute('ETH','USD','Kraken')['Data'] ) )
## http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_json.html
#
##df = type(crcomp.get_historical_price_minute())
##print(json.loads(str(crcomp.get_historical_price_minute())))
##df = pandas.read_json()
##print(df)
##time: 1548006900
##close: 2772.27
##high: 2772.45
##low: 2771.81
##open: 2772.45
##volumefrom: 0.5832
##volumeto: 1610.12
#
#
## Converting date to pandas datetime format
#df['time'] = pandas.to_datetime(df['time'], unit='s')
#df['time'] = df['time'].apply(mdates.date2num)
#print(df)
#
## Creating required data in new DataFrame OHLC
#ohlc = df[['time', 'open', 'high', 'low', 'close']].copy()
#print(ohlc)
#
## Formatting for HA 'date', 'open', 'high', 'low', 'close', 'volume'
#df['volume'] = df['volumeto'] - df['volumefrom']
#ha = ti.HA(df, ['open', 'high', 'low', 'close'])
#ha = ha.drop(['open', 'high', 'low', 'close', 'volumefrom', 'volumeto'], axis=1)
#ha = ha.rename(index=str, columns={"HA_close": "close", "HA_open": "open", "HA_high": "high", "HA_low": "low"})
##print(ha)
#
## In case we want to check for shorter timespan
## ohlc = ohlc.tail(60)
#
#
#f1, ax = plt.subplots(figsize = (10,5))
#
## plot the candlesticks
#candlestick_ohlc(ax, ohlc.values, width=.6, colorup='green', colordown='red')
#ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
#
### Creating SMA columns
#ohlc['SMA50'] = ohlc["close"].rolling(50).mean()
#ohlc['SMA100'] = ohlc["close"].rolling(100).mean()
#
##Plotting SMA columns
#ax.plot(ohlc['time'], ohlc['SMA50'], color = 'green', label = 'SMA50')
#ax.plot(ohlc['time'], ohlc['SMA100'], color = 'blue', label = 'SMA100')
#
## Saving image
## plt.savefig('OHLC with SMA HDFC.png')
## Save file
#ohlc.to_csv('ohlc.csv')
##plt.show()
#
#
## plotly TEST
#trace = go.Candlestick(x=ha['time'],
#                open=ha['open'],
#                high=ha['high'],
#                low=ha['low'],
#                close=ha['close'])
#data = [trace]
#py.offline.plot(data, filename='simple_candlestick.html')


def getAllHisto(symbol, currency, exchange, timeframe):
    #if type(timeframe) is str and timeframe in ['minute', 'hour', 'day'] and type(symbol) is str and type(cyrrency) is str and type(exchange) is str :
        i = 0, limit = 2000, toTs = 0
        allDfs = dict()
        while(i<5):
            allDfs[i] = pandas.read_json( json.dumps( crcomp.get_historical_price_minute(symbol, currency, exchange, 1, True, 2000)['Data'] ) ) #toTs TODO
            #print(allDfs[i])
            
            i = i+1
        
        #print(allDfs) 
        df = pandas.concat(allDfs)
        #print(df)

        df['time'] = pandas.to_datetime(df['time'], unit='s')
        df['time'] = df['time'].apply(mdates.date2num)
        ohlcv = df[['time', 'open', 'high', 'low', 'close']].copy()
        ohlcv['volume'] = df['volumeto'] - df['volumefrom']
        ohlcv.to_csv('OHLCV_'+ symbol + currency + '_' + exchange + '_' + timeframe +'.csv')
        print ('Done')
        
    #else :
    #    print('invalid param(s) specified')
    
    
getAllHisto('ETH', 'USD', 'kraken', 'minute')
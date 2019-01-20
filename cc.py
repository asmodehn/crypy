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


"""
import matplotlib.pyplot as plt   # https://github.com/matplotlib/matplotlib
import numpy as np

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))

# generate some random test data
all_data = [np.random.normal(0, std, 100) for std in range(6, 10)]

# plot violin plot
axes[0].violinplot(all_data,
                   showmeans=False,
                   showmedians=True)
axes[0].set_title('violin plot')

# plot box plot
axes[1].boxplot(all_data)
axes[1].set_title('box plot')

# adding horizontal grid lines
for ax in axes:
    ax.yaxis.grid(True)
    ax.set_xticks([y+1 for y in range(len(all_data))])
    ax.set_xlabel('xlabel')
    ax.set_ylabel('ylabel')

# add x-tick labels
plt.setp(axes, xticks=[y+1 for y in range(len(all_data))],
         xticklabels=['x1', 'x2', 'x3', 'x4'])
plt.show()
"""


################################################################################################
#	name:	timeseries_OHLC_with_SMA.py
#	desc:	creates OHLC graph with overlay of simple moving averages
#	date:	2018-06-15
#	Author:	conquistadorjd
#   https://www.techtrekking.com/how-to-plot-simple-and-candlestick-chart-using-python-pandas-matplotlib/
################################################################################################
import pandas
# import pandas_datareader as datareader
import matplotlib.pyplot as plt
import datetime
from mpl_finance.mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates

import json

import TechnicalIndicators.indicator.indicators as ti

#look into https://plot.ly/python/candlestick-charts/

#df = pandas.read_json(crcomp.get_historical_price_minute())
#df.locations = pandas.DataFrame(df.locations.values.tolist())['Data']
#df = df.groupby(['date','name','number'])['locations'].apply(','.join).reset_index()

#print( json.loads( str( crcomp.get_historical_price_minute() ) ) )
df = pandas.read_json( json.dumps( crcomp.get_historical_price_day('BTC','USD','Kraken')['Data'] ) )
# http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_json.html

#df = type(crcomp.get_historical_price_minute())
#print(json.loads(str(crcomp.get_historical_price_minute())))
#df = pandas.read_json()
#print(df)
#time: 1548006900
#close: 2772.27
#high: 2772.45
#low: 2771.81
#open: 2772.45
#volumefrom: 0.5832
#volumeto: 1610.12

#df = pandas.read_csv('15-06-2016-TO-14-06-2018HDFCBANKALLN.csv')

# ensuring only equity series is considered
#df = df.loc[df['Series'] == 'EQ']

# Converting date to pandas datetime format
#df['Date'] = pandas.to_datetime(df['Date'])
#df["Date"] = df["Date"].apply(mdates.date2num)
df['time'] = pandas.to_datetime(df['time'], unit='s')
df['time'] = df['time'].apply(mdates.date2num)
print(df)

# Creating required data in new DataFrame OHLC
ohlc = df[['time', 'open', 'high', 'low', 'close']].copy()
print(ohlc)

# Formatting for indicator 'date', 'open', 'high', 'low', 'close', 'volume'
#ha = df[['open', 'high', 'low', 'close']].copy()
#ha['date'] = df['time']
df['volume'] = df['volumeto'] - df['volumefrom']
ha = ti.HA(df, ['open', 'high', 'low', 'close'])
ha = ha.drop(['open', 'high', 'low', 'close', 'volumefrom', 'volumeto'], axis=1)
ha = ha.rename(index=str, columns={"HA_close": "close", "HA_open": "open", "HA_high": "high", "HA_low": "low"})
print(ha)

# In case you want to check for shorter timespan
# ohlc =ohlc.tail(60)

"""
df = pandas.read_csv('15-06-2016-TO-14-06-2018HDFCBANKALLN.csv')

df = df.loc[df['Series'] == 'EQ']

df['Date'] = pandas.to_datetime(df['Date'])
df["Date"] = df["Date"].apply(mdates.date2num)


ohlc= df[['Date', 'Open Price', 'High Price', 'Low Price','Close Price']].copy()
print(ohlc)
"""




f1, ax = plt.subplots(figsize = (10,5))

# plot the candlesticks
candlestick_ohlc(ax, ohlc.values, width=.6, colorup='green', colordown='red')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

## Creating SMA columns
#ohlc['SMA5'] = ohlc["close"].rolling(5).mean()
#ohlc['SMA10'] = ohlc["close"].rolling(10).mean()
#ohlc['SMA20'] = ohlc["close"].rolling(20).mean()
ohlc['SMA50'] = ohlc["close"].rolling(50).mean()
ohlc['SMA100'] = ohlc["close"].rolling(100).mean()
#ohlc['SMA200'] = ohlc["close"].rolling(200).mean()

#Plotting SMA columns
# ax.plot(ohlc['time'], ohlc['SMA5'], color = 'blue', label = 'SMA5')
#ax.plot(ohlc['time'], ohlc['SMA10'], color = 'orange', label = 'SMA10')
#ax.plot(ohlc['time'], ohlc['SMA20'], color = 'red', label = 'SMA20')
ax.plot(ohlc['time'], ohlc['SMA50'], color = 'green', label = 'SMA50')
ax.plot(ohlc['time'], ohlc['SMA100'], color = 'blue', label = 'SMA100')
#ax.plot(ohlc['time'], ohlc['SMA200'], color = 'blue', label = 'SMA200')

# Saving image
#plt.savefig('OHLC with SMA HDFC.png')

# In case you dont want to save image but just displya it

# ohlc.to_csv('ohlc.csv')
plt.show()


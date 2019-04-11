#!/usr/bin/env python
# -*- coding: utf-8 -*-

defEXCHANGE = "testnet.bitmex"
defPAIR = "BTCUSD"
exchange_data = {
    "kraken": { 'confSection': "kraken", 'ccxtName': "kraken"},
    "bitmex": { 'confSection': "bitmex", 'ccxtName': "bitmex"},
    "testnet.bitmex": { 'confSection': "testnet.bitmex", 'ccxtName': "bitmex", 'test': True }
}
ticker2symbol = {
    'ETHUSD': 'ETH/USD',
    'XBTUSD': 'XBT/USD',
    'ETHEUR': 'ETH/EUR',
    'BTCUSD': 'BTC/USD',
    'BTCEUR': 'BTC/EUR',
    'ETHBTC': 'ETH/BTC'
    #TBC
} #todo handle multiple symbol for pair if needed #todo this is exchange specific
symbol2id = {
    'BTC/USD': 'XBTUSD',
    'XBT/USD': 'XBTUSD'
    #TBC
} #todo this is exchange specific

tf2second = {
    '1m': 60, '3m': 180, '15m': 900, '30m': 1800, '1h': 3600, '2H': 7200, '4H': 14400, '6H': 21600, '12H': 43200, '1D': 86400, '3D': 259200, '1W': 604800, '1M': 2592000
    } #warning 1M == 30days

#nb: will be gotten from the bot in the end
#nb2 link to exchange first
wholeData = {
    'ETHUSD': {
        'data': {
            'value': 105,
            'indicators': { 'rsi': 52.01, 'ew': 'five of five of 1 up' },
            #### TIMEFRAME for data ??  ####
            'orderbook': []
        },
        'positions': [{
                'side': 'short',
                'amount': 60,
                'price': 92.19,
                'leverage': 5,
                'p/l %': 10,
                'p/l': 800
            }],
        'orders': [{
                'id': '12312155156156',
                'side': 'short',
                'type': 'limit',
                'amount': 30,
                'price': 92,
                'leverage': 5,
                'expiracy': '1 hour'
            },
            {
                'id': '2212155156156',
                'side': 'short',
                'type': 'limit',
                'amount': 35,
                'price': 96,
                'leverage': 5
            }],
        'trades': [{
                'id': '1212155156156',
                'side': 'short',
                'type': 'limit',
                'amount': 35,
                'price': 96,
                'leverage': 5,
                'datetime': '2018/05/02 15:32:12'
            },
            {
                'id': '1212155156157',
                'side': 'long',
                'type': 'limit',
                'amount': 35,
                'price': 95,
                'leverage': 5,
                'datetime': '2018/09/02 15:32:12'
            }]
    },
    'ETHEUR': {
        'data': {
            'value': 100,
            'indicators': { 'rsi': 49.01, 'ew': 'five of five of 1 up' },
            #### TIMEFRAME for data ??  ####
            'orderbook': []
        },
        'positions': [{
                'side': 'short',
                'amount': 60,
                'price': 94.19,
                'leverage': 5,
                'p/l %': 10,
                'p/l': 800
            }],
        'orders': [{
                'id': '1212155176156',
                'side': 'short',
                'type': 'limit',
                'amount': 30,
                'price': 86,
                'leverage': 5,
                'expiracy': '1 hour'
            },
            {
                'id': '1214155156156',
                'side': 'short',
                'type': 'limit',
                'amount': 34,
                'price': 76,
                'leverage': 10
            }],
        'trades': [{
                'id': '1219155156156',
                'side': 'short',
                'type': 'limit',
                'amount': 35,
                'price': 53,
                'leverage': 5,
                'datetime': '2018/05/02 16:32:12'
            },
            {
                'id': '1422155156156',
                'side': 'long',
                'type': 'limit',
                'amount': 35,
                'price': 89,
                'leverage': 5,
                'datetime': '2018/09/02 15:34:12'
            }]
    }
}

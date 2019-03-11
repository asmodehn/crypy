#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import global_vars as gv
except (ImportError, ValueError, ModuleNotFoundError):
    import crypy.desk.global_vars as gv

from .utils import Utils

try:
    from ..euc import ccxt
    from .. import config
except (ImportError, ValueError, ModuleNotFoundError):
    from crypy.euc import ccxt
    from crypy import config

class Desk(object):
    def __init__(self, conf: config.Config = None, exchange=gv.defEXCHANGE):
        self.config = conf if conf is not None else config.Config()
        self.exchangeName = (exchange or gv.defEXCHANGE)
        exgData = gv.exchange_data[self.exchangeName] #TODO check existance
        self.exchange = getattr(ccxt, exgData['ccxtName'])(self.config.sections[exgData['confSection']].asdict()) #TODO check exchange id existing in CCXT
        if 'test' in exgData and exgData['test']:
            self.exchange.urls['api'] = self.exchange.urls['test']  #switch the base URL to test net url
        
        self.exchange.loadMarkets(True) #preload market data. NB: forced reloading w reload=True param, do we want to always do that ? #https://github.com/ccxt/ccxt/wiki/Manual#loading-markets

    def do_getExchangeInfo(self):
        filename = 'exg_' + gv.exchange_data[self.exchangeName]['confSection'] + '.txt'
        file = open( filename, 'w')
        print ("### HAS ###", file = file)
        print (str(self.exchange.has).replace(', ', ', \r\n'), file = file)
        print ("\r\n### SYMBOLS ###", file = file)
        print (str(self.exchange.symbols).replace(', ', ', \r\n'), file = file)
        print ("\r\n### FULL EXCHANGE DATA ###", file = file)
        print (dir(self.exchange), file = file)  #List exchange available methods
        file.close()
        #Exchange properties https://github.com/ccxt/ccxt/wiki/Manual#exchange-properties
        return 'Exchange data printed to ' + filename

    def do_list(self, arg):
        arg = "data" if arg is '' else arg
        what = {
            'data': 'data',
            'orders': 'orders',
            'positions': 'positions',
            'trades': 'trades'
        }.get(arg, "data")
        for pair in gv.wholeData:
            print(f"{pair} {what}: {str(gv.wholeData[pair][what])}")
    
    def _ccxtFetchXXX(self, ccxtMethod, **kwargs):
        """ccxt fetchXXX wrapper"""
        exg = self.exchange
        if not ccxtMethod in exg.has or not exg.has[ccxtMethod]:
            return f'{ccxtMethod} not available for this exchange'

        try:
            #Do we need to (re)load market everytime to get accurate data?
            ret = getattr(exg, ccxtMethod)(**kwargs)
            return ret

        except ccxt.BaseError as error:
            return error.args[0]

    def do_fetchOHLCV(self, symbol, timeframe, since, limit, customParams = {}):
        #Get data
        tohlcv = self._ccxtFetchXXX('fetchOHLCV', symbol = symbol, timeframe = timeframe, limit = limit, params = customParams) #, since = (exg.seconds()-since)
        #TODO handle exception in return

        #format data into a list
        # initialize a list to store the parsed ohlc data
        tohlcvlist = []

        for period in tohlcv:
            # Initialize an OrderedDict to garantee the column order
            tohlcvdict = dict()
            tohlcvdict["CloseTime"] = Utils.formatTS(period[0])
            tohlcvdict["Open"] = period[1]
            tohlcvdict["High"] = period[2]
            tohlcvdict["Low"] = period[3]
            tohlcvdict["Close"] = period[4]
            tohlcvdict["Volume"] = period[5] #volume in base currency
            tohlcvlist.append(tohlcvdict)

        if not tohlcvlist:
            return
        # Reverse trade list to have the most recent interval at the top
        tohlcvlist = tohlcvlist[::-1]

        return tohlcvlist

    def do_fetchBalance(self, customParams):
        return self._ccxtFetchXXX('fetchBalance', params = customParams)
    def do_fetchTotalBalance(self, customParams):
        return self._ccxtFetchXXX('fetchTotalBalance', params = customParams)
    def do_fetchFreeBalance(self, customParams):
        return self._ccxtFetchXXX('fetchFreeBalance', params = customParams)
    def do_fetchUsedBalance(self, customParams):
        return self._ccxtFetchXXX('fetchUsedBalance', params = customParams)
    def do_fetchPartialBalance(self, customParams):
        return self._ccxtFetchXXX('fetchPartialBalance', params = customParams)

    def do_fetchLedger(self, code, since, limit, customParams):
        return self._ccxtFetchXXX('fetchLedger', code = code, since = since, limit = limit, params = customParams)

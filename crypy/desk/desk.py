#!/usr/bin/env python
# coding: utf-8
import typing

import json


try:
    from desk import capital
    import global_vars as gv
except (ImportError, ValueError, ModuleNotFoundError):
    import crypy.desk.global_vars as gv
    from crypy.desk import capital

from .utils import formatTS


try:
    from ..euc import ccxt
    from .. import config
    from .model.balance import BalanceAll
    from .model.symbol import Symbol, SymbolError
    from .market import Market
except (ImportError, ValueError, ModuleNotFoundError):
    from crypy.euc import ccxt
    from crypy import config
    from crypy.desk.model.balance import BalanceAll
    from crypy.desk.model.symbol import Symbol, SymbolError
    from crypy.desk.market import Market, MarketError


class Desk:

    @property
    def markets(self) -> typing.Dict[Symbol, Market]:
        if self.exchange.markets is None:
            self.exchange.load_markets()

        # symbol filter
        filtered_syms = dict()
        for s, m in self.exchange.markets.items():
            try:
                filtered_syms[Symbol.from_str(s)] = m
            except SymbolError as se:
                pass
        markets_dict = {s: Market.from_dict(m) for s, m in filtered_syms.items()}
        return markets_dict

    @property
    def balance(self) -> BalanceAll:
        # TODO : timer to do the call only after some timeout...
        bal_raw = self._ccxtMethod('fetchBalance')
        bal = BalanceAll(**{e: bal_raw.get(e) for e in ['free', 'used', 'total']})
        return bal

    def __init__(self, conf: config.ExchangeSection = None):
        self.exchangeName = conf.name

        # Using the impl_hook from settings.ini
        self.exchange = conf.exec_hook(ccxt=ccxt)

        # Requesting Key from initialization
        # TODO : anonymous by default, on demand auth
        self.exchange.apiKey = conf.apiKey
        self.exchange.secret = conf.secret

        self.exchange.loadMarkets() #preload market data. NB: forced reloading w reload=True param, TODO: when do we want to do that ? #https://github.com/ccxt/ccxt/wiki/Manual#loading-markets

        self.capital = capital.Capital(self.exchange)
        self.capital.update()

    def do_getExchangeInfo(self):
        filename = 'exg_' + self.exchangeName + '.txt'
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

    def do_list(self, what, customParams, symbol=None):
        #for pair in gv.wholeData:
        #    print(f"{pair} {what}: {str(gv.wholeData[pair][what])}")
        defaultKWargs = { 'params' : customParams }
        name2cmd = {
            'data': {
                'cmd' :'fetchData', #TODO: exchange.fetchData doesn't exists so make it
                'kwargs': { 'symbol' : symbol, 'params' : customParams }
            },
            'orders-all': {
                'cmd' : 'fetchOrders', #working
                'kwargs': { 'symbol' : symbol, 'params' : customParams }
            },
            'orders-open': {
                'cmd' : 'fetchOpenOrders', #working
                'kwargs': { 'symbol' : symbol, 'params' : customParams }
            },
            'orders-closed': {
                'cmd' : 'fetchClosedOrders', #working
                'kwargs': { 'symbol' : symbol, 'params' : customParams }
            },
            'positions': {
                'cmd' : 'private_get_position', #TODO: should be exchange.fetchPositions but doesn't exists on mex so make it
                'kwargs': { 'params': ({ 'filter': json.dumps({ 'symbol': gv.symbol2id[symbol] }) } if symbol is not None else customParams) } #todo exchange specific mex
            },
            'trades': {
                'cmd' : 'fetchMyTrades', #TODO: exchange.fetchMyTrades not available on mex but available on kraken
                'kwargs': { 'symbol' : symbol, 'params' : customParams }
            }
        } #TODO: type cheking of keys

        ret = self._ccxtMethod(name2cmd[what]['cmd'], **name2cmd[what]['kwargs'])
        return (ret if (len(ret) > 0) else 'no '+ what)
    
    def _ccxtMethod(self, ccxtMethod, **kwargs):
        """ccxt Method wrapper"""
        exg = self.exchange
        if not ccxtMethod in exg.has or not exg.has[ccxtMethod]: #ccxt unified method check
            if not hasattr(exg, ccxtMethod): #ccxt implicit (not unified) method check
                return f'{ccxtMethod}() not available for this exchange'

        try:
            #Do we need to (re)load market everytime to get accurate data?
            ret = getattr(exg, ccxtMethod)(**kwargs)
            return ret

        except ccxt.BaseError as error:
            return error.args[0]
        except TypeohlcvError as error:
            return f"invalid argument(s) when calling {ccxtMethod}(). Internal error: {error.args[0]}"

    def do_fetchOHLCV(self, symbol, timeframe, since, limit, customParams = {}):
        #Get data
        tohlcv = self._ccxtMethod('fetchOHLCV', symbol = symbol, timeframe = timeframe, limit = limit, params = customParams) #, since = (exg.seconds()-since)
        #TODO handle exception in return

        #format data into a list
        # initialize a list to store the parsed ohlc data
        tohlcvlist = []

        for period in tohlcv:
            # Initialize an OrderedDict to garantee the column order
            tohlcvdict = dict()
            tohlcvdict["CloseTime"] = formatTS(period[0])
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
        return self._ccxtMethod('fetchBalance', params = customParams)
    def do_fetchTotalBalance(self, customParams):
        return self._ccxtMethod('fetchTotalBalance', params = customParams)
    def do_fetchFreeBalance(self, customParams):
        return self._ccxtMethod('fetchFreeBalance', params = customParams)
    def do_fetchUsedBalance(self, customParams):
        return self._ccxtMethod('fetchUsedBalance', params = customParams)
    def do_fetchPartialBalance(self, customParams):
        return self._ccxtMethod('fetchPartialBalance', params = customParams)

    def do_fetchLedger(self, code, since, limit, customParams):
        return self._ccxtMethod('fetchLedger', code = code, since = since, limit = limit, params = customParams)

    def do_fetchTrades(self, symbol, since, limit, customParams):
        return self._ccxtMethod('fetchTrades', symbol = symbol, since = since, limit = limit, params = customParams)

    def do_fetchMarketPrice(self, symbol):
        orderbook = self._ccxtMethod('fetch_order_book', symbol = symbol)
        bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
        ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
        spread = (ask - bid) if (bid and ask) else None
        return { 'bid': bid, 'ask': ask, 'spread': spread }


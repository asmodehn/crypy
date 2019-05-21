#!/usr/bin/env python
# coding: utf-8
import typing

import json


try:
    from . import capital
    from .order import Order
    from . import errors
    import global_vars as gv
except (ImportError, ValueError, ModuleNotFoundError):
    import crypy.desk.global_vars as gv
    from crypy.desk import capital
    from crypy.desk.order import Order
    from crypy.desk import errors

from .utils import formatTS


try:
    from ..euc import async_support as ccxt
    from .. import config
    from .model.balance import BalanceAll
    from .model.symbol import Symbol, SymbolError
    from .market import Market
except (ImportError, ValueError, ModuleNotFoundError):
    from crypy.euc import async_support as ccxt
    from crypy import config
    from crypy.desk.model.balance import BalanceAll
    from crypy.desk.model.symbol import Symbol, SymbolError
    from crypy.desk.market import Market, MarketError



import structlog
filename = 'desk.log'
file = open( filename, 'a') #TODO where do we close it
#structlog.configure( logger_factory=structlog.PrintLogger(file = file) )
logger = structlog.PrintLogger(file = file)

class Desk:

    @property
    async def markets(self) -> typing.Dict[Symbol, Market]:
        if self.exchange.markets is None:
            await self.exchange.load_markets()

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
    async def balance(self) -> BalanceAll:
        # TODO : timer to do the call only after some timeout...
        bal_raw = await self._ccxtMethod('fetchBalance')
        bal = BalanceAll(**{e: bal_raw.get(e) for e in ['free', 'used', 'total']})
        return bal


    async def __aenter__(self):
        await self.exchange.loadMarkets()  # preload market data. NB: forced reloading w reload=True param, TODO: when do we want to do that ? #https://github.com/ccxt/ccxt/wiki/Manual#loading-markets

        self.capital = capital.Capital(self.exchange)
        self.capital.update()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.exchange.close()

    def __init__(self, conf: config.ExchangeSection = None):
        self.exchangeName = conf.name

        # Using the impl_hook from settings.ini
        self.exchange = conf.exec_hook(ccxt=ccxt)

        # Requesting Key from initialization
        # TODO : anonymous by default, on demand auth
        self.exchange.apiKey = conf.apiKey
        self.exchange.secret = conf.secret


    async def do_getExchangeInfo(self):
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

    async def do_list(self, what, customParams, symbol=None):
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
    
    async def _ccxtMethod(self, ccxtMethod, **kwargs):
        """ccxt Method wrapper"""
        exg = self.exchange
        if not ccxtMethod in exg.has or not exg.has[ccxtMethod]: #ccxt unified method check
            if not hasattr(exg, ccxtMethod): #ccxt implicit (not unified) method check
                return f'{ccxtMethod}() not available for this exchange'

        try:
            #Do we need to (re)load market everytime to get accurate data?
            ret = await getattr(exg, ccxtMethod)(**kwargs)
            return ret

        except ccxt.BaseError as error:
            return error.args[0]
        except TypeError as error:
            return f"invalid argument(s) when calling {ccxtMethod}(). Internal error: {error.args[0]}"

    async def do_fetchOHLCV(self, symbol, timeframe, since, limit, customParams = {}):
        #NB: this fetch OHLCV from the start of the exchange pair on Mex
        
        #TODO handle supported exchanges.timeframes

        #NB: the "since" param has precedence over the "limit" one (which is just a max)
        #So if we want to have the "full" limit backward from the current time we need to compute a since value from $now, otherwise will only get the latest candle
        if since is None and limit is not None:
            since = self.exchange.milliseconds() - gv.tf2second[timeframe]*1000 * limit #datetimes and timestamps https://github.com/ccxt/ccxt/wiki/Manual#working-with-datetimes-and-timestamps
        elif since is not None: #we need to format it to a ms timestamp
            import pytz, datetime
            #Datetime ops https://www.programiz.com/python-programming/datetime
            #Format: https://www.programiz.com/python-programming/datetime/strftime
            #TimeZone: https://pypi.org/project/pytz/
            parisTZ = pytz.timezone("Europe/Paris")
            since = parisTZ.localize(since)
            since = since.astimezone(pytz.utc)
            since = since.timestamp() * 1000 #timestamp in millisecond

        #Get data
        tohlcv = await self._ccxtMethod('fetchOHLCV', symbol = symbol, timeframe = timeframe, since = since, limit = limit, params = customParams)
        if isinstance(tohlcv, str): #handle return in error
            return tohlcv

        #format data into a list
        #initialize a list to store the parsed ohlc data
        tohlcvlist = []

        for period in tohlcv:
            # Initialize an OrderedDict to garantee the column order
            tohlcvdict = dict()
            tohlcvdict["CloseTimeUTC"] = formatTS(period[0])
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

    async def do_fetchBalance(self, customParams, part = None):
        if part is None:
            return await self._ccxtMethod('fetchBalance', params = customParams)
        else:
            return await self._ccxtMethod('fetchPartialBalance', part = part, params = customParams)

    async def do_fetchLedger(self, code, since, limit, customParams):
        return await self._ccxtMethod('fetchLedger', code = code, since = since, limit = limit, params = customParams)

    async def do_fetchTrades(self, symbol, since, limit, customParams):
        return await self._ccxtMethod('fetchTrades', symbol = symbol, since = since, limit = limit, params = customParams)

    async def do_fetchMarketPrice(self, symbol):
        orderbook = await self._ccxtMethod('fetch_order_book', symbol = symbol)
        bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
        ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
        spread = (ask - bid) if (bid and ask) else None
        return { 'bid': bid, 'ask': ask, 'spread': spread }


    async def fetchL2OrderBook(self, symbol, limit):
        orderbook = await self._ccxtMethod('fetchL2OrderBook', symbol = symbol, limit = limit)
        return orderbook #TODO better format i guess


    async def create_order(self, symbol, order_type, expiracy, side, amount=None, price=None, peg_offset_value=None,
                         peg_price_type=None, leverage=None, display_qty=None, stop_px=None, exec_inst=None):

        # TODO proper return type (see https://github.com/dry-python/returns for example) to handle errors via type
        if not 'createOrder' in self.exchange.has or not self.exchange.has['createOrder']:
            raise errors.CrypyException(msg=f'createOrder() not available for this exchange')

        ### TYPE handling ###
        if order_type in ['Market', 'Limit']:
            # if self.data['leverage'] > 1:
            # set leverage in call cases, working on bitmex, check other exchanges
            if not hasattr(self.exchange, 'privatePostPositionLeverage'):
                raise errors.CrypyException(msg=f'privatePostPositionLeverage() not available for this exchange')

        # TODO : instantiate the order implementation matching our current exchange.
        order = Order(symbol=symbol, side=side, type=order_type, leverage=leverage,
                      display_qty=display_qty, stop_px=stop_px, peg_offset_value=peg_offset_value,
                      peg_price_type=peg_price_type, exec_inst=exec_inst, expiracy=expiracy, id=None,
                      amount=amount,
                      price=price)

        return order

    async def edit_order(self, symbol, order_type, expiracy, order_id, side, amount=None, price=None, peg_offset_value=None,
                   peg_price_type=None, leverage=None, display_qty=None, stop_px=None, exec_inst=None):

        # TODO proper return type (see https://github.com/dry-python/returns for example) to handle errors via type
        if not 'editOrder' in self.exchange.has or not self.exchange.has['editOrder']:
            raise errors.CrypyException(f'editOrder() not available for this exchange')

        ### TYPE handling ###
        if order_type in ['Market', 'Limit']:
            # if self.data['leverage'] > 1:
            # set leverage in call cases, working on bitmex, check other exchanges
            if not hasattr(self.exchange, 'privatePostPositionLeverage'):
                raise errors.CrypyException(msg=f'privatePostPositionLeverage() not available for this exchange')

        order = await Order(symbol=symbol, side=side, type=order_type, leverage=leverage,
                      display_qty=display_qty, stop_px=stop_px, peg_offset_value=peg_offset_value,
                      peg_price_type=peg_price_type, exec_inst=exec_inst, expiracy=expiracy, id=order_id, amount=amount,
                      price=price)

        return order

    async def execute_order(self, ordr: Order):
        try:
            # first handle the leverage (NB: it changes leverage of existing orders too!)
            # NB: we do it here coz we cant the leverage value to be visible when showing data
            leverage = ordr.data['leverage']
            if leverage is not None:
                response2 = await self.exchange.privatePostPositionLeverage(
                    {"symbol": self.exchange.markets[ordr.data['symbol']]['id'], "leverage": leverage})
                logger.msg(str(response2))
            del ordr.data['leverage']  # remove the leverage from the order data coz createOrder() doesnt handle it

            # second post/update order
            if 'id' not in ordr.data:
                response = await self.exchange.createOrder(**dict(ordr.data))
            else:
                response = await self.exchange.editOrder(**dict(ordr.data))

            logger.msg(str(response))

            return 'order_id: ' + response['id']

        except ccxt.BaseError as error:
            return error.args[0]
        except Exception as error:
            return "Error: " + str(type(error)) + " " + str(error)

    async def cancel_order(self, order_ids):
        if not 'cancelOrder' in self.exchange.has or not self.exchange.has['cancelOrder']:
            return f'cancelOrder() not available for this exchange'

        for order_id in order_ids:
            try:
                await self.exchange.cancelOrder(order_id)
                print(f'order(s) {order_id} canceled')
                #TODO remove from order log also
            except ccxt.NetworkError as err:
                #TODO retry cancelation
                pass
            except ccxt.ValidationError as err:
                print(f'order(s) {order_id} invalid: bad length, cancel failed')
            except ccxt.OrderNotFound as err:
                print(f'order(s) {order_id} not found: already canceled/closed or invalid order id, cancel failed')
            except ccxt.BaseError as error:
                print(f'order(s) {order_id} not found invalid order id or something else, cancel failed')
                print(error.args[0])


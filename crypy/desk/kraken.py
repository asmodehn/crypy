import dataclasses

import numpy
import pandas

import time

import functools
import typing
import logging
from dataclasses import dataclass, field
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


try:
    from ..euc import ccxt
    from .. import config
except (ImportError, ValueError):
    from crypy.euc import ccxt
    from crypy import config

try:
    from . import errors, limiter
    from .impl import ccxt as impl
except ImportError:
    from crypy.desk import errors, limiter
    from crypy.desk.impl import ccxt as impl

#
# # TODO :check pydantic to verify config data
# Credentials = typing.NamedTuple(typename="Credentials", fields=[
#     ("apiKey", str),
#     ("secret", str),
#     ("uid", typing.Optional[str]),
#     ("login", typing.Optional[str]),
#     ("password", typing.Optional[str]),
#     ("twofa", typing.Optional[str]),  # 2-factor authentication (one-time password key)
#     ("privateKey", typing.Optional[str]),  # a "0x"-prefixed hexstring private key for a wallet
#     ("walletAddress", typing.Optional[str])
# ])


#: one limiter per IP, ie. per interpreter instance.
public_limiter = limiter.CallDropper(max_cps=1.0)


@dataclass
class PrivateLimiter:
    max_cps: int = 15
    apiKey: str = 0
    callcounter: int = 0
    last_call: float = field(init=False)

    def __call__(self, decr_period: int = 3):

        def decorator(func):
            nonlocal self

            def wrapper(*args, **kwargs):
                nonlocal self
                # Too hacky
                # TODO : link with limiter's measured time
                now = time.perf_counter()
                time_since_last_call = now - self.last_call
                self.last_call = now
                # We can simulate time passing on the spot (non need for background running thread).
                self.callcounter += 1 - time_since_last_call / decr_period
                func(*args, **kwargs)

            return limiter.CallDropper(max_cps=self.max_cps)(wrapper)
        return decorator


#TODO : fix it, this is still WIP...
def Tier2Limiter(apiKey):
    return functools.partial(PrivateLimiter, max_cps=15, apiKey=apiKey)


def Tier3Limiter(apiKey):
    return functools.partial(PrivateLimiter, max_cps=20, apiKey=apiKey)


def Tier4Limiter(apiKey):
    return functools.partial(PrivateLimiter, max_cps=20, apiKey=apiKey)


@dataclass
class OrderLimiter:
    pass


class OHLC(typing.NamedTuple):
    Open: float
    High: float
    Low: float
    Close: float


class Public:
    """
    Kraken API returning panda dataframes

    TODO : consolidate to make a more functional interface... see Caerbannog.
    TODO : test it, extensively.
    TODO :  support different libraries as implementation.
    """

    def __init__(self, conf: config.Config = None, public=True):
        """Initializing a public desk for kraken
        public is ony meant to be used by private kraken desk. TODO : better design ?
        """
        conf = conf if conf is not None else config.Config()

        #self.exchange = impl.kraken(conf, public)
        self.exchange = impl.bitmex(conf, public)

    ## Properties (proxy objects for remote data)

    @property
    def markets(self):
        if self.exchange.markets is None:
            self.exchange.load_markets()
        return self.exchange.markets



    ## Public API

    @public_limiter
    def _load_markets(self, reload=False):
        """This calls self.exchange.fetch_markets internally"""
        self.exchange.load_markets(reload=reload)
        return self

    @public_limiter
    def _fetch_markets(self):

        # {
        #     'id':     'btcusd',   // string literal for referencing within an exchange
        #     'symbol': 'BTC/USD',  // uppercase string literal of a pair of currencies
        #     'base':   'BTC',      // uppercase string, base currency, 3 or more letters
        #     'quote':  'USD',      // uppercase string, quote currency, 3 or more letters
        #     'active': true,       // boolean, market status
        #     'precision': {        // number of decimal digits "after the dot"
        #         'price': 8,       // integer, might be missing if not supplied by the exchange
        #         'amount': 8,      // integer, might be missing if not supplied by the exchange
        #         'cost': 8,        // integer, very few exchanges actually have it
        #     },
        #     'limits': {           // value limits when placing orders on this market
        #         'amount': {
        #             'min': 0.01,  // order amount should be > min
        #             'max': 1000,  // order amount should be < max
        #         },
        #         'price': { ... }, // same min/max limits for the price of the order
        #         'cost':  { ... }, // same limits for order cost = price * amount
        #     },
        #     'info':      { ... }, // the original unparsed market info from the exchange
        # }

        self.exchange.fetch_markets()
        return self

    #@public_limiter
    def _fetch_currencies(self):
        currencies = self.exchange.fetch_currencies()

        return currencies

    #@public_limiter
    def _fetch_ticker(self, symbol, params=None):
        params = {} if params is None else params

        # {
        #     'symbol':        string symbol of the market ('BTC/USD', 'ETH/BTC', ...)
        #     'info':        { the original non-modified unparsed reply from exchange API },
        #     'timestamp':     int (64-bit Unix Timestamp in milliseconds since Epoch 1 Jan 1970)
        #     'datetime':      ISO8601 datetime string with milliseconds
        #     'high':          float, // highest price
        #     'low':           float, // lowest price
        #     'bid':           float, // current best bid (buy) price
        #     'bidVolume':     float, // current best bid (buy) amount (may be missing or undefined)
        #     'ask':           float, // current best ask (sell) price
        #     'askVolume':     float, // current best ask (sell) amount (may be missing or undefined)
        #     'vwap':          float, // volume weighed average price
        #     'open':          float, // opening price
        #     'close':         float, // price of last trade (closing price for current period)
        #     'last':          float, // same as `close`, duplicated for convenience
        #     'previousClose': float, // closing price for the previous period
        #     'change':        float, // absolute change, `last - open`
        #     'percentage':    float, // relative change, `(change/open) * 100`
        #     'average':       float, // average price, `(last + open) / 2`
        #     'baseVolume':    float, // volume of base currency traded for last 24 hours
        #     'quoteVolume':   float, // volume of quote currency traded for last 24 hours
        # }

        ticker = self.exchange.fetch_ticker(symbol, params=params)

        return ticker

    # TODO : maybe not available for kraken... to verify
    @public_limiter
    def _fetch_tickers(self):
        return self.exchange.fetch_tickers()

    @public_limiter
    def _fetch_orderbook(self):
        book = self.exchange.fetch_orderbook()

        return book

    # TMP : relying on ccxt limiter for now
    #@public_limiter
    def fetch_ohlcv(self, symbol, timeframe='1d', since=None, limit=None, params=None):
        params = {} if params is None else params

        # [
        #     [
        #         1504541580000, // UTC timestamp in milliseconds, integer
        #         4235.4,        // (O)pen price, float
        #         4240.6,        // (H)ighest price, float
        #         4230.0,        // (L)owest price, float
        #         4230.7,        // (C)losing price, float
        #         37.72941911    // (V)olume (in terms of the base currency), float
        #     ],
        #     ...
        # ]

        # get raw data in numpy
        ohlcv = numpy.array(self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit, params=params))

        # filter what we need to get into pandas series/dataframes
        df = pandas.DataFrame(data=ohlcv[:, 1:], index=ohlcv[:, 0], columns=["Open", "High", "Low", "Close", "Volume"], dtype=float)

        return df

    # TMP : relying on ccxt limiter for now
    #@public_limiter
    def _fetch_trades(self, symbol, since=None, limit=None, params=None):
        params = {} if params is None else params

        # [
        #     {
        #         'info':       { ... },                  // the original decoded JSON as is
        #         'id':        '12345-67890:09876/54321', // string trade id
        #         'timestamp':  1502962946216,            // Unix timestamp in milliseconds
        #         'datetime':  '2017-08-17 12:42:48.000', // ISO8601 datetime with milliseconds
        #         'symbol':    'ETH/BTC',                 // symbol
        #         'order':     '12345-67890:09876/54321', // string order id or undefined/None/null
        #         'type':      'limit',                   // order type, 'market', 'limit' or undefined/None/null
        #         'side':      'buy',                     // direction of the trade, 'buy' or 'sell'
        #         'price':      0.06917684,               // float price in quote currency
        #         'amount':     1.5,                      // amount of base currency
        #     },
        #     ...
        # ]


        trades = self.exchange.fetch_trades(symbol, since=since, limit=limit, params=params)

        return trades


class Private(Public):

    @property
    def apiKey(self):
        logging.warning("APIKey accessed for Kraken")
        return self.exchange.apiKey

    @apiKey.setter
    def apiKey(self, apiKey: str):
        logging.warning("APIKey modified for Kraken")
        setattr(self.exchange, 'apiKey', apiKey)
        # WIP : is this enough or do we need to reset the exchange ??

    @property
    def secret(self):
        logging.warning("Secret accessed for Kraken")
        return self.exchange.secret

    @secret.setter
    def secret(self, secret: str):
        logging.warning("Secret modified for Kraken")
        setattr(self.exchange, 'secret', secret)
        # WIP : is this enough or do we need to reset the exchange ??

    def __init__(self, conf=None):
        super().__init__(conf, public=False)

    @property
    def balance(self):
        """Fetches the balance of the account.
        If this fails because we are not authenticated, provide a solution in the exception.
        """
        try:
            self._balance = self.exchange.fetch_balance()
        except ccxt.base.errors.AuthenticationError as exc:
            raise
            # TODO : interactive login if needed
            def auth_n_retry(*args, **kwargs):
                self.credentials_set(*args, **kwargs)
                return self.balance

            raise errors.AuthenticationError(original=exc, fixer=auth_n_retry)
        return self._balance

    def create_order(self):
        return self.exchange.create_order()

    def cancel_order(self):
        return self.exchange.cancel_order()

    def fetch_order(self):
        return self.exchange.fetch_order()

    def fetch_orders(self):
        # {
        #     'bids': [
        #         [ price, amount ], // [ float, float ]
        #         [ price, amount ],
        #         ...
        #     ],
        #     'asks': [
        #         [ price, amount ],
        #         [ price, amount ],
        #         ...
        #     ],
        #     'timestamp': 1499280391811, // Unix Timestamp in milliseconds (seconds * 1000)
        #     'datetime': '2017-07-05T18:47:14.692Z', // ISO8601 datetime string with milliseconds
        # }

        orders = self.exchange.fetch_orders()

        return orders

    def fetch_open_orders(self):
        return self.exchange.fetch_open_orders()

    def fetch_closed_orders(self):
        return self.exchange.fetch_closed_orders()

    def fetch_my_trades(self):
        return self.exchange.fetch_my_trades()

    def deposit(self):
        return self.exchange.deposit()

    def withdraw(self):
        return self.exchange.withdraw()


if __name__ == '__main__':

    k = Public()
    print(k.markets)

    #k.fetch_ohlcv('ADA/CAD').plot()
    #plt.show()

    #res = k._fetch_ticker('ADA/CAD')
    #print(res)


    # res = k._fetch_currencies()
    # print(res)

    # res = k._fetch_trades('ADA/CAD')
    #
    # print(res)



    kpriv = Private()
    #print(kpriv.markets)
    #print(kpriv.balance)

    kpriv.fetch_orders()

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
except ImportError:
    from crypy.desk import errors, limiter

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
        assert 'kraken.com' in conf.sections.keys()  # preventing errors early

        if public:
            self.conf = conf.sections.get('kraken.com').public()
        else:
            self.conf = conf.sections.get('kraken.com')

        self.exchange = ccxt.kraken(dataclasses.asdict(self.conf))


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
        self.exchange.fetch_markets()
        return self

    @public_limiter
    def _fetch_currencies(self):
        return self.exchange.fetch_currencies()

    @public_limiter
    def _fetch_ticker(self):
        return self.exchange.fetch_ticker()

    @public_limiter
    def _fetch_tickers(self):
        return self.exchange.fetch_tickers()

    @public_limiter
    def _fetch_orderbook(self):
        return self.exchange.fetch_orderbook()

    # TMP : relying on ccxt limiter for now
    #@public_limiter
    def fetch_ohlcv(self, symbol, timeframe='1d', since=None, limit=None, params=None):
        params = {} if params is None else params
        # get raw data in numpy
        ohlcv = numpy.array(self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit, params=params))

        # filter what we need to get into pandas series/dataframes
        df = pandas.DataFrame(data=ohlcv[:, 1:], index=ohlcv[:, 0], columns=["Open", "High", "Low", "Close", "Volume"], dtype=float)

        return df

    @public_limiter
    def _fetch_trades(self):
        return self.exchange.fetch_trades()


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
        return self.exchange.fetch_orders()

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
    #print(k.markets)

    k.fetch_ohlcv('ADA/CAD').plot()

    plt.show()

    #kpriv = Private()
    #print(kpriv.markets)
    #print(kpriv.balance)


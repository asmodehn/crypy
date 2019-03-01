import dataclasses
import typing

try:
    from ...euc import ccxt
    from ... import config
except (ImportError, ValueError):
    from crypy.euc import ccxt
    from crypy import config

try:
    from .. import errors, limiter, exchange, market, symbol
except (ImportError, ValueError):
    from crypy.desk import errors, limiter, exchange, market, symbol

"""
Module implementing APIs with various exchanges, through ccxt.
returns raw data, extracted from the API library
"""


class CCXT(exchange.Exchange):

    def __init__(self, impl):
        self.impl = impl

        super().__init__(apiKey = self.impl.apiKey,
                         secret = self.impl.secret,
                         timeout = self.impl.timeout,
                         ratelimited = self.impl.enableRateLimit,
                         verbose = self.impl.verbose)


    @property
    def markets(self) -> typing.List[market.Market]:
        if self.impl.markets is None:
            self.impl.load_markets()

        mlist = []
        for s, m in self.impl.markets.items():
            mlist.append(market.Market(symbol=s,
                                       active=m.get('active'),
                                       precision= m.get('precision'),
                                       limits= m.get('limits'),

                                       # more TODO




                                       ))

        # Formatting with proper class instances


        return mlist



def kraken(apiKey="", secret="", timeout = 30000, enableRateLimit = True, verbose=False):
    """Initializing an exchange proxy for kraken
    """

    return CCXT(impl=ccxt.kraken(config={
        'apiKey' : apiKey,
        'secret' : secret,
        'timeout': timeout,
        'enableRateLimit': enableRateLimit,
        'verbose': verbose,
    }))


def bitmex(apiKey="", secret="", timeout = 30000, enableRateLimit = True, verbose=False, paper=True):
    """Initializing an exchange proxy for bitmex
    """

    return CCXT(impl=ccxt.bitmex(config={
        'apiKey' : apiKey,
        'secret' : secret,
        'timeout': timeout,
        'enableRateLimit': enableRateLimit,
        'verbose': verbose,
    }))

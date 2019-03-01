#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

import pandas


try:
    from ..euc import ccxt
    from .. import config
except (ImportError, ValueError):
    from crypy.euc import ccxt
    from crypy import config

try:
    from . import errors, limiter
    from .symbol import Symbol
except ImportError:
    from crypy.desk import errors, limiter
    from crypy.desk.symbol import Symbol


@dataclass(frozen=True)
class Ticker:
    symbol: Symbol  # symbol of the market ('BTC/USD', 'ETH/BTC', ...)
    timestamp: pandas.Timestamp  # Timestamp

    high: float  # highest price
    low: float  # lowest price
    bid: float  # current best bid (buy) price
    bidVolume: float  # current best bid (buy) amount (may be missing or undefined)
    ask: float  # current best ask (sell) price
    askVolume: float  # current best ask (sell) amount (may be missing or undefined)
    vwap: float  # volume weighed average price
    open: float  # opening price
    close: float  # price of last trade (closing price for current period)
    last: float  # same as `close`, duplicated for convenience
    previousClose: float  # closing price for the previous period
    change: float  # absolute change, `last - open`
    percentage: float  # relative change, `(change/open) * 100`
    average: float  # average price, `(last + open) / 2`
    baseVolume: float  # volume of base currency traded for last 24 hours
    quoteVolume: float  # volume of quote currency traded for last 24 hours



def ticker(api, symbol, params=None):
    params = {} if params is None else params

    ticker_data = api.exchange.fetch_ticker(symbol, params=params)

    return Ticker()


# TODO
# if __name__ == "__main__":
#
#     s = symbol("EUR/ETH")
#     assert type(s) is Symbol
#     print(s.base)
#     assert type(s.base) is Currency and s.base == Currency("EUR")
#     print(s.quote)
#     assert type(s.quote) is Currency and s.quote == Currency("ETH")
#     print(s)



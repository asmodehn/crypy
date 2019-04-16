#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import typing
from pydantic.dataclasses import dataclass

import pandas


try:
    from ..euc import ccxt
    from .. import config
except (ImportError, ValueError):
    from crypy.euc import ccxt
    from crypy import config

try:
    from . import errors, limiter
    from crypy.desk.model.symbol import Symbol
except ImportError:
    from crypy.desk import errors, limiter
    from crypy.desk.model.symbol import Symbol


class TickerError(errors.CrypyException):
    pass


@dataclass(frozen=True)
class Ticker:

    @staticmethod
    def from_dict(data: dict) -> Ticker:
        return Ticker(**data)

    symbol: Symbol  # symbol of the market ('BTC/USD', 'ETH/BTC', ...)
    timestamp: pandas.Timestamp  # Timestamp

    high: float  # highest price
    low: float  # lowest price
    bid: float  # current best bid (buy) price
    bidVolume: typing.Optional[float]  # current best bid (buy) amount (may be missing or undefined)
    ask: float  # current best ask (sell) price
    askVolume: typing.Optional[float]  # current best ask (sell) amount (may be missing or undefined)
    vwap: float  # volume weighed average price
    open: float  # opening price
    close: float  # price of last trade (closing price for current period)
    # last: float
    previousClose: typing.Optional[float]  # closing price for the previous period
    # TODO : we need these only if we get it in the data from the exchange. otherwise we compute on demand.
    # change: float
    # percentage: float
    # average: float
    baseVolume: float  # volume of base currency traded for last 24 hours
    quoteVolume: float  # volume of quote currency traded for last 24 hours

    @property
    def last(self):  # same as `close`, duplicated for convenience
        return self.close

    @property
    def change(self):  # absolute change, `last - open`
        return self.close - self.open

    @property
    def percentage(self):  # relative change, `(change/open) * 100`
        return (self.change * 100.0) / self.open

    @property
    def average(self):   # average price, `(last + open) / 2`
        return (self.close + self.open) / 2


# def ticker(s: Symbol, t:pandas.Timestamp, high: float, low: float,
#            bid: float,  ask: float,  vwap: float, open: float, close: float,
#            last: float,change: float, percentage: float, average: float, baseVolume: float, quoteVolume: float,
#             bidVolume:float = None,
#            askVolume: float = None,
#            previousClose: float = None):
#
#     #TODO : proper type based data validation (pydantic or other)
#     return Ticker(symbol=s,
#                   timestamp=t,
#                   high=float(high),
#                   low=float(low),
#                   bid=float(bid),
#                   bidVolume=float(bidVolume) if bidVolume is not None else None,
#                   ask=float(ask),
#                   askVolume=float(askVolume) if askVolume is not None else None,
#                   vwap=float(vwap),
#                   open=float(open),
#                   close=float(close),
#                   #last=float(last),
#                   previousClose=float(previousClose) if previousClose is not None else None,
#                   #change=float(change)if change is not None else None,
#                   #percentage=float(percentage),
#                   #average=float(average),
#                   baseVolume=float(baseVolume),
#                   quoteVolume=float(quoteVolume)
#                   )


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



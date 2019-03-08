#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

from pydantic.dataclasses import dataclass

import numpy
import pandas
import pydantic
import typing

try:
    from ...euc import ccxt
    from ... import config
except (ImportError, ValueError):
    from crypy.euc import ccxt
    from crypy import config

try:
    from .. import errors, bounds, limiter, exchange, market, symbol, ticker, limits
    from ..precision import Precision  # solving forward ref errors for pydantic
except (ImportError, ValueError):
    from crypy.desk import errors, bounds, limiter, exchange, market, symbol, ticker, limits
    from crypy.desk.precision import Precision  # solving forward ref errors for pydantic

"""
Module implementing APIs with various exchanges, through ccxt.
returns raw data, extracted from the API library
"""


@dataclass(frozen=True)
class Symbol(symbol.Symbol):

    @staticmethod
    def from_str(s: str) -> Symbol:
        try:
            base, quote = s.split("/")
        except ValueError as ve:  # not enough values to unpack
            raise symbol.SymbolError(msg="Cannot parse symbol {s}", original =ve)
        return Symbol(symbol.Currency(base), symbol.Currency(quote))


@dataclass
class Bounds(bounds.Bounds):

    @staticmethod
    def from_dict(data: dict) -> Bounds:
        return super().__init__(upper=data.get('max'),
                      lower=data.get('min'))


@dataclass
class Limits(limits.Limits):

    @staticmethod
    def from_dict(data: dict) -> Limits:
        return Limits(**data)

    # making sure we get our overload of Bounds as type here
    price: Bounds
    amount: Bounds
    cost: Bounds


@dataclass
class Market(market.Market):

    @staticmethod
    def from_dict(data: dict) -> Market:
        return Market(**{k: w for k, w in data.items() if k in Market.__annotations__})

    # Using overloaded Symbol
    @pydantic.validator('symbol')
    def symbol_from_str(cls, v: str):
        return Symbol.from_str(v)

    # Using overloaded limits (depending on overloaded bounds for ccxt)
    @pydantic.validator('limits')
    def limits_from_dict(cls, v: dict ):
        return Limits.from_dict(v)

    # Using base precision (no extra meaning for ccxt)
    @pydantic.validator('precision')
    def precision_from_dict(cls, v: dict):
        return Precision.from_dict(v)


    def ticker(self) -> ticker.Ticker:
        ccxt_ticker = self.impl.fetch_ticker(str(self.symbol))

        t = ticker.Ticker.factory(ccxt_ticker)

        return t

    def ohlcv(self, s: symbol.Symbol, timeframe='1d', since=None, limit=None, params=None) -> pandas.DataFrame:
        params = {} if params is None else params

        ohlcv = numpy.array(
            self.impl.fetch_ohlcv(str(s), timeframe=timeframe, since=since, limit=limit, params=params))

        # filter what we need to get into pandas series/dataframes
        df = pandas.DataFrame(data=ohlcv[:, 1:], index=ohlcv[:, 0], columns=["Open", "High", "Low", "Close", "Volume"],
                              dtype=float)

        return df



class Exchange(exchange.Exchange):

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

        mdict = dict()
        for s, m in self.impl.markets.items():
            try:
                mdict[symbol.Symbol.from_str(s)] = Market.from_dict(m)
            except market.MarketError as me:
                pass  # ignoring erroring data for now

        # Formatting with proper class instances


        return mdict




def kraken(apiKey="", secret="", timeout = 30000, enableRateLimit = True, verbose=False):
    """Initializing an exchange proxy for kraken
    """

    return Exchange(impl=ccxt.kraken(config={
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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import typing
import pandas
from pydantic.dataclasses import dataclass
from pydantic import validator
from dataclasses import field
from .errors import CrypyException
from .bounded_price import BoundedPrice, BoundedPriceError
from .bounded_amount import BoundedAmount, BoundedAmountError
from .bounded_cost import BoundedCost, BoundedCostError
from .symbol import Symbol, SymbolError
from .ticker import Ticker, TickerError
from .limits import Limits, LimitsError

from datetime import datetime
import dateutil.parser

from .impl.mpmath import MPFloat, MPFuzzyFloat, MPBoundedFloat, MPBoundedFuzzyFloat


class MarketError(CrypyException):
    pass


# Ref : https://stackoverflow.com/questions/53376099/python-dataclass-from-dict

@dataclass
class Tiers:

    @staticmethod
    def factory(data: dict) -> Tiers:

        return Tiers(**data)

    taker: typing.List[tuple]
    maker: typing.List[tuple]


@dataclass
class Market:

    @staticmethod
    def from_dict(data: dict) -> typing.Optional[Market]:

        a = p = c = None

        for k, e in {'price': p, 'amount':a, 'cost':c}.items():
            value = data.get(k)
            if value is not None:
                precision = data.get('precision').get(k)
                limits = data.get('limits').get(k)
                if precision is not None:
                    if limits is not None:
                        e = MPBoundedFuzzyFloat(value=value, bounds=limits)
                    else: # no bounds
                        e = MPFuzzyFloat(value=value)
                elif limits is not None: # no precision
                    e = MPBoundedFloat(value=value, bounds=limits)
                else: # no bounds no precision
                    e= MPFloat(value=value)
            # else e remains None

            try:
                return Market(
                    symbol=data.get('symbol'),
                    active=data.get('active'),
                    price=p,
                    amount=a,
                    cost=c,
                )
            except Exception as exc:
                return None

    symbol: Symbol
    active: bool

    price: typing.Optional[typing.Union[MPBoundedFuzzyFloat, MPFuzzyFloat, MPBoundedFloat, MPFloat]]
    amount: typing.Optional[typing.Union[MPBoundedFuzzyFloat, MPFuzzyFloat, MPBoundedFloat, MPFloat]]
    cost: typing.Optional[typing.Union[MPBoundedFuzzyFloat, MPFuzzyFloat, MPBoundedFloat, MPFloat]]

    @validator('symbol')
    def symbol_from_str(cls, v: str):
        return Symbol.from_str(v)

    # @validator('price')
    # def price_from_dict(cls, v: dict):
    #     return Precision.from_dict(v)
    #
    # @validator('amount')
    # def amount_from_dict(cls, v: dict ):
    #     return Limits.from_dict(v)
    #
    # @validator('cost')
    # def cost_from_dict(cls, v: dict ):
    #     return Limits.from_dict(v)


    #TODO
    #taker: float
    #maker: float
    #tiers: Tiers

    def ticker(self) -> Ticker:
        return  # TODO : proper and safe error/non-implementation signalling ?

    def ohlcv(self, timeframe='1d', since=None, limit=None, params=None) -> pandas.DataFrame:
        return  # TODO : proper and safe error/non-implementation signalling ?


# def market_factory(sym: str, active: bool, p: dict, lim: dict) -> Market:
#     """utility function to typecheck/convert/validate raw data"""
#     # TODO : use pydantic or similar dynamic typechecker
#
#     try:
#         s = Symbol.from_str(sym)
#     except SymbolError as se:
#         raise MarketError(msg="Market not recognized", original=se)
#     a = bool(active)
#     p = Precision.factory(p)  # assuming it is passed as a dict
#     l = Limits.factory({k: bounds(upper=v.get('max'), lower=v.get('min')) for k, v in lim.items()})   # assuming it is passed as a dict
#
#     return Market(symbol=s, active=a, precision=p, limits=l)

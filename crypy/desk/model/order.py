# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import datetime
import uuid
import enum

import typing

from . import symbol


from pydantic.dataclasses import dataclass
from pydantic import validator
from pydantic import ValidationError

try:
    from ..errors import CrypyException
except (ImportError, ValueError):
    from crypy.desk.errors import CrypyException


"""
Module defining Currency and Symbol
To use types to filter out what we are not interested in.
"""

class OrderError(CrypyException):
    pass



class OrderSide(enum.Enum):
    sell= 'sell'
    buy= 'buy'

    def __str__(self) -> str:
        return f'{self.name}'

    def __repr__(self) -> str:
        return f'{self.name}'


class OrderStatus(enum.Enum):
    open= 'open'
    closed= 'closed'

    def __str__(self) -> str:
        return f'{self.name}'

    def __repr__(self) -> str:
        return f'{self.name}'


class OrderType(enum.Enum):
    market= 'market'
    limit = 'limit'

    def __str__(self) -> str:
        return f'{self.name}'

    def __repr__(self) -> str:
        return f'{self.name}'


@dataclass(frozen=True)
class Order:
    """
    Clean Model for Order data we get from an exchange.
    This dataclass aims at invalidating any suspicious data we get from the network.
    It remains to be seen if the same class/type can be used for data that we build ourselves (orders before sending them to the exchange)
    """

    id: uuid.UUID
    timestamp: int
    datetime: datetime.datetime
    lastTradeTimestamp: int
    symbol: symbol.Symbol
    side: OrderSide
    price: float
    amount: float
    cost: float
    filled: float
    remaining: float
    type: OrderType
    status: OrderStatus
    fee: typing.Optional[float]

    @validator('symbol', pre=True, always=True)
    def cast_Symbol(cls, v: str) -> symbol.Symbol:

        if isinstance(v, symbol.Symbol):
            return v
        else:
            try:
                if isinstance(v, str):
                    s = symbol.Symbol.from_str(v)
                else:
                    raise OrderError(f"Symbol not parsed from {v}")

            except CrypyException:
                raise OrderError(f"Symbol not parsed from {v}")
        return s


def parse(d) -> Order:

    o = Order(**{
        k : v for k, v in d.items()
        if k not in ['info']
    })
    return o


if __name__ == "__main__":
    import unittest
    import doctest

    testSuite = unittest.TestSuite()
    testSuite.addTest(doctest.DocTestSuite())
    unittest.TextTestRunner(verbosity=2).run(testSuite)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import typing
import pandas
from pydantic.dataclasses import dataclass
from dataclasses import field
from .errors import CrypyException
from .bounds import bounds, Bounds
from .symbol import Symbol, SymbolError
from .ticker import Ticker, TickerError
from .precision import Precision, PrecisionError

from datetime import datetime
import dateutil.parser


class LimitsError(CrypyException):
    pass

@dataclass
class Limits:

    @staticmethod
    def from_dict(data: dict) -> Limits:
        return Limits(**data)

    price: Bounds
    amount: Bounds
    cost: Bounds


# def limits(price: Bounds, amount: Bounds, cost: Bounds) -> Limits:
#     return Limits(price=price,
#                   amount=amount,
#                   cost=cost)


# TODO:
if __name__ == '__main__':
    # test code
    pass


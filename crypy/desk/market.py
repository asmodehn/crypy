import typing
from dataclasses import dataclass, field
from .bounds import Bounds
from .symbol import symbol, Symbol


@dataclass
class Precision:
    price: int
    amount: int
    cost: int


@dataclass
class Limits:
    price: Bounds
    amount: Bounds
    cost: Bounds


@dataclass
class Tiers:
    taker: typing.List[tuple]
    maker: typing.List[tuple]


@dataclass
class Market:
    symbol: Symbol
    active: bool
    precision: Precision
    limits: Limits

    #TODO
    #taker: float
    #maker: float
    #tiers: Tiers


def market(sym, active, precision, limits) -> Market:
    """utility function to typecheck/convert/validate raw data"""
    # TODO : use pydantic or similar dynamic typechecker

    s = symbol(sym)
    a = bool(active)
    p = Precision(**precision)  # assuming it is passed as a dict
    l = Limits(**limits)  # assuming it is passed as a dict

    return Market(symbol=s, active=a, precision=p, limits=l)

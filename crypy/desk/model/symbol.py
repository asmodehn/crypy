#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import typing
from enum import Enum

from pydantic.dataclasses import dataclass
try:
    from desk.errors import CrypyException
except (ImportError, ValueError):
    from crypy.desk.errors import CrypyException


class CurrencyError(CrypyException):
    pass


class SymbolError(CrypyException):
    pass


"""
Module defining Currency and Symbol
To use types to filter out what we are not interested in.
"""


class Currency(Enum):
    def __str__(self) -> str:
        return f'{self.name}'

    def __repr__(self) -> str:
        return f'{self.name}'


# Enums to store accepted currencies.
# Unknown currencies will be ignored by pydantic
class Fiat(Currency):
    """
    >>> Fiat('EUR')
    EUR
    """
    EUR= 'EUR'
    USD= 'USD'
    CAD= 'CAD'
    KRW= 'KRW'
    JPY= 'JPY'


class Crypto(Currency):
    """
    >>> Crypto('BTC')
    BTC
    """
    BTC= 'BTC'
    ETH= 'ETH'


class Alt(Currency):
    """
    >>> Alt("XRP")
    XRP
    """
    XRP= 'XRP'


def currency(c: str) -> typing.Optional[Currency]:
    """
    >>> c = currency('EUR')
    >>> type(c)
    <enum 'Fiat'>
    >>> c
    EUR

    >>> c = currency('BTC')
    >>> type(c)
    <enum 'Crypto'>
    >>> c
    BTC

    >>> c = currency('XRP')
    >>> type(c)
    <enum 'Alt'>
    >>> c
    XRP

    """
    if c in Fiat.__members__:
        return getattr(Fiat, c)
    elif c in Crypto.__members__:
        return getattr(Crypto, c)
    elif c in Alt.__members__:
        return getattr(Alt, c)
    else:
        raise CurrencyError



#
#
# @dataclass(frozen=True)
# class Currency:
#     """
#     For clarity:
#
#     >>> Currency.from_str('USD')
#     USD
#
#     But actually just does :
#
#     >>> Currency('USD')
#     USD
#
#     Which should be properly :
#
#     >>> Currency(Fiat.USD)
#     USD
#     """
#     @staticmethod
#     def from_str(s: str) -> Currency:
#         return Currency(code=s)
#
#     code: typing.Union[Fiat, Crypto, Alt]
#
#     def __repr__(self):
#         return str(self.code)


@dataclass(frozen=True)
class Symbol:
    """
    >>> Symbol.from_str("EUR/ETH")
    EUR/ETH
    """
    @staticmethod
    def from_str(s: str) -> typing.Optional[Symbol]:
        try:
            base, quote = s.split("/")
        except ValueError as ve:  # not enough values to unpack
            raise SymbolError(msg="Cannot parse symbol {s}", original =ve)

        try:
            basec = currency(base)
            quotec = currency(quote)
        except Exception as exc:
            raise
        if basec is not None and quotec is not None:
            try:
                s = Symbol(base=basec, quote=quotec)
            except Exception as exc:
                raise
            return s
        else:
            return None

    base: typing.Union[Fiat, Crypto, Alt]
    quote: typing.Union[Fiat, Crypto, Alt]

    def __repr__(self):
        return f"{self.base}/{self.quote}"


if __name__ == "__main__":
    import pytest
    pytest.main(['-s', '--doctest-modules', '--doctest-continue-on-failure', __file__])


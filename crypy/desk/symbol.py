#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import typing
from enum import Enum

from pydantic.dataclasses import dataclass
try:
    from .errors import CrypyException
except (ImportError, ValueError):
    from crypy.desk.errors import CrypyException


class SymbolError(CrypyException):
    pass


# Enums to store accepted currencies.
# Unknown currencies will be ignored by pydantic
Fiat = Enum("Fiat", "EUR USD CAD")
Crypto = Enum("Crypto", "ETH BTC")
Alt = Enum("Alt", "XRP")


@dataclass(frozen=True)
class Currency:

    @staticmethod
    def from_str(s: str) -> Currency:
        return Currency(code=s)

    code: typing.Union[Fiat, Crypto, Alt]

    def __repr__(self):
        return str(self.code)


@dataclass(frozen=True)
class Symbol:

    @staticmethod
    def from_str(s: str) -> Symbol:
        try:
            base, quote = s.split("/")
        except ValueError as ve:  # not enough values to unpack
            raise SymbolError(msg="Cannot parse symbol {s}", original =ve)
        return Symbol(Currency(base), Currency(quote))

    base: Currency
    quote: Currency

    def __repr__(self):
        return f"{self.base}/{self.quote}"


if __name__ == "__main__":

    s = Symbol.from_str("EUR/ETH")
    assert type(s) is Symbol
    print(s.base)
    assert type(s.base) is Currency and s.base == Currency("EUR")
    print(s.quote)
    assert type(s.quote) is Currency and s.quote == Currency("ETH")
    print(s)

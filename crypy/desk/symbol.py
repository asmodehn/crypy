#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Currency:
    code: str

    def __repr__(self):
        return self.code


@dataclass(frozen=True)
class Symbol:
    base: Currency
    quote: Currency

    def __repr__(self):
        return f"{self.base}/{self.quote}"


def symbol(s: str):
    base, quote = s.split("/")
    return Symbol(Currency(base), Currency(quote))


if __name__ == "__main__":

    s = symbol("EUR/ETH")
    assert type(s) is Symbol
    print(s.base)
    assert type(s.base) is Currency and s.base == Currency("EUR")
    print(s.quote)
    assert type(s.quote) is Currency and s.quote == Currency("ETH")
    print(s)

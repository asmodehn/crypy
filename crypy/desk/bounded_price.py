#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

from pydantic import validator
from pydantic.dataclasses import dataclass
from dataclasses import field
import typing

# TODO : this can be made generic by parametrizing on the type float
# TODO : optimized interval logic ?


# Ref : https://en.wikipedia.org/wiki/Interval_arithmetic

# Ref : http://mpmath.org/
# TODO : from bounds. to be used in multiple places....

# Ref : http://mpmath.org/

try:
    from ..euc import mpmath
    from .errors import CrypyException
except (ImportError, ValueError):
    from crypy.euc import mpmath
    from crypy.desk.errors import CrypyException


class PydanticConfig:
    arbitrary_types_allowed = True


class BoundedPriceError(CrypyException):
    pass


@dataclass(frozen=True, config=PydanticConfig)
class BoundedPrice:
    """
    Class representing a price, bounded in an interval
    """
    value: mpmath.mp.mpf
    # delegating implementation to mpmath
    bounds: mpmath.iv.mpf

    # Currently ignored by pydantic
    # @validator('value')
    # def value_init(self, v: float):
    #     return mpmath.mp.mpf(v)
    #
    # @validator('bounds')
    # def bounds_init(self, i: typing.Iterable):
    #     TODO : if None : basic error to have same as init
    #     return mpmath.iv.mpf(i)

    def __init__(self, value: float, bounds: typing.Optional[typing.Iterable[float]] = None):

        if bounds is None:
            # using value as bounds. semantic of a value with minimal error
            object.__setattr__(self, 'bounds', mpmath.iv.mpf(str(value)))
        else:
            object.__setattr__(self, 'bounds', mpmath.iv.mpf(bounds))

        object.__setattr__(self, 'value', mpmath.mp.mpf(value))

    def __post_init__(self):
        # checking bounds right after init, to except early.
        self()

    def __call__(self) -> mpmath.mp.mpf:
        """
        Calling this instance verify the bounds and return the actual value
        :return:
        """
        try:
            self.value in self.bounds
        except Exception as exc:
            raise BoundedPriceError("Price value not inside bounds", original=exc)
        return self.value


if __name__ == "__main__":
    p = BoundedPrice(value=34.56, bounds=[33.5, 35.7])
    assert type(p) is BoundedPrice
    print(p)


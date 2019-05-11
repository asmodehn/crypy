#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import pydantic
import typing
import hypothesis
import hypothesis.strategies

# Ref : https://en.wikipedia.org/wiki/Interval_arithmetic

# Ref : http://mpmath.org/

try:
    from ...euc import mpmath
    from ..errors import CrypyException
except (ImportError, ValueError):
    from crypy.euc import mpmath
    from crypy.desk.errors import CrypyException


"""
Module providing an interface to mpmath, allowing it to work with pydantic for runtime type enforcement.
Note the dataclasses here are pure python dataclasses.
pydantic is not involved in the type enforcement at this level.
"""


class MPFloatException(CrypyException):
    pass


class MPFloat(mpmath.mpf):
    """
    A Basic Multiprecision float (in the mpmath sense)
    """

    @staticmethod
    def strategy(
        min_value: float = None,
        max_value: float = None,
        exclude_min: bool = False,
        exclude_max=False,
        allow_infinity=False,
    ):
        return hypothesis.strategies.builds(
            MPFloat,
            hypothesis.strategies.floats(
                allow_nan=False,
                min_value=min_value,
                max_value=max_value,
                exclude_min=exclude_min,
                exclude_max=exclude_max,
                allow_infinity=allow_infinity,  # careful https://github.com/HypothesisWorks/hypothesis/issues/1859
            ),
        )

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return mpmath.mpf(v)
        except Exception as exc:
            raise MPFloatException(original=exc)


class MPFuzzyFloatException(CrypyException):
    pass


class MPFuzzyFloat(mpmath.mpf):
    """
    A Fuzzy Float, ie, a float that is somewhere in an interval,
    and this interval is managed during arithmetic computation.
    """

    @staticmethod
    def strategy(
        min_value: float = None,
        max_value: float = None,
        exclude_min: bool = False,
        exclude_max=False,
        allow_infinity=False,
    ):
        return hypothesis.strategies.builds(
            MPFloat,
            hypothesis.strategies.floats(
                allow_nan=False,
                min_value=min_value,
                max_value=max_value,
                exclude_min=exclude_min,
                exclude_max=exclude_max,
                allow_infinity=allow_infinity,  # careful https://github.com/HypothesisWorks/hypothesis/issues/1859
            ),
        )

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: float):
        try:
            return mpmath.iv.mpf(str(v))
        except Exception as exc:
            raise MPFuzzyFloatException(original=exc)


class MPIntervalException(CrypyException):
    pass


class MPInterval(mpmath.iv.mpf):
    """
    An interval on the float line. No infinite bounds.
    """

    @staticmethod
    @hypothesis.strategies.composite
    def strategy(draw):
        low_bound = draw(hypothesis.strategies.floats(allow_nan=False))
        high_bound = draw(
            hypothesis.strategies.floats(allow_nan=False, min_value=low_bound)
        )
        return MPInterval(mpmath.mpi(low_bound, high_bound))

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, b: typing.Union[typing.List[float], mpmath.iv.mpf]):
        """enforce needing a pair to define an interval"""
        try:
            if isinstance(b, list):
                # assert b[0] <= b[1]  # TODO : can interval be inverted (inverting the meaning of being "in" to "out") ??
                return mpmath.mpi(b[0], b[1])
            elif isinstance(b, mpmath.iv.mpf):
                # assert b.a <= b.b  # TODO : can interval be inverted (inverting the meaning of being "in" to "out") ??
                return b
            else:
                raise MPIntervalException(f"Cannot validate {b}")
        except Exception as exc:
            raise MPIntervalException(original=exc)



class MPBoundedFloatException(CrypyException):
    pass


@pydantic.dataclasses.dataclass(frozen=True)
class MPBoundedFloat:
    """
    Class representing an amount, bounded in an interval
    >>> MPBoundedFloat(value=34.56, bounds=[33.5, 35.7])
    BoundedAmount(value=mpf('34.560000000000002'), bounds=mpi('33.5', '35.700000000000003'))
    """

    @staticmethod
    @hypothesis.strategies.composite
    def strategy(draw):
        b = draw(MPInterval.strategy())
        hypothesis.assume(b.a != -float("inf"))
        hypothesis.assume(b.b != float("inf"))
        v = draw(MPFloat.strategy(min_value=float(b.a), max_value=float(b.b)))
        return MPBoundedFloat(value=v, bounds=b)

    value: MPFloat
    # delegating implementation to mpmath
    bounds: MPInterval

    def __post_init__(self):
        # checking bounds right after init, to except early.
        self()

    def __call__(self) -> MPFloat:
        """
        Calling this instance verify the bounds and return the actual value
        :return:
        """
        if not self.value in self.bounds:
            raise MPBoundedFloatException("Price value not inside bounds")

        # TMP just in case mpmath lets us down
        assert self.value >= self.bounds.a
        assert self.value <= self.bounds.b

        return self.value


class MPBoundedFuzzyFloatException(CrypyException):
    pass


@pydantic.dataclasses.dataclass(frozen=True)
class MPBoundedFuzzyFloat:
    """
    Class representing an amount, bounded in an interval
    >>> MPBoundedFuzzyFloat(value=34.56, bounds=[33.5, 35.7])
    MPBoundedFuzzyFloat(value=mpf('34.560000000000002'), bounds=mpi('33.5', '35.700000000000003'))
    """

    @staticmethod
    @hypothesis.strategies.composite
    def strategy(draw):
        b = draw(MPInterval.strategy())
        hypothesis.assume(b.a != -float("inf"))
        hypothesis.assume(b.b != float("inf"))
        v = draw(MPFloat.strategy(min_value=float(b.a), max_value=float(b.b)))
        return MPBoundedFloat(value=v, bounds=b)

    value: MPFuzzyFloat
    # delegating implementation to mpmath
    bounds: MPInterval

    def __post_init__(self):
        # checking bounds right after init, to except early.
        self()

    def __call__(self) -> MPFloat:
        """
        Calling this instance verify the bounds and return the actual value
        :return:
        """
        if not self.value in self.bounds:
            raise MPBoundedFuzzyFloatException("Float value not inside bounds")

        # TMP just in case mpmath lets us down
        assert self.value >= self.bounds.a
        assert self.value <= self.bounds.b

        return self.value


# extra utils
isfinite = mpmath.isfinite
isinf = mpmath.isinf
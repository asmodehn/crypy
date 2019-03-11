#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

from pydantic.dataclasses import dataclass
import hypothesis.strategies

try:
    from .impl.mpmath import MPFloat, MPInterval
    from .errors import CrypyException
except (ImportError, ValueError):
    from crypy.desk.impl.mpmath import MPFloat, MPInterval
    from crypy.desk.errors import CrypyException


class PydanticConfig:
    pass
    # arbitrary_types_allowed = True


class BoundedAmountError(CrypyException):
    pass


@dataclass(frozen=True, config=PydanticConfig)
class BoundedAmount:
    """
    Class representing an amount, bounded in an interval
    >>> BoundedAmount(value=34.56, bounds=[33.5, 35.7])
    BoundedAmount(value=mpf('34.560000000000002'), bounds=mpi('33.5', '35.700000000000003'))
    """

    @staticmethod
    @hypothesis.strategies.composite
    def strategy(draw):
        b = draw(MPInterval.strategy())
        hypothesis.assume(b.a != -float("inf"))
        hypothesis.assume(b.b != float("inf"))
        v = draw(MPFloat.strategy(min_value=float(b.a), max_value=float(b.b)))
        return BoundedAmount(value=v, bounds=b)

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
            raise BoundedAmountError("Price value not inside bounds")

        # TMP just in case mpmath lets us down
        assert self.value >= self.bounds.a
        assert self.value <= self.bounds.b

        return self.value


if __name__ == "__main__":
    import pytest
    pytest.main(['-s', '--doctest-modules', '--doctest-continue-on-failure', __file__])

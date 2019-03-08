#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import pytest
from pydantic import validator
from pydantic.dataclasses import dataclass
from dataclasses import field
import typing
from hypothesis import given, settings, Verbosity, infer
from hypothesis.strategies import integers, floats, builds, lists, composite

from ..mpmath import Exact, Interval


@dataclass(frozen=True)
class ExactDC:
    """
    Class representing a price, bounded in an interval
    """

    value: Exact


@dataclass(frozen=True)
class IntervalDC:
    """
    Class representing a price, bounded in an interval
    """

    value: Interval


@given(val=infer)
def test_exact(val: float):
    e = Exact(val)

    # TODO : test more stuff (equality, comprators, arithmetic...)


@composite
def low_high(draw):
    low = draw(floats(allow_nan=False, allow_infinity=True))
    high = draw(floats(min_value=low, allow_nan=False, allow_infinity=True))

    return low, high


@given(b=low_high())
def test_interval(b: typing.Tuple[float]):
    i = IntervalDC(b)
    # TODO : test more stuff (equality, comprators, arithmetic...)


if __name__ == "__main__":
    pytest.main(["-s", __file__])

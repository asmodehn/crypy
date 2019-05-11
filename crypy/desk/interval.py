#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass, field
import typing


# Ref : https://en.wikipedia.org/wiki/Interval_arithmetic

# Ref : http://mpmath.org/
import mpmath


@dataclass(frozen=True, eq=True, order=False)
class Interval:
    """
    Class representing an interval, supporting interval arithmetic.
    """
    # delegating implementation to mpmath
    impl: mpmath.iv.mpf = field(init=False)

    @staticmethod
    def from_mpmath(mpiv: mpmath.iv.mpf)-> Interval:
        return Interval(mpiv.a, mpiv.b)

    def __init__(self, lower: float, upper: float):
        # Note : we rely on mpmath for validation here.
        if upper < lower:
            # implementation by delegation to specialized library
            object.__setattr__(self, 'impl', mpmath.iv.mpf((upper, lower)))
        else:
            # implementation by delegation to specialized library
            object.__setattr__(self, 'impl', mpmath.iv.mpf((lower, upper)))

        mpmath.iv.pretty = True

    def __repr__(self):
        return repr(self.impl)

    def __eq__(self, other):
        return mpmath.iv.almosteq(self.impl, other.impl)

    def __add__(self, other):
        return Interval.from_mpmath(mpmath.iv.fadd(self.impl, other.impl))

    def __sub__(self, other):
        return Interval.from_mpmath(mpmath.iv.fsub(self.impl, other.impl))

    def __mul__(self, other):
        return Interval.from_mpmath(mpmath.iv.fmul(self.impl, other.impl))

    def __divmod__(self, other):
        return mpmath.iv.fdiv(self.impl, other.impl), mpmath.iv.fmod(self.impl, other.impl)


if __name__ == "__main__":

    p = Interval(0.3, 0.5)
    assert type(p) is Interval


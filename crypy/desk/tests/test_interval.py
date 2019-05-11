import random

import mpmath
import pydantic
import pytest
from hypothesis import given, settings, Verbosity
from hypothesis.strategies import integers, floats, dictionaries, lists, tuples, sampled_from, builds, composite
from .. import interval


# TODO : bounds as pytest fixture. Pb : how about https://github.com/pytest-dev/pytest/issues/916 ?
# Ref : https://hypothesis.works/articles/hypothesis-pytest-fixtures/


@given(floats(allow_nan=False, allow_infinity=True), floats(allow_nan=False, allow_infinity=True))
@settings(verbosity=Verbosity.verbose)
def test_init(b1: float, b2: float):

    b = interval.Interval(b1, b2)
    assert type(b) is interval.Interval


@composite
def intervals(draw):
    b1 = draw(floats(allow_nan=False, allow_infinity=True))
    b2 = draw(floats(allow_nan=False, allow_infinity=True))
    # interval will reorder the bounds (suitable ?)
    return interval.Interval(b1, b2)


@given(intervals())
@settings(verbosity=Verbosity.verbose)
def test_reflexive_equality(i1):
    assert i1 == i1


@given(intervals(), intervals())
@settings(verbosity=Verbosity.verbose)
def test_symmetric_equality(i1, i2):
    if i1 == i2:
        assert i2 == i1


@given(intervals(), intervals(), intervals())
@settings(verbosity=Verbosity.verbose)
def test_transitive_equality(i1, i2, i3):
    if i1 == i2 and i2 == i3:
        assert i1 == i3


@given(intervals(), intervals())
@settings(verbosity=Verbosity.verbose)
def test_equality(i1, i2):
    eq = (i1 == i2)
    # equals iff bounds are same
    # TODO : another implementation
    assert eq == mpmath.iv.almosteq(i1.impl, i2.impl)


@given(intervals(), intervals())
@settings(verbosity=Verbosity.verbose)
def test_inequality(i1, i2):
    ineq = (i1 != i2)
    # TODO : another implementation
    assert ineq == (not mpmath.iv.almosteq(i1.impl, i2.impl))


@given(intervals(), intervals())
@settings(verbosity=Verbosity.verbose)
def test_add(i1, i2):

    isum = i1 + i2

    # TODO : another implementation
    assert isum == interval.Interval.from_mpmath(mpmath.iv.fadd(i1.impl, i2.impl))


@given(intervals(), intervals())
@settings(verbosity=Verbosity.verbose)
def test_sub(i1, i2):
    isub = i1 - i2

    # TODO : another implementation
    assert isub == interval.Interval.from_mpmath(mpmath.iv.fsub(i1.impl, i2.impl))


@given(intervals(), intervals())
@settings(verbosity=Verbosity.verbose)
def test_mul(i1, i2):
    imul = i1 * i2

    # TODO : another implementation
    assert imul == interval.Interval.from_mpmath(mpmath.iv.fmul(i1.impl, i2.impl))


@given(intervals(), intervals())
@settings(verbosity=Verbosity.verbose)
def test_div(i1, i2):
    idiv = i1 / i2

    # TODO : another implementation
    assert idiv == interval.Interval.from_mpmath(mpmath.iv.fdiv(i1.impl, i2.impl))




@given(intervals(), intervals())
@settings(verbosity=Verbosity.verbose)
def test_mod(i1, i2):
    idiv = i1 % i2

    # TODO : another implementation
    assert idiv == interval.Interval.from_mpmath(mpmath.iv.fmod(i1.impl, i2.impl))






if __name__ == "__main__":
    pytest.main(["-s", __file__])

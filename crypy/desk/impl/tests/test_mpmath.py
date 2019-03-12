#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import sys

import pytest
import typing
from hypothesis import given, settings, Verbosity, assume, HealthCheck
from hypothesis.strategies import composite, floats

from ..mpmath import MPFloat, MPFuzzyFloat, MPInterval, MPBoundedFloat, MPBoundedFloatException,  MPBoundedFuzzyFloat, MPBoundedFuzzyFloatException, isfinite

"""
To Verify MPMath Semantics and wrap it in type(class-e)s that makes sense for us
"""


@given(mpf=MPFloat.strategy())
@settings(verbosity=Verbosity.verbose)
def test_mpfloat_identity_equality(mpf):

    assert mpf is not float(mpf)

    mpf_bis = mpf

    assert mpf_bis is mpf
    assert mpf_bis == mpf

    mpg = MPFloat(float(mpf))

    assert mpg is not mpf
    assert mpg == mpf


@given(mpff=MPFuzzyFloat.strategy())
@settings(verbosity=Verbosity.verbose)
def test_mpfuzzyfloat_identity_equality(mpff):

    assert mpff is not float(mpff)

    mpff_bis = mpff

    assert mpff_bis is mpff
    assert mpff_bis == mpff

    mpfg = MPFuzzyFloat(float(mpff))

    assert mpfg is not mpff
    assert mpfg == mpff


@given(mpij=MPInterval.strategy())
@settings(verbosity=Verbosity.verbose)
def test_mpinterval_identity_equality(mpij):

    mpij_bis = mpij

    assert mpij_bis is mpij
    assert mpij_bis == mpij

    mpjk = MPInterval((mpij.a, mpij.b))

    assert mpjk is not mpij
    assert mpjk == mpij


@given(
    mpf=MPFloat.strategy(),
    val=floats(allow_nan=False, allow_infinity=False),
)
@settings(verbosity=Verbosity.verbose)
def test_mpfloat_add_sub(mpf, val):

    added_raw = mpf + val
    added_mp = mpf + MPFloat(val)

    assert added_raw == added_mp

    sub_raw_raw = added_raw - val

    sub_mp_raw = added_mp - val

    sub_raw_mp = added_raw - MPFloat(val)

    sub_mp_mp = added_mp - MPFloat(val)

    assert sub_raw_raw == sub_mp_raw == sub_raw_mp == sub_mp_mp


@given(
    mpf=MPFuzzyFloat.strategy(),
    val=floats(allow_nan=False, allow_infinity=False),
)
@settings(verbosity=Verbosity.verbose)
def test_mpfuzzyfloat_add_sub(mpf, val):

    added_raw = mpf + val
    added_fuzz = mpf + MPFuzzyFloat(val)

    assert added_raw == added_fuzz

    sub_raw_raw = added_raw - val

    sub_mp_raw = added_fuzz - val

    sub_raw_mp = added_raw - MPFuzzyFloat(val)

    sub_mp_mp = added_fuzz - MPFuzzyFloat(val)

    assert sub_raw_raw == sub_mp_raw == sub_raw_mp == sub_mp_mp


@given(mpia=MPInterval.strategy(), mpib=MPInterval.strategy())
@settings(verbosity=Verbosity.verbose)
def test_mpinterval_add_sub(mpia, mpib):

    added = mpia + mpib

    subbeda = added - mpia

    assert mpib in subbeda

    subbedb = added - mpib

    assert mpia in subbedb


###############################

@given(bp=MPBoundedFloat.strategy())
@settings(verbosity=Verbosity.verbose)
def test_init(bp):
    # it should be a good init bounded value
    assert bp() == bp.value


# Testing equality properties
@given(bp=MPBoundedFloat.strategy())
@settings(verbosity=Verbosity.verbose)
def test_eq_reflx(bp):
    assert bp == bp


@given(
    bp1=MPBoundedFloat.strategy(),
    bp2=MPBoundedFloat.strategy(),
)
@settings(verbosity=Verbosity.verbose)
def test_eq_symm(bp1, bp2):
    if bp1 == bp2:
        assert bp2 == bp1


@given(
    bp1=MPBoundedFloat.strategy(),
    bp2=MPBoundedFloat.strategy(),
    bp3=MPBoundedFloat.strategy(),
)
@settings(verbosity=Verbosity.verbose)
def test_eq_trans(bp1, bp2, bp3):
    if bp1 == bp2 and bp2 == bp3:
        assert bp1 == bp3


@given(bp=MPBoundedFloat.strategy())
@settings(verbosity=Verbosity.verbose)
def test_in_call(bp):
    assert bp() in bp.bounds


# TODO : adjust for https://github.com/HypothesisWorks/hypothesis/issues/1859


@composite
def underbounds(draw,):
    b = draw(MPInterval.strategy())
    assume(isfinite(b.a) and sys.float_info.min < float(b.a) < sys.float_info.max)
    v = draw(
        MPFloat.strategy(
            max_value=float(b.a), exclude_max=True, allow_infinity=False
        )
    )
    return v, b


@composite
def overbounds(draw,):
    b = draw(MPInterval.strategy())
    assume(isfinite(b.b) and sys.float_info.max > float(b.b) > sys.float_info.min)
    v = draw(
        MPFloat.strategy(
            min_value=float(b.b), exclude_min=True, allow_infinity=False
        )
    )
    return v, b


@given(vb=overbounds())
@settings(verbosity=Verbosity.verbose, suppress_health_check=[HealthCheck.too_slow])
def test_overbounds(vb):
    v, b = vb
    with pytest.raises(MPBoundedFloatException):
        bp = MPBoundedFloat(value=v, bounds=b)


@given(vb=underbounds())
@settings(verbosity=Verbosity.verbose, suppress_health_check=[HealthCheck.too_slow])
def test_underbounds(vb):
    v, b = vb
    with pytest.raises(MPBoundedFloatException):
        bp = MPBoundedFloat(value=v, bounds=b)


# TODO : test basic arithmetic with variable precision...


if __name__ == "__main__":
    pytest.main(["-s", __file__])

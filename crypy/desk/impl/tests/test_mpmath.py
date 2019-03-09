#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import pytest
import typing
from hypothesis import given, Verbosity, settings
import hypothesis.strategies

from ..mpmath import MPFloat, MPFuzzyFloat, MPInterval

"""
To Verify MPMath Semantics and wrap it in types that makes sense for us
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
    val=hypothesis.strategies.floats(allow_nan=False, allow_infinity=False),
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
    val=hypothesis.strategies.floats(allow_nan=False, allow_infinity=False),
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


if __name__ == "__main__":
    pytest.main(["-s", __file__])

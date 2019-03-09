import typing

import pytest
from hypothesis import given, settings, Verbosity, infer, assume
from hypothesis.strategies import integers, floats, builds, lists, composite, one_of

from .. import bounded_price


@composite
def out_of_bounds(draw,):
    b = draw(bounded_price.MPInterval.strategy())
    # invert bound to generate value outside of bounds
    valid_strats = []
    assume(b.a != -float('inf'))
    valid_strats.append(bounded_price.MPFloat.strategy(max_value=float(b.a), exclude_max=True))
    assume(b.b != float('inf'))
    valid_strats.append(bounded_price.MPFloat.strategy(min_value=float(b.b), exclude_min=True))
    v = draw(one_of(valid_strats))
    return v, b


@given(oob=out_of_bounds())
@settings(verbosity=Verbosity.verbose)
def test_bad_init(oob):
    v, b = oob
    with pytest.raises(bounded_price.BoundedPriceError):
        bounded_price.BoundedPrice(value=v, bounds=b)


@given(bp=bounded_price.BoundedPrice.strategy())
@settings(verbosity=Verbosity.verbose)
def test_init(bp):
    # it should be a good init bounded value
    assert bp() == bp.value


# Testing equality properties
@given(bp=bounded_price.BoundedPrice.strategy())
def bp_eq_reflx(bp):
    assert bp == bp


@given(bp1=bounded_price.BoundedPrice.strategy(), bp2=bounded_price.BoundedPrice.strategy())
def bp_eq_symm(bp1, bp2):
    if bp1 == bp2:
        assert bp2 == bp1


@given(bp1=bounded_price.BoundedPrice.strategy(), bp2=bounded_price.BoundedPrice.strategy(), bp3=bounded_price.BoundedPrice.strategy())
def bp_eq_trans(bp1, bp2, bp3):
    if bp1 == bp2 and bp2 == bp3:
        assert bp1 == bp3


if __name__ == "__main__":
    pytest.main(["-s", __file__])

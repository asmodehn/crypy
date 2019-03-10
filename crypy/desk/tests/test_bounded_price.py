import typing

import pytest
from hypothesis import given, settings, Verbosity, infer, assume
from hypothesis.strategies import integers, floats, builds, lists, composite, one_of

from mpmath import isinf
from .. import bounded_price

# TODO : adjust for https://github.com/HypothesisWorks/hypothesis/issues/1859


@composite
def underbounds(draw,):
    b = draw(bounded_price.MPInterval.strategy())
    # TMP if infinite, need to allow infinite in strategy.
    inf = isinf(b.a) or isinf(b.a)
    v = draw(bounded_price.MPFloat.strategy(max_value=float(b.a), exclude_max=True, allow_infinity=inf))
    return v, b


@composite
def overbounds(draw,):
    b = draw(bounded_price.MPInterval.strategy())
    # TMP if infinite, need to allow infinite in strategy.
    inf = isinf(b.b) or isinf(b.b)
    v = draw(bounded_price.MPFloat.strategy(min_value=float(b.b), exclude_min=True, allow_infinity=inf))
    return v, b


@given(vb=overbounds())
@settings(verbosity=Verbosity.verbose)
def test_overbounds(vb):
    v, b = vb
    with pytest.raises(bounded_price.BoundedPriceError):
        bp = bounded_price.BoundedPrice(value=v, bounds=b)
        # WARNING : pydantic dataclass doesnt call post_init ?
        bp()


@given(vb=underbounds())
@settings(verbosity=Verbosity.verbose)
def test_underbounds(vb):
    v, b = vb
    with pytest.raises(bounded_price.BoundedPriceError):
        bp = bounded_price.BoundedPrice(value=v, bounds=b)
        # WARNING : pydantic dataclass doesnt call post_init ?
        bp()


@given(bp=bounded_price.BoundedPrice.strategy())
@settings(verbosity=Verbosity.verbose)
def test_init(bp):
    # it should be a good init bounded value
    assert bp() == bp.value


# Testing equality properties
@given(bp=bounded_price.BoundedPrice.strategy())
@settings(verbosity=Verbosity.verbose)
def test_eq_reflx(bp):
    assert bp == bp


@given(
    bp1=bounded_price.BoundedPrice.strategy(), bp2=bounded_price.BoundedPrice.strategy()
)
@settings(verbosity=Verbosity.verbose)
def test_eq_symm(bp1, bp2):
    if bp1 == bp2:
        assert bp2 == bp1


@given(
    bp1=bounded_price.BoundedPrice.strategy(),
    bp2=bounded_price.BoundedPrice.strategy(),
    bp3=bounded_price.BoundedPrice.strategy(),
)
@settings(verbosity=Verbosity.verbose)
def test_eq_trans(bp1, bp2, bp3):
    if bp1 == bp2 and bp2 == bp3:
        assert bp1 == bp3


@given(bp=bounded_price.BoundedPrice.strategy())
@settings(verbosity=Verbosity.verbose)
def test_in_call(bp):
    assert bp() in bp.bounds


if __name__ == "__main__":
    pytest.main(["-s", __file__])

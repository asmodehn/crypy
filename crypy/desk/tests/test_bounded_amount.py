import typing

import pytest
from hypothesis import given, settings, Verbosity, infer, assume, HealthCheck
from hypothesis.strategies import integers, floats, builds, lists, composite, one_of

from mpmath import isinf
from .. import bounded_amount

# TODO : adjust for https://github.com/HypothesisWorks/hypothesis/issues/1859


@composite
def underbounds(draw,):
    b = draw(bounded_amount.MPInterval.strategy())
    # TMP if infinite, need to allow infinite in strategy.
    assume(not isinf(b.a))
    v = draw(bounded_amount.MPFloat.strategy(max_value=float(b.a), exclude_max=True, allow_infinity=False))
    return v, b


@composite
def overbounds(draw,):
    b = draw(bounded_amount.MPInterval.strategy())
    # TMP if infinite, need to allow infinite in strategy.
    assume(not isinf(b.b))
    v = draw(bounded_amount.MPFloat.strategy(min_value=float(b.b), exclude_min=True, allow_infinity=False))
    return v, b


@given(vb=overbounds())
@settings(verbosity=Verbosity.verbose, suppress_health_check=[HealthCheck.too_slow])
def test_overbounds(vb):
    v, b = vb
    with pytest.raises(bounded_amount.BoundedAmountError):
        bp = bounded_amount.BoundedAmount(value=v, bounds=b)
        # WARNING : pydantic dataclass doesnt call post_init ?
        bp()


@given(vb=underbounds())
@settings(verbosity=Verbosity.verbose, suppress_health_check=[HealthCheck.too_slow])
def test_underbounds(vb):
    v, b = vb
    with pytest.raises(bounded_amount.BoundedAmountError):
        bp = bounded_amount.BoundedAmount(value=v, bounds=b)
        # WARNING : pydantic dataclass doesnt call post_init ?
        bp()


@given(bp=bounded_amount.BoundedAmount.strategy())
@settings(verbosity=Verbosity.verbose)
def test_init(bp):
    # it should be a good init bounded value
    assert bp() == bp.value


# Testing equality properties
@given(bp=bounded_amount.BoundedAmount.strategy())
@settings(verbosity=Verbosity.verbose)
def test_eq_reflx(bp):
    assert bp == bp


@given(
    bp1=bounded_amount.BoundedAmount.strategy(), bp2=bounded_amount.BoundedAmount.strategy()
)
@settings(verbosity=Verbosity.verbose)
def test_eq_symm(bp1, bp2):
    if bp1 == bp2:
        assert bp2 == bp1


@given(
    bp1=bounded_amount.BoundedAmount.strategy(),
    bp2=bounded_amount.BoundedAmount.strategy(),
    bp3=bounded_amount.BoundedAmount.strategy(),
)
@settings(verbosity=Verbosity.verbose)
def test_eq_trans(bp1, bp2, bp3):
    if bp1 == bp2 and bp2 == bp3:
        assert bp1 == bp3


@given(bp=bounded_amount.BoundedAmount.strategy())
@settings(verbosity=Verbosity.verbose)
def test_in_call(bp):
    assert bp() in bp.bounds


if __name__ == "__main__":
    pytest.main(["-s", __file__])

import random

import pydantic
import pytest
from hypothesis import given, settings, Verbosity
from hypothesis.strategies import integers, floats, builds
from .. import bounds


# TODO : bound as pytest fixture

@given(floats(allow_nan=False, allow_infinity=False), floats(allow_nan=False, allow_infinity=False))
@settings(verbosity=Verbosity.verbose)
def test_bounds(b1: float, b2: float):


    # test wrong bounds
    # TODO : should work implicitly or not ?
    if b1 < b2:

        with pytest.raises(AssertionError):
            wb = bounds.Bounds(lower= b2, upper=b1)
    elif b1 > b2:

        with pytest.raises(AssertionError):
            wb = bounds.Bounds(lower= b1, upper=b2)


    # correct use
    if b1 < b2:
        gb = bounds.Bounds(lower = b1, upper = b2)

    else:
        gb = bounds.Bounds(lower = b2, upper=b1)


    # test call
    went_over = 0
    went_under = 0

    def signal_over(v,b):
        nonlocal went_over
        went_over += 1

    def signal_under(v,b):
        nonlocal went_under
        went_under += 1

    try :
        good_value = random.randrange(gb.lower, gb.upper)

        gb(good_value, on_over=signal_over, on_under=signal_under)

        assert went_over == went_under == 0
    except ValueError:
        pass # on empty range

    # QUICK HACK
    eps = .000001

    lower_value = gb.lower - eps - random.random() * (gb.upper - gb.lower)

    gb(lower_value, on_over=signal_over, on_under=signal_under)

    if lower_value < gb.lower:
        assert went_under == 1, f"{lower_value} went under {gb.lower} undetected"

    assert went_over == 0

    over_value = gb.upper + eps + random.random() * (gb.upper - gb.lower)

    gb(over_value, on_over=signal_over, on_under=signal_under)

    if over_value > gb.upper:
        assert went_over == 1, f"{over_value} went over {gb.upper} undetected"




if __name__ == "__main__":
    pytest.main(["-s", __file__])

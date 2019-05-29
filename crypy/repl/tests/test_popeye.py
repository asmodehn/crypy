from hypothesis.strategies import integers
from hypothesis import given


@given(v=integers(), t=int)
def test_basetype_membership(v, t):
    assert v in t


def test_uniontype_membership(v, t):
    assert v in t


def test_producttype_membership(v, t):
    assert v in t


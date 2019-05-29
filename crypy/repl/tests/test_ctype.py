from hypothesis.strategies import integers
from hypothesis import given


@given(v=integers(), t=int)
def test_type_membership(v, t):
    assert v in t


@given()
def test_value_equality(v1, v2, t):
    assert v1 in t and v2 in t and v1 == v2


@given(t1, t2)
def test_typevalue_equality(t1, t2):
    for v in t1:
        assert v in t2

    for v in t2:
        assert v in t1



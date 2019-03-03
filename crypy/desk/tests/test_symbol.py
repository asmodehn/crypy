import pydantic
import pytest
from hypothesis import given
from hypothesis.strategies import sampled_from
from .. import symbol


@given(sampled_from(symbol.Fiat))
def test_fiat_currency(code: str):

    c1 = symbol.Currency.from_str(code)

    c2 = symbol.Currency(code=code)

    assert str(c1) == str(code) == str(c2)
    assert repr(c1) == repr(c2)
    assert c1 == c2
    # careful
    assert c1 is not c2


@given(sampled_from(symbol.Crypto))
def test_crypto_currency(code: str):

    c1 = symbol.Currency.from_str(code)

    c2 = symbol.Currency(code=code)

    assert str(c1) == str(code) == str(c2)
    assert repr(c1) == repr(c2)
    assert c1 == c2
    # careful
    assert c1 is not c2


@given(sampled_from(symbol.Alt))
def test_alt_currency(code: str):

    c1 = symbol.Currency.from_str(code)

    c2 = symbol.Currency(code=code)

    assert str(c1) == str(code) == str(c2)
    assert repr(c1) == repr(c2)
    assert c1 == c2
    # careful
    assert c1 is not c2


@given(sampled_from(["RAND" "str" "code"]))
def test_unknown_currency(code: str):

    # Using unknown currency will trigger error
    with pytest.raises(pydantic.error_wrappers.ValidationError):
        symbol.Currency.from_str(code)

    with pytest.raises(pydantic.error_wrappers.ValidationError):
        symbol.Currency(code=code)



# TODO : symbol test
# def test_symbol(base, quote):
#     pass


# s = Symbol.from_str("EUR/ETH")
# assert type(s) is Symbol
# print(s.base)
# assert type(s.base) is Currency and s.base == Currency("EUR")
# print(s.quote)
# assert type(s.quote) is Currency and s.quote == Currency("ETH")
# print(s)


if __name__ == "__main__":
    pytest.main(["-s", __file__])

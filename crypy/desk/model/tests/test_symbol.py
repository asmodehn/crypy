import pydantic
import pytest
from hypothesis import given, settings, Verbosity
from hypothesis.strategies import sampled_from
from desk.model import symbol


@given(sampled_from(symbol.Fiat))
@settings(verbosity=Verbosity.verbose) #, suppress_health_check=[HealthCheck.too_slow])
def test_fiat_currency(code: symbol.Fiat):

    cur = symbol.currency(str(code))

    assert str(code) == str(cur)
    assert repr(code) == repr(cur)
    assert code == cur
    assert code is cur


@given(sampled_from(symbol.Crypto))
def test_crypto_currency(code: symbol.Crypto):

    cur = symbol.currency(str(code))

    assert str(cur) == str(code)
    assert repr(cur) == repr(code)
    assert cur == code
    assert cur is code


@given(sampled_from(symbol.Alt))
def test_alt_currency(code: symbol.Alt):

    cur = symbol.currency(str(code))

    assert str(cur) == str(code)
    assert repr(cur) == repr(code)
    assert cur == code
    assert cur is code


@given(sampled_from(["RAND", "str", "code"]))
def test_unknown_currency(code: str):

    # Using unknown currency will trigger error
    with pytest.raises(symbol.CurrencyError):
        symbol.currency(str(code))




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

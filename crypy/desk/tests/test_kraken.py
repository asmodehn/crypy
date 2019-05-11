import pytest

from .. import errors

# TODO : test authentication in config is optional

# TODO : test many possible configuration


def test_markets(kraken_exchange):
    m = kraken_exchange.markets
    assert len(m) > 0  # assert that we actually loaded some market data


@pytest.mark.skip
def test_fetch_balance(kraken_exchange):
    with pytest.raises(errors.AuthenticationError) as excinfo:
        kraken_exchange.fetch_balance()

    # Test that we can dynamically authenticate (with the same exchange instance)
    # by reading the configuration and authenticating.
    from ... import config
    exc = excinfo.value
    b = exc({"apiKey": config.config(config.locate()).get("apiKey"),
         "secret": config.config(config.locate()).get("secret"),
    })

    assert b


#@pytest.mark.skip
def test_fetch_balance_directly(kraken_exchange_auth):
    kraken_exchange_auth.fetch_balance()





if __name__ == '__main__':
    pytest.main(['-s', __file__])
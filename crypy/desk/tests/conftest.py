import pytest

from .. import kraken

from ... import config


@pytest.fixture(scope="module")
def kraken_exchange():
    """Fixture to test with authentication."""
    k = kraken.Kraken(conf={"verbose": True})
    return k


@pytest.fixture(scope="module")
def kraken_exchange_auth():
    """Fixture to test with authentication.
    Careful here, don't spam the exchange..."""
    kakonfg = dict(config.configure().get('kraken.com'))
    k = kraken.Kraken(conf={
        "apiKey": kakonfg.get("apiKey",),
        "secret": kakonfg.get("secret"),
        "verbose": True
    })
    return k

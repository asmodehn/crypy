import pytest

from crypy.exchange import Exchange, Bad


@pytest.fixture()
def exchange():
    """An exchange with pathological behavior for testing purposes"""
    return Exchange(Bad)

@pytest.fixture
def supervisor(exchange):
    return Supervisor(exchange)


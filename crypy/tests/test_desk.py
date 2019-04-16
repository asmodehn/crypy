import dataclasses
import unittest

# https://docs.python.org/3/library/unittest.mock.html
# https://docs.pytest.org/en/latest/unittest.html
from parameterized import parameterized

import crypy.desk.global_vars as gv  # TODO Validate it first
from crypy.desk.desk import Desk  # TODO Validate it first
from crypy.desk.order import Order
from crypy.config import resolve, ExchangeSection

"""
Module testing the whole desk sub package, in integration with ccxt and the actual exchange.
"""


params = [
    # ("Default Config - Public", ExchangeSection(credentials_file='')),
    (
        "Default Config - Private",
        ExchangeSection(
            name="testnet.bitmex",
            credentials_file=resolve("testnet.bitmex.key"),
            enableRateLimit=True,
            impl_hook="impl= ccxt.bitmex(config); impl.urls['api'] = impl.urls['test']",
        ),
    )
]


class TestDesk(unittest.TestCase):
    def test_markets(self):
        for msg, exchange_section in params:
            with self.subTest(msg=msg, exchange_section=None):
                # Hack to build a fake config around the exchange we are interested in
                # TODO : cleanup desk !

                desk = Desk(conf=exchange_section)

                assert desk.markets

    def test_balance(self):
        for msg, exchange_section in params:
            with self.subTest(msg=msg, exchange_section=None):
                # Hack to build a fake config around the exchange we are interested in
                # TODO : cleanup desk !

                desk = Desk(conf=exchange_section)

                assert desk.balance


if __name__ == '__main__':
    import pytest
    pytest.main(['-s', __file__])

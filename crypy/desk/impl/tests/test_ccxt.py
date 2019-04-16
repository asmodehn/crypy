import unittest
# https://docs.python.org/3/library/unittest.mock.html
# https://docs.pytest.org/en/latest/unittest.html

from crypy.config import resolve, ExchangeSection

from crypy.desk.impl import ccxt

params = [
    ("Kraken - Public", ExchangeSection(
        name="kraken",
        credentials_file=None,
        enableRateLimit= True,  # avoid hammering the exchange
        impl_hook="impl= ccxt.kraken(config)",
    ),[
            'createMarketOrder',
            'createOrder',
            'editOrder',
            'cancelOrder',
            'fetchL2OrderBook'
        ] ),

    ("Bitmex - Public", ExchangeSection(
        name="bitmex",
        credentials_file=None,
        enableRateLimit= True,  # avoid hammering the exchange
        impl_hook="impl= ccxt.bitmex(config)",
    ),[
            'createMarketOrder',
            'createOrder',
            'editOrder',
            'privatePostPositionLeverage',
            'cancelOrder',
            'fetchL2OrderBook'
        ]),

    ("Bitmex TestNet - Public", ExchangeSection(
        name="testnet.bitmex",
        credentials_file=None,
        enableRateLimit= True,  # avoid hammering the exchange
        impl_hook="impl= ccxt.bitmex(config); impl.urls['api'] = impl.urls['test']",
    ), [
            'createMarketOrder',
            'createOrder',
            'editOrder',
            'privatePostPositionLeverage',
            'cancelOrder',
            'fetchL2OrderBook'
        ]),
]


class TestCCXT(unittest.TestCase):
    def test_exchange_methods(self):
        for msg, exchange_section, needed_methods in params:
            with self.subTest(msg = msg, exchange_section = exchange_section, needed_methods=needed_methods):
                self.exchange = exchange_section.exec_hook(ccxt=ccxt)

                for ccxtMethod in needed_methods:
                    if ccxtMethod not in self.exchange.has or not self.exchange.has[ccxtMethod]:  # ccxt unified method check
                        if not hasattr(self.exchange, ccxtMethod):  # ccxt implicit (not unified) method check
                            self.fail(msg=f'{ccxtMethod}() not available for exchange {self.exchange.name}')


if __name__ == "__main__":
    unittest.main()

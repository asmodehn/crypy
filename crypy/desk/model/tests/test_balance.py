import unittest

from crypy.desk.model.balance import Balance, BalanceAll, Currency


class TestBalanceAll(unittest.TestCase):
    class TestCrypto(Currency):
        TC1 = 1
        TC2 = 2
        TC3 = 3

    def test_per_currency(self):
        b = BalanceAll(
            free={TestBalanceAll.TestCrypto.TC1: 42.0},
            used={TestBalanceAll.TestCrypto.TC1: 51.0},
            total={TestBalanceAll.TestCrypto.TC1: 93.0},
        )

        assert b.per_currency(currency_list=[TestBalanceAll.TestCrypto.TC1]) == {
            TestBalanceAll.TestCrypto.TC1: Balance(free=42.0, used=51.0, total=93.0)
        }


if __name__ == "__main__":
    unittest.main()

import unittest
from hypothesis import given, settings, Verbosity
from hypothesis.strategies import sampled_from
from crypy.desk.model import symbol

from .. import order


class TestOrderSide(unittest.TestCase):

    def test_buy(self):
        assert order.OrderSide.buy == order.OrderSide('buy')
        assert str(order.OrderSide.buy) == 'buy'

    def test_sell(self):

        assert order.OrderSide.sell == order.OrderSide('sell')
        assert str(order.OrderSide.sell) == 'sell'


class TestOrderStatus(unittest.TestCase):

    def test_open(self):
        assert order.OrderStatus.open == order.OrderStatus('open')
        assert str(order.OrderStatus.open) == 'open'

    def test_closed(self):
        assert order.OrderStatus.closed == order.OrderStatus('closed')
        assert str(order.OrderStatus.closed) == 'closed'


class TestOrderType(unittest.TestCase):

    def test_market(self):
        assert order.OrderType.market == order.OrderType('market')
        assert str(order.OrderType.market) == 'market'

    def test_limit(self):
        assert order.OrderType.limit == order.OrderType('limit')
        assert str(order.OrderType.limit) == 'limit'



class TestOrder(unittest.TestCase):
    # TODO : make sure consistency is checked on raw data before building the dataclass...

    def test_id(self):
        pass

    def test_timestamp(self):
        #TODO : enforce consistency of timestamps
        pass

    def test_symbol(self):
        pass

    def test_side(self):
        pass

    def test_price(self):
        pass

    def test_amount(self):
        pass

    def test_cost(self):
        pass

    def test_filled(self):
        pass

    def test_remaining(self):
        pass

    def test_type(self):
        pass

    def test_status(self):
        pass

    def test_fee(self):
        pass


if __name__ == "__main__":
    unittest.main()
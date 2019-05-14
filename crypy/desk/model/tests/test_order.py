import unittest

from dataclasses import asdict
import pydantic
import pydantic.dataclasses as dataclasses

from hypothesis import given, settings, Verbosity
from hypothesis.strategies import sampled_from, integers

import uuid
import datetime

try:
    from .. import order, symbol
except ImportError:
    from crypy.desk.model import order, symbol


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

    basic_valid = order.Order(**{
        'id': uuid.uuid4(),
        'timestamp': int(),
        'datetime': datetime.datetime.now(),
        'lastTradeTimestamp': int(),
        'symbol': symbol.Symbol(base='USD', quote='BTC'),
        'side': order.OrderSide('buy'),
        'price': float(),
        'amount': float(),
        'cost': float(),
        'filled': float(),
        'remaining': float(),
        'type': order.OrderType('market'),
        'status': order.OrderStatus('closed'),
        'fee': None,
    })

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

    @given(integers())
    def test_filled_valid(self, v):
        neword_vals = {k: v for k, v in asdict(self.basic_valid).items()
               if k not in ['filled']
            }
        neword_vals.update({ 'filled': v })
        neword = order.Order(
            **neword_vals
        )

    @given(sampled_from([0.42, 'bob']))
    def test_filled_invalid(self, val):
        neword_vals = {k: v for k, v in asdict(self.basic_valid).items()
               if k not in ['filled']
            }
        neword_vals.update({'filled': val})
        with self.assertRaises(pydantic.ValidationError):
            neword = order.Order(
                **neword_vals
            )

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
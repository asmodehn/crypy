import unittest
#https://docs.python.org/3/library/unittest.mock.html
# https://docs.pytest.org/en/latest/unittest.html

import crypy.desk.global_vars as gv  #TODO Validate it first
from crypy.desk.order import Order
from crypy.config import resolve, ExchangeSection


params = [
    ("create" , None),
    ("update", '686796f9-61d9-d3fa-b690-551d94385b65,8517156d-42d6-67c7-1507-c7f6692f1a98')
]


class TestOrder(unittest.TestCase):
    exchangeName = "testnet.bitmex" #TODO temp in the end will need to test every and all exchanges
    ticker = 'BTCUSD' #TODO temp in the end we will need to handle all traded pair for the exchange

    #marketPrice = desk.do_fetchMarketPrice(symbol = gv.ticker2symbol[ticker])
    marketPrice = {'bid': 4000, 'ask': 4001, 'spread': 1}

    ### defaults ###
    leverage = 25
    display_qty = None #TODO TEST others
    amount = None
    price = None
    peg_offset_value = None
    peg_price_type = None
    stop_px = None
    exec_inst = None
    expiracy = None


    def test_LimitLong(self):
        for msg, order_id in params:
            with self.subTest(msg = msg, order_id = order_id):
                side = 'buy'
                type = 'Limit'
                symbol = gv.ticker2symbol[self.ticker]
                amount = 0.5
                price = self.marketPrice['bid'] - 100
                mexAmount = Order._mexContractAmount(currencyAmount = amount, currencyPrice = price)

                order = Order(
                    symbol = symbol,
                    side = side,
                    type = type,
                    leverage = self.leverage,
                    display_qty = self.display_qty,
                    stop_px = self.stop_px,
                    peg_offset_value = self.peg_offset_value,
                    peg_price_type = self.peg_price_type,
                    exec_inst = self.exec_inst,
                    expiracy = self.expiracy,
                    id = order_id,
                    amount = amount,
                    price = price
                )

                orderValidation = order.format(self.marketPrice)
                assert orderValidation is None, orderValidation

                assert order.data == { **{
                    'amount': mexAmount,
                    'leverage': self.leverage,
                    'params': {
                        'displayQty': self.display_qty,
                        'execInst': self.exec_inst,
                        'pegOffsetValue': self.peg_offset_value,
                        'pegPriceType': self.peg_price_type,
                        'stopPx': self.stop_px},
                    'price': price,
                    'side': side,
                    'symbol': symbol,
                    'type': type
                }, **({} if order_id is None else {'id' : order_id}) }, 'invalid order to execute'

    def test_LimitShort(self):
        for msg, order_id in params:
            with self.subTest(msg = msg, order_id =  order_id):
                side = 'sell'
                type = 'Limit'
                symbol = gv.ticker2symbol[self.ticker]
                amount = 0.5
                price = self.marketPrice['ask'] + 100
                mexAmount = Order._mexContractAmount(currencyAmount = amount, currencyPrice = price)

                order = Order(
                    symbol = symbol,
                    side = side,
                    type = type,
                    leverage = self.leverage,
                    display_qty = self.display_qty,
                    stop_px = self.stop_px,
                    peg_offset_value = self.peg_offset_value,
                    peg_price_type = self.peg_price_type,
                    exec_inst = self.exec_inst,
                    expiracy = self.expiracy,
                    id = order_id,
                    amount = amount,
                    price = price
                )

                orderValidation = order.format(self.marketPrice)
                assert orderValidation is None, orderValidation

                assert order.data == {**{
                    'amount': mexAmount,
                    'leverage': self.leverage,
                    'params': {
                        'displayQty': self.display_qty,
                        'execInst': self.exec_inst,
                        'pegOffsetValue': self.peg_offset_value,
                        'pegPriceType': self.peg_price_type,
                        'stopPx': self.stop_px
                    },
                    'price': price,
                    'side': side,
                    'symbol': symbol,
                    'type': type
                }, **({} if order_id is None else {'id': order_id})}, 'invalid order to execute'

    def test_MarketLong(self):
        for msg, order_id in params:
            with self.subTest(msg = msg, order_id =  order_id):
                side = 'buy'
                type = 'Market'
                symbol = gv.ticker2symbol[self.ticker]
                amount = 0.5
                price = None
                currentPrice = (self.marketPrice['bid'] + self.marketPrice['ask'])/2
                mexAmount = Order._mexContractAmount(currencyAmount = amount, currencyPrice = currentPrice)

                order = Order(
                    symbol = symbol,
                    side = side,
                    type = type,
                    leverage = self.leverage,
                    display_qty = self.display_qty,
                    stop_px = self.stop_px,
                    peg_offset_value = self.peg_offset_value,
                    peg_price_type = self.peg_price_type,
                    exec_inst = self.exec_inst,
                    expiracy = self.expiracy,
                    id = order_id,
                    amount = amount,
                    price = price
                )

                orderValidation = order.format(self.marketPrice)
                assert orderValidation is None, orderValidation

                assert order.data == { **{
                    'amount': mexAmount,
                    'leverage': self.leverage,
                    'params': {
                        'displayQty': self.display_qty,
                        'execInst': self.exec_inst,
                        'pegOffsetValue': self.peg_offset_value,
                        'pegPriceType': self.peg_price_type,
                        'stopPx': self.stop_px},
                    'price': price,
                    'side': side,
                    'symbol': symbol,
                    'type': type
                }, **({} if order_id is None else {'id' : order_id}) }, 'invalid order to execute'

    def test_MarketShort(self):
        for msg, order_id in params:
            with self.subTest(msg = msg, order_id =  order_id):
                side = 'sell'
                type = 'Market'
                symbol = gv.ticker2symbol[self.ticker]
                amount = 0.5
                price = None
                currentPrice = (self.marketPrice['bid'] + self.marketPrice['ask'])/2
                mexAmount = Order._mexContractAmount(currencyAmount = amount, currencyPrice = currentPrice)

                order = Order(
                    symbol = symbol,
                    side = side,
                    type = type,
                    leverage = self.leverage,
                    display_qty = self.display_qty,
                    stop_px = self.stop_px,
                    peg_offset_value = self.peg_offset_value,
                    peg_price_type = self.peg_price_type,
                    exec_inst = self.exec_inst,
                    expiracy = self.expiracy,
                    id = order_id,
                    amount = amount,
                    price = price
                )

                orderValidation = order.format(self.marketPrice)
                assert orderValidation is None, orderValidation

                assert order.data == { **{
                    'amount': mexAmount,
                    'leverage': self.leverage,
                    'params': {
                        'displayQty': self.display_qty,
                        'execInst': self.exec_inst,
                        'pegOffsetValue': self.peg_offset_value,
                        'pegPriceType': self.peg_price_type,
                        'stopPx': self.stop_px},
                    'price': price,
                    'side': side,
                    'symbol': symbol,
                    'type': type}, **({} if order_id is None else {'id' : order_id}) }, 'invalid order to execute'

    def test_StopBuy(self):
        for msg, order_id in params:
            with self.subTest(msg = msg, order_id =  order_id):
                side = 'buy'
                type = 'Market'
                symbol = gv.ticker2symbol[self.ticker]
                amount = 0.5
                price = self.marketPrice['ask'] + 100

                mexAmount = Order._mexContractAmount(currencyAmount = amount, currencyPrice = price)
                returnedType = 'Stop'
                returned_stopPx = price
                returned_exec_inst = 'IndexPrice'

                order = Order(
                    symbol = symbol,
                    side = side,
                    type = type,
                    leverage = self.leverage,
                    display_qty = self.display_qty,
                    stop_px = self.stop_px,
                    peg_offset_value = self.peg_offset_value,
                    peg_price_type = self.peg_price_type,
                    exec_inst = self.exec_inst,
                    expiracy = self.expiracy,
                    id = order_id,
                    amount = amount,
                    price = price
                )

                orderValidation = order.format(self.marketPrice)
                assert orderValidation is None, orderValidation

                assert order.data == { **{
                    'amount': mexAmount,
                    'leverage': self.leverage,
                    'params': {
                        'displayQty': self.display_qty,
                        'execInst': returned_exec_inst,
                        'pegOffsetValue': self.peg_offset_value,
                        'pegPriceType': self.peg_price_type,
                        'stopPx': returned_stopPx
                    },
                    'side': side,
                    'symbol': symbol,
                    'type': returnedType}, **({} if order_id is None else {'id' : order_id})}, 'invalid order to execute'

    def test_StopSell(self):
        for msg, order_id in params:
            with self.subTest(msg = msg, order_id =  order_id):
                side = 'sell'
                type = 'Market'
                symbol = gv.ticker2symbol[self.ticker]
                amount = 0.5
                price = self.marketPrice['bid'] - 100

                mexAmount = Order._mexContractAmount(currencyAmount = amount, currencyPrice = price)
                returnedType = 'Stop'
                returned_stopPx = price
                returned_exec_inst = 'IndexPrice'

                order = Order(
                    symbol = symbol,
                    side = side,
                    type = type,
                    leverage = self.leverage,
                    display_qty = self.display_qty,
                    stop_px = self.stop_px,
                    peg_offset_value = self.peg_offset_value,
                    peg_price_type = self.peg_price_type,
                    exec_inst = self.exec_inst,
                    expiracy = self.expiracy,
                    id = order_id,
                    amount = amount,
                    price = price
                )

                orderValidation = order.format(self.marketPrice)
                assert orderValidation is None, orderValidation

                assert order.data == { ** {
                    'amount': mexAmount,
                    'leverage': self.leverage,
                    'params': {
                        'displayQty': self.display_qty,
                        'execInst': returned_exec_inst,
                        'pegOffsetValue': self.peg_offset_value,
                        'pegPriceType': self.peg_price_type,
                        'stopPx': returned_stopPx
                    },
                    'side': side,
                    'symbol': symbol,
                    'type': returnedType
                }, **({} if order_id is None else {'id' : order_id})}, 'invalid order to execute'

    def test_TakeProfitBuy(self):
        for msg, order_id in params:
            with self.subTest(msg = msg, order_id =  order_id):
                side = 'buy'
                type = 'Market'
                symbol = gv.ticker2symbol[self.ticker]
                amount = 0.5
                price = self.marketPrice['bid'] - 100

                mexAmount = Order._mexContractAmount(currencyAmount = amount, currencyPrice = price)
                returnedType = 'MarketIfTouched'
                returned_stopPx = price
                returned_exec_inst = 'IndexPrice'

                order = Order(
                    symbol = symbol,
                    side = side,
                    type = type,
                    leverage = self.leverage,
                    display_qty = self.display_qty,
                    stop_px = self.stop_px,
                    peg_offset_value = self.peg_offset_value,
                    peg_price_type = self.peg_price_type,
                    exec_inst = self.exec_inst,
                    expiracy = self.expiracy,
                    id = order_id,
                    amount = amount,
                    price = price
                )

                orderValidation = order.format(self.marketPrice)
                assert orderValidation is None, orderValidation

                assert order.data == { **{
                    'amount': mexAmount,
                    'leverage': self.leverage,
                    'params': {
                        'displayQty': self.display_qty,
                        'execInst': returned_exec_inst,
                        'pegOffsetValue': self.peg_offset_value,
                        'pegPriceType': self.peg_price_type,
                        'stopPx': returned_stopPx
                    },
                    'side': side,
                    'symbol': symbol,
                    'type': returnedType}, **({} if order_id is None else {'id' : order_id})}, 'invalid order to execute'

    def test_TakeProfitSell(self):
        for msg, order_id in params:
            with self.subTest(msg = msg, order_id =  order_id):
                side = 'sell'
                type = 'Market'
                symbol = gv.ticker2symbol[self.ticker]
                amount = 0.5
                price = self.marketPrice['ask'] + 100

                mexAmount = Order._mexContractAmount(currencyAmount = amount, currencyPrice = price)
                returnedType = 'MarketIfTouched'
                returned_stopPx = price
                returned_exec_inst = 'IndexPrice'

                order = Order(
                    symbol = symbol,
                    side = side,
                    type = type,
                    leverage = self.leverage,
                    display_qty = self.display_qty,
                    stop_px = self.stop_px,
                    peg_offset_value = self.peg_offset_value,
                    peg_price_type = self.peg_price_type,
                    exec_inst = self.exec_inst,
                    expiracy = self.expiracy,
                    id = order_id,
                    amount = amount,
                    price = price
                )

                orderValidation = order.format(self.marketPrice)
                assert orderValidation is None, orderValidation

                assert order.data == { **{
                    'amount': mexAmount,
                    'leverage': self.leverage,
                    'params': {
                        'displayQty': self.display_qty,
                        'execInst': returned_exec_inst,
                        'pegOffsetValue': self.peg_offset_value,
                        'pegPriceType': self.peg_price_type,
                        'stopPx': returned_stopPx
                    },
                    'side': side,
                    'symbol': symbol,
                    'type': returnedType
                }, **({} if order_id is None else {'id' : order_id}) }, 'invalid order to execute'

    def test_Stop(self):
        for msg, order_id in params:
            with self.subTest(msg = msg, order_id =  order_id):
                side = 'buy' #TODO other side
                type = 'Stop'
                symbol = gv.ticker2symbol[self.ticker]
                amount = None #TODO partial Stop w n amount
                stop_px = self.marketPrice['ask'] + 100
                exec_inst = 'IndexPrice' #',Close' #TODO full stop

                #mexAmount = Order._mexContractAmount(currencyAmount = amount, currencyPrice = price)
                returned_type = type
                returned_amount = Order._mexContractAmount(currencyAmount = amount, currencyPrice = price) if amount is not None else None
                returned_stopPx = stop_px
                returned_exec_inst = exec_inst

                order = Order(
                    symbol = symbol,
                    side = side,
                    type = type,
                    leverage = self.leverage,
                    display_qty = self.display_qty,
                    stop_px = stop_px,
                    peg_offset_value = self.peg_offset_value,
                    peg_price_type = self.peg_price_type,
                    exec_inst = exec_inst,
                    expiracy = self.expiracy,
                    id = order_id,
                    amount = amount,
                    price = self.price
                )

                orderValidation = order.format(self.marketPrice)
                assert orderValidation is None, orderValidation

                assert order.data == { **{
                    'amount': returned_amount,
                    'leverage': self.leverage,
                    'params': {
                        'displayQty': self.display_qty,
                        'execInst': returned_exec_inst,
                        'pegOffsetValue': self.peg_offset_value,
                        'pegPriceType': self.peg_price_type,
                        'stopPx': returned_stopPx
                    },
                    'price': None,
                    'side': side,
                    'symbol': symbol,
                    'type': returned_type
                }, **({} if order_id is None else {'id' : order_id}) }, 'invalid order to execute'

    def test_TakeProfit(self):
        for msg, order_id in params:
            with self.subTest(msg = msg, order_id =  order_id):
                side = 'sell' #TODO other side
                type = 'MarketIfTouched'
                symbol = gv.ticker2symbol[self.ticker]
                amount = None #TODO partial TP w an amount
                stop_px = self.marketPrice['bid'] - 100
                exec_inst = 'IndexPrice' #',Close' #TODO full stop

                #mexAmount = Order._mexContractAmount(currencyAmount = amount, currencyPrice = price)
                returned_type = type
                returned_amount = Order._mexContractAmount(currencyAmount = amount, currencyPrice = price) if amount is not None else None
                returned_stopPx = stop_px
                returned_exec_inst = exec_inst

                order = Order(
                    symbol = symbol,
                    side = side,
                    type = type,
                    leverage = self.leverage,
                    display_qty = self.display_qty,
                    stop_px = stop_px,
                    peg_offset_value = self.peg_offset_value,
                    peg_price_type = self.peg_price_type,
                    exec_inst = exec_inst,
                    expiracy = self.expiracy,
                    id = order_id,
                    amount = amount,
                    price = self.price
                )

                orderValidation = order.format(self.marketPrice)
                assert orderValidation is None, orderValidation

                assert order.data ==  { **{
                    'amount': returned_amount,
                    'leverage': self.leverage,
                    'params': {
                        'displayQty': self.display_qty,
                        'execInst': returned_exec_inst,
                        'pegOffsetValue': self.peg_offset_value,
                        'pegPriceType': self.peg_price_type,
                        'stopPx': returned_stopPx
                    },
                    'price': None,
                    'side': side,
                    'symbol': symbol,
                    'type': returned_type
                }, **({} if order_id is None else {'id' : order_id}) }, 'invalid order to execute'

    def test_TrailingStop(self):
        for msg, order_id in params:
            with self.subTest(msg = msg, order_id =  order_id):
                side = 'buy' #TODO other side
                type = 'Pegged'
                peg_price_type = 'TrailingStopPeg'
                symbol = gv.ticker2symbol[self.ticker]
                amount = None #TODO partial Stop w n amount
                peg_offset_value = 100
                exec_inst = 'IndexPrice' #',Close' #TODO full stop

                #mexAmount = Order._mexContractAmount(currencyAmount = amount, currencyPrice = price)
                returned_type = 'Stop'
                returned_amount = Order._mexContractAmount(currencyAmount = amount, currencyPrice = price) if amount is not None else None
                returned_peg_price_type = peg_price_type
                returned_peg_offset_value = peg_offset_value
                returned_exec_inst = exec_inst

                order = Order(
                    symbol = symbol,
                    side = side,
                    type = type,
                    leverage = self.leverage,
                    display_qty = self.display_qty,
                    stop_px = self.stop_px,
                    peg_offset_value = peg_offset_value,
                    peg_price_type = peg_price_type,
                    exec_inst = exec_inst,
                    expiracy = self.expiracy,
                    id = order_id,
                    amount = amount,
                    price = self.price
                )

                orderValidation = order.format(self.marketPrice)
                assert orderValidation is None, orderValidation

                assert order.data == { **{
                    'amount': returned_amount,
                    'leverage': self.leverage,
                    'params': {
                        'displayQty': self.display_qty,
                        'execInst': returned_exec_inst,
                        'pegOffsetValue': returned_peg_offset_value,
                        'pegPriceType': returned_peg_price_type,
                        'stopPx': self.stop_px
                    },
                    'price': None,
                    'side': side,
                    'symbol': symbol,
                    'type': returned_type
                }, **({} if order_id is None else {'id' : order_id}) }, 'invalid order to execute'


if __name__ == '__main__':
    unittest.main()

import unittest
#https://docs.python.org/3/library/unittest.mock.html
import pytest
# https://docs.pytest.org/en/latest/unittest.html

import crypy.desk.global_vars as gv #TODO Validate it first
from crypy.desk.desk import Desk #TODO Validate it first
from crypy.desk.order import Order


def pytest_generate_tests(metafunc):
    # called once per each test function
    try:
        funcarglist = metafunc.cls.params[metafunc.function.__name__]
    except KeyError:
        return

    argnames = sorted(funcarglist[0])
    metafunc.parametrize(argnames, [[funcargs[name] for name in argnames]
            for funcargs in funcarglist])


class TestOrder:
    exchangeName = "testnet.bitmex" #TODO temp in the ne d will need to very all exchanges
    ticker = 'BTCUSD' #TODO temp in the ne d will need to very all traded pair for the exchange

    desk = Desk(exchange=exchangeName)
    exchange = desk.exchange
    #marketPrice = desk.do_fetchMarketPrice(symbol = gv.ticker2symbol[ticker])
    marketPrice = { 'bid': 4000, 'ask': 4001, 'spread': 1 }

    ### defaults ###
    ticker = 'BTCUSD'
    side = 'buy' #TODO TEST others
    order_type = 'Limit' #TODO TEST others
    leverage = 25
    display_qty = None #TODO TEST others
    id = None #TODO TEST w & wo
    amount = None
    price = None
    peg_offset_value = None
    peg_price_type = None
    stop_px = None
    exec_inst = None
    expiracy = None

    # Ref : https://docs.pytest.org/en/latest/example/parametrize.html#parametrizing-test-methods-through-per-class-configuration
    # a map specifying multiple argument sets for a test method
    params = {
        'test_LimitLong': [{'id': None}, {'id': '686796f9-61d9-d3fa-b690-551d94385b65,8517156d-42d6-67c7-1507-c7f6692f1a98'}],
        'test_LimitShort': [{'id': None}, {'id': '686796f9-61d9-d3fa-b690-551d94385b65,8517156d-42d6-67c7-1507-c7f6692f1a98'}],
        'test_MarketLong': [{'id': None}, {'id': '686796f9-61d9-d3fa-b690-551d94385b65,8517156d-42d6-67c7-1507-c7f6692f1a98'}],
        'test_MarketShort': [{'id': None}, {'id': '686796f9-61d9-d3fa-b690-551d94385b65,8517156d-42d6-67c7-1507-c7f6692f1a98'}],
        'test_StopBuy': [{'id': None}, {'id': '686796f9-61d9-d3fa-b690-551d94385b65,8517156d-42d6-67c7-1507-c7f6692f1a98'}],
        'test_StopSell': [{'id': None}, {'id': '686796f9-61d9-d3fa-b690-551d94385b65,8517156d-42d6-67c7-1507-c7f6692f1a98'}],
        'test_TakeProfitBuy': [{'id': None}, {'id': '686796f9-61d9-d3fa-b690-551d94385b65,8517156d-42d6-67c7-1507-c7f6692f1a98'}],
        'test_TakeProfitSell': [{'id': None}, {'id': '686796f9-61d9-d3fa-b690-551d94385b65,8517156d-42d6-67c7-1507-c7f6692f1a98'}],
        'test_Stop': [{'id': None}, {'id': '686796f9-61d9-d3fa-b690-551d94385b65,8517156d-42d6-67c7-1507-c7f6692f1a98'}],
        'test_TakeProfit': [{'id': None}, {'id': '686796f9-61d9-d3fa-b690-551d94385b65,8517156d-42d6-67c7-1507-c7f6692f1a98'}],
        'test_TrailingStop': [{'id': None}, {'id': '686796f9-61d9-d3fa-b690-551d94385b65,8517156d-42d6-67c7-1507-c7f6692f1a98'}],
    }

    def test_Exchange(self):
        ccxtExchangeNeededMethods = [
            'createMarketOrder',
            'createOrder',
            'editOrder',
            'privatePostPositionLeverage',
            'cancelOrder',
            'fetchL2OrderBook'
        ]
        #TODO test 'do_fetchMarketPrice' exists on desk

        for ccxtMethod in ccxtExchangeNeededMethods:
            if ccxtMethod not in self.exchange.has or not self.exchange.has[ccxtMethod]: #ccxt unified method check
                if not hasattr(self.exchange, ccxtMethod): #ccxt implicit (not unified) method check
                    pytest.fail( msg =  f'{ccxtMethod}() not available for this exchange' )

    def test_LimitLong(self, id):
        side = 'buy'
        type = 'Limit'
        symbol = gv.ticker2symbol[self.ticker]
        amount = 0.5
        price = self.marketPrice['bid'] - 100
        mexAmount = Order._mexContractAmount(currencyAmount = amount, currencyPrice = price)

        order = Order(
            exchange = self.exchange,
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
            id = id,
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
        }, **({} if id is None else {'id' : id}) }, 'invalid order to execute'

    def test_LimitShort(self, id):
        side = 'sell'
        type = 'Limit'
        symbol = gv.ticker2symbol[self.ticker]
        amount = 0.5
        price = self.marketPrice['ask'] + 100
        mexAmount = Order._mexContractAmount(currencyAmount = amount, currencyPrice = price)

        order = Order(
            exchange = self.exchange,
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
            id = id,
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
        }, **({} if id is None else {'id': id})}, 'invalid order to execute'


    def test_MarketLong(self, id):
        side = 'buy'
        type = 'Market'
        symbol = gv.ticker2symbol[self.ticker]
        amount = 0.5
        price = None
        currentPrice = (self.marketPrice['bid'] + self.marketPrice['ask'])/2
        mexAmount = Order._mexContractAmount(currencyAmount = amount, currencyPrice = currentPrice)

        order = Order(
            exchange = self.exchange,
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
            id = id,
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
        }, **({} if id is None else {'id' : id}) }, 'invalid order to execute'

    def test_MarketShort(self, id):
        side = 'sell'
        type = 'Market'
        symbol = gv.ticker2symbol[self.ticker]
        amount = 0.5
        price = None
        currentPrice = (self.marketPrice['bid'] + self.marketPrice['ask'])/2
        mexAmount = Order._mexContractAmount(currencyAmount = amount, currencyPrice = currentPrice)

        order = Order(
            exchange = self.exchange,
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
            id = id,
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
            'type': type}, **({} if id is None else {'id' : id}) }, 'invalid order to execute'

    def test_StopBuy(self, id):
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
            exchange = self.exchange,
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
            id = id,
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
            'type': returnedType}, **({} if id is None else {'id' : id})}, 'invalid order to execute'

    def test_StopSell(self, id):
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
            exchange = self.exchange,
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
            id = id,
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
        }, **({} if id is None else {'id' : id})}, 'invalid order to execute'


    def test_TakeProfitBuy(self, id):
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
            exchange = self.exchange,
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
            id = id,
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
            'type': returnedType}, **({} if id is None else {'id' : id})}, 'invalid order to execute'

    def test_TakeProfitSell(self, id):
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
            exchange = self.exchange,
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
            id = id,
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
        }, **({} if id is None else {'id' : id}) }, 'invalid order to execute'


    def test_Stop(self, id):
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
            exchange = self.exchange,
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
            id = id,
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
        }, **({} if id is None else {'id' : id}) }, 'invalid order to execute'

    def test_TakeProfit(self, id):
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
            exchange = self.exchange,
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
            id = id,
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
        }, **({} if id is None else {'id' : id}) }, 'invalid order to execute'

    def test_TrailingStop(self, id):
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
            exchange = self.exchange,
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
            id = id,
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
        }, **({} if id is None else {'id' : id}) }, 'invalid order to execute'


    @pytest.mark.skip(reason="Not implemented")
    def test_Cancel(self):
        #Nothing specific to test atm except execution
        pass


    @pytest.mark.skip(reason="Not implemented")
    def test_CancelAll(self):
        #Method not done yet
        pass


    @pytest.mark.skip(reason="Not implemented")
    def test_fetchL2OrderBook(self):
        #Nothing specific to test atm except execution
        pass

    @pytest.mark.skip(reason="Not implemented")
    def test_execute(self):
        #Nothing specific to test atm except execution
        #order.execute()
        pass

    
if __name__ == '__main__':
    pytest.main(['-s', __file__])

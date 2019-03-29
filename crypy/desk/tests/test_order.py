import unittest
#https://docs.python.org/3/library/unittest.mock.html

import crypy.desk.global_vars as gv #TODO Validate it first
from crypy.desk.desk import Desk #TODO Validate it first
from crypy.desk.order import Order

class Test_order(unittest.TestCase):
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
                    self.fail( msg =  f'{ccxtMethod}() not available for this exchange' )

        self.assertTrue

    def test_CreateLimitLong(self):
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
            id = self.id,
            amount = amount,
            price = price
        )

        orderValidation = order.format(self.marketPrice)
        if orderValidation is not None:
            self.fail(msg = orderValidation)
        
        self.assertEqual(
            first = order.data,
            second = {'amount': mexAmount, 'leverage': self.leverage, 'params': {'displayQty': self.display_qty, 'execInst': self.exec_inst, 'pegOffsetValue': self.peg_offset_value, 'pegPriceType': self.peg_price_type, 'stopPx': self.stop_px}, 'price': price, 'side': side, 'symbol': symbol, 'type': type},
            msg = 'invalid order to execute'
        )

    def test_CreateLimitShort(self):
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
            id = self.id,
            amount = amount,
            price = price
        )

        orderValidation = order.format(self.marketPrice)
        if orderValidation is not None:
            self.fail(msg = orderValidation)
        
        self.assertEqual(
            first = order.data,
            second = {'amount': mexAmount, 'leverage': self.leverage, 'params': {'displayQty': self.display_qty, 'execInst': self.exec_inst, 'pegOffsetValue': self.peg_offset_value, 'pegPriceType': self.peg_price_type, 'stopPx': self.stop_px}, 'price': price, 'side': side, 'symbol': symbol, 'type': type},
            msg = 'invalid order to execute'
        )

    def test_CreateMarketLong(self):
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
            id = self.id,
            amount = amount,
            price = price
        )

        orderValidation = order.format(self.marketPrice)
        if orderValidation is not None:
            self.fail(msg = orderValidation)
        
        self.assertEqual(
            first = order.data,
            second = {'amount': mexAmount, 'leverage': self.leverage, 'params': {'displayQty': self.display_qty, 'execInst': self.exec_inst, 'pegOffsetValue': self.peg_offset_value, 'pegPriceType': self.peg_price_type, 'stopPx': self.stop_px}, 'price': price, 'side': side, 'symbol': symbol, 'type': type},
            msg = 'invalid order to execute'
        )

    def test_CreateMarketShort(self):
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
            id = self.id,
            amount = amount,
            price = price
        )

        orderValidation = order.format(self.marketPrice)
        if orderValidation is not None:
            self.fail(msg = orderValidation)
        
        self.assertEqual(
            first = order.data,
            second = {'amount': mexAmount, 'leverage': self.leverage, 'params': {'displayQty': self.display_qty, 'execInst': self.exec_inst, 'pegOffsetValue': self.peg_offset_value, 'pegPriceType': self.peg_price_type, 'stopPx': self.stop_px}, 'price': price, 'side': side, 'symbol': symbol, 'type': type},
            msg = 'invalid order to execute'
        )

    def test_CreateStopBuy(self):
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
            id = self.id,
            amount = amount,
            price = price
        )

        orderValidation = order.format(self.marketPrice)
        if orderValidation is not None:
            self.fail(msg = orderValidation)
        
        self.assertEqual(
            first = order.data,
            second = {'amount': mexAmount, 'leverage': self.leverage, 'params': {'displayQty': self.display_qty, 'execInst': returned_exec_inst, 'pegOffsetValue': self.peg_offset_value, 'pegPriceType': self.peg_price_type, 'stopPx': returned_stopPx}, 'side': side, 'symbol': symbol, 'type': returnedType},
            msg = 'invalid order to execute'
        )

    def test_CreateStopSell(self):
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
            id = self.id,
            amount = amount,
            price = price
        )

        orderValidation = order.format(self.marketPrice)
        if orderValidation is not None:
            self.fail(msg = orderValidation)
        
        self.assertEqual(
            first = order.data,
            second = {'amount': mexAmount, 'leverage': self.leverage, 'params': {'displayQty': self.display_qty, 'execInst': returned_exec_inst, 'pegOffsetValue': self.peg_offset_value, 'pegPriceType': self.peg_price_type, 'stopPx': returned_stopPx}, 'side': side, 'symbol': symbol, 'type': returnedType},
            msg = 'invalid order to execute'
        )

    def test_CreateTakeProfitBuy(self):
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
            id = self.id,
            amount = amount,
            price = price
        )

        orderValidation = order.format(self.marketPrice)
        if orderValidation is not None:
            self.fail(msg = orderValidation)
        
        self.assertEqual(
            first = order.data,
            second = {'amount': mexAmount, 'leverage': self.leverage, 'params': {'displayQty': self.display_qty, 'execInst': returned_exec_inst, 'pegOffsetValue': self.peg_offset_value, 'pegPriceType': self.peg_price_type, 'stopPx': returned_stopPx}, 'side': side, 'symbol': symbol, 'type': returnedType},
            msg = 'invalid order to execute'
        )

    def test_CreateTakeProfitSell(self):
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
            id = self.id,
            amount = amount,
            price = price
        )

        orderValidation = order.format(self.marketPrice)
        if orderValidation is not None:
            self.fail(msg = orderValidation)
        
        self.assertEqual(
            first = order.data,
            second = {'amount': mexAmount, 'leverage': self.leverage, 'params': {'displayQty': self.display_qty, 'execInst': returned_exec_inst, 'pegOffsetValue': self.peg_offset_value, 'pegPriceType': self.peg_price_type, 'stopPx': returned_stopPx}, 'side': side, 'symbol': symbol, 'type': returnedType},
            msg = 'invalid order to execute'
        )

    def test_CreateStop(self):
        self.assertTrue

    def test_CreateTakeProfit(self):
        self.assertTrue

    def test_CreateTrailingStop(self):
        self.assertTrue


    def test_UpdateLimitLong(self):
        self.assertTrue

    def test_UpdateLimitShort(self):
        self.assertTrue

    def test_UpdateMarketShort(self):
        self.assertTrue

    def test_UpdateMarketShort(self):
        self.assertTrue

    def test_UpdateStopBuy(self):
        self.assertTrue

    def test_UpdateStopSell(self):
        self.assertTrue

    def test_UpdateTakeProfitBuy(self):
        self.assertTrue

    def test_UpdateTakeProfitSell(self):
        self.assertTrue

    def test_UpdateStop(self):
        self.assertTrue

    def test_UpdateTakeProfit(self):
        self.assertTrue

    def test_UpdateTrailingStop(self):
        self.assertTrue


    def test_Cancel(self):
        self.assertTrue


    def test_CancelAll(self):
        self.assertTrue


    def test_fetchL2OrderBook(self):
        self.assertTrue


    def test_showData(self):
        self.assertTrue


    def test_execute(self):
        self.assertTrue

    
if __name__ == '__main__':
    unittest.main()

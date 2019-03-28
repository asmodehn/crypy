import unittest

import crypy.desk.global_vars as gv #TODO Validate it first
from crypy.desk.desk import Desk #TODO Validate it first
from crypy.desk.order import Order

class Test_order(unittest.TestCase):
        exchangeName = "testnet.bitmex" #TODO temp in the ne d will need to very all exchanges
        ticker = 'BTCUSD' #TODO temp in the ne d will need to very all traded pair for the exchange

        desk = Desk(exchange=exchangeName)
        exchange = desk.exchange
        marketPrice = desk.do_fetchMarketPrice(symbol = gv.ticker2symbol[ticker])

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


    def test_New(self):

        order = Order(symbol=gv.ticker2symbol[ticker], side=side, type=order_type, leverage=leverage, display_qty=display_qty, stop_px=stop_px, peg_offset_value=peg_offset_value, peg_price_type=peg_price_type, exec_inst=exec_inst, expiracy=expiracy, id=id, amount=amount, price=price)

        orderValidation = order.format()
        if orderValidation is not None:
            return self.fail( msg = orderValidation)

        self.assertTrue

        def test_CreateLimitLong(self):
            self.assertTrue

        def test_CreateLimitShort(self):
            self.assertTrue

        def test_CreateMarketShort(self):
            self.assertTrue

        def test_CreateMarketShort(self):
            self.assertTrue

        def test_CreateStopBuy(self):
            self.assertTrue

        def test_CreateStopSell(self):
            self.assertTrue

        def test_CreateTakeProfitBuy(self):
            self.assertTrue

        def test_CreateTakeProfitSell(self):
            self.assertTrue

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


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click

import structlog
filename = 'log.txt'
file = open( filename, 'a') #TODO where do we close it
#structlog.configure( logger_factory=structlog.PrintLogger(file = file) )
logger = structlog.PrintLogger(file = file)


try:
    from ..euc import ccxt
except (ImportError, ValueError, ModuleNotFoundError):
    from crypy.euc import ccxt

class Order():
    """
    Order class WIP
    abstract
    """

    def __init__(self, side, symbol, type, leverage, display_qty, stop_px, peg_offset_value, peg_price_type, exec_inst, expiracy, amount, price, id = None):
        #TODO(future): Note, that some exchanges will not accept market orders (they only allow limit orders).
        #if exchange.has['createMarketOrder']:

        self.data = {
            'symbol' : symbol,
            'type' : type,
            'side' : side,
            'amount' : amount,
            'price' : price,
            'leverage': leverage,
            'id': id,
            'params' : {
                'stopPx': stop_px,
                "execInst" : exec_inst,
                "displayQty" : display_qty,
                "pegOffsetValue" : peg_offset_value,
                "pegPriceType" : peg_price_type
             }
        }
        self.format()

    def format(self):
        #TODO: MAYBE we should think about passing the exchange to the order class directly on class instanciation and use one instance ?
        desk = click.get_current_context().obj
        exg = desk.exchange

        ### LEVERAGE handling ###
        leverage = self.data['leverage']
        del self.data['leverage'] #remove the leverage from the order data coz createOrder() doesnt handle it
        ### end LEVERAGE handling ###

        ### ID handling ###
        orderId = self.data['id']
        if orderId is None:
            if not 'createOrder' in exg.has or not exg.has['createOrder']:
                return f'createOrder() not available for this exchange'
            del self.data['id'] #remove the id from the order data coz createOrder() doesnt handle it
        else:
            if not 'editOrder' in exg.has or not exg.has['editOrder']:
                return f'editOrder() not available for this exchange'

            #TODO check side of new and old orders (aka when an id is present) are the same, otherwise ccxt error (mex: immediate liquidation error)
        ### end ID handling ###

            
        ### TYPE handling ###
        if self.data['type'] in ['Market', 'Limit']:
            if leverage > 1:
                if not hasattr(exg, 'privatePostPositionLeverage'): #working on bitmex, check other exchanges
                    return f'privatePostPositionLeverage() not available for this exchange'

            if self.data['type'] is 'Market': #market order
                marketPrice = desk.do_fetchMarketPrice(symbol = self.data['symbol'])

                if self.data['price'] is None: #market order -> 'real' Market order
                    price = (marketPrice['bid'] + marketPrice['ask'])/2

                else: #stop-buy|sell and take-profit-buy|sell orders
                    #stop/tp price
                    price = self.data['price']
                    self.data['params']['stopPx'] = price
                    del self.data['price']

                    self.data['params']['exec_inst'] = 'IndexPrice'
                    
                    #Mex valid order type
                    if self.data['side'] is 'buy':
                        if price >= marketPrice['bid']: #stop-buy
                            self.data['type'] =  'Stop'
                        elif price <= marketPrice['ask']: #tp-buy
                            self.data['type'] =  'MarketIfTouched'
                    if self.data['side'] is 'sell':
                        if price >= marketPrice['bid']: #tp-sell
                            self.data['type'] =  'MarketIfTouched'
                        elif price <= marketPrice['ask']: #stop-sell
                            self.data['type'] =  'Stop'


            else: #limit order [TODO(future) 'StopLimit' and take profit limit ('LimitIfTouched') orders maybe]
                price = self.data['price']


            
        elif self.data['type'] in ['Stop', 'MarketIfTouched']: #Stop & Take profit order
            if not self.data['amount'] is None: #don't care if we don't have an amount but if we do we need to transform it into bitmex contracts
                price = self.data['params']['stopPx']


        elif self.data['type'] in ['Pegged']: #trailing stop order
            #Mex valid order type
            self.data['type'] =  'Stop'

            if not self.data['amount'] is None:  #don't care if we don't have an amount but if we do we need to transform it into bitmex contracts
                marketPrice = desk.do_fetchMarketPrice(symbol = self.data['symbol'])
                price = (marketPrice['bid'] + marketPrice['ask'])/2 + self.data['params']['pegOffsetValue'] #add offset to market price
        ### end TYPE handling ###

        ### AMOUNT handling ###
        #Mex Specifik: nb of contracts to order (int) == order amount * order price
        if not self.data['amount'] is None:
            self.data['amount'] = int(self.data['amount'] * price)
            self.data['amount'] = (1 if self.data['amount'] == 0 else self.data['amount']) #always at least 1 contract for the order and handle negative values
        ### end AMOUNT handling ###

    def showData(self): 
        for key, value in self.data.items():
            if type(value) is dict:
                print(f" ○ {key}:")
                for subKey, subValue in value.items():
                    print(f"    • {subKey}: {subValue}")
            else:
                print(f" ○ {key}: {value}")

    def execute(self, leverage):
        try:
            #TODO: MAYBE we should think about passing the exchange to the order class directly on class instanciation and use one instance ?
            exg = click.get_current_context().obj.exchange

            #first handle the leverage (NB: it changes leverage of existing orders too!)
            if leverage is not None:
                response2 = exg.privatePostPositionLeverage({"symbol": exg.markets[self.data['symbol']]['id'], "leverage": leverage})
                logger.msg(str(response2))

            #second post/update order
            if 'id' not in self.data or self.data['id'] is None:
                response = exg.createOrder(**dict(self.data))
            else:
                response = exg.editOrder(**dict(self.data))
                
            logger.msg(str(response))

            return 'order_id: ' + response['id']

        except ccxt.BaseError as error:
            return error.args[0]
        except Exception as error:
            return "Error: " + str(type(error)) + " " + str(error)

    @staticmethod
    def cancel(order_ids):
        exg = click.get_current_context().obj.exchange
        if not 'cancelOrder' in exg.has or not exg.has['cancelOrder']:
            return f'cancelOrder() not available for this exchange'

        for order_id in order_ids:
            try:
                exg.cancelOrder(order_id)
                print(f'order(s) {order_id} canceled')
                #TODO remove from log also
            except ccxt.NetworkError as err:
                #TODO retry cancelation
                pass
            except ccxt.ValidationError as err:
                print(f'order(s) {order_id} invalid: bad length, cancel failed')
            except ccxt.OrderNotFound as err:
                print(f'order(s) {order_id} not found: already canceled/closed or invalid order id, cancel failed')
            except ccxt.BaseError as error:
                print(f'order(s) {order_id} not found invalid order id or something else, cancel failed')
                print(error.args[0])

    @staticmethod
    def fetchL2OrderBook(symbol, limit):
        orderbook = click.get_current_context().obj._ccxtMethod('fetchL2OrderBook', symbol = symbol, limit = limit)
        return orderbook #TODO better format i guess

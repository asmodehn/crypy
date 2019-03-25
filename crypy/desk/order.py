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
    #struct = {
    #    'symbol' : 'TBD',
    #    'side': 'buy|sell',
    #    'type': 'limit(default)|market [future: |stop limit|stop market|take profit|traling stop]', #TODO other useful types need to overide exchange params https://github.com/ccxt/ccxt/wiki/Manual#overriding-unified-api-params
    #    'amount': 'TBD',
    #    'price': 'TBD',
    #    'leverage': '1->5(default)',
    #    'expiracy': 'none(default)|TBD'
    #}

    def __init__(self, side, symbol, type, leverage, display_qty, stop_px, peg_offset_value, peg_price_type, exec_inst, expiracy, amount, price, id = None):
        #TODO(future): Note, that some exchanges will not accept market orders (they allow limit orders only).
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
                "execInst" : exec_inst
             }
        }
        ## TODO overrides for other orders
        #params = {
        #    'stopPrice': 123.45,  # your stop price
        #    'type': 'stopLimit',
        #}

    def showData(self): 
        for k, v in self.data.items():
            print(f" ¤ {k} -> {v}")

    def execute(self):
        try:
            #TODO: MAYBE we should think about passing the exchange to the order class directly on class instanciation and use one instance ?
            desk = click.get_current_context().obj
            exg = desk.exchange
            leverage = self.data['leverage']
            del self.data['leverage'] #remove the leverage from the order data coz createOrder() doesnt handle it

            ### ORDER ID HANDLING ###
            orderId = self.data['id']
            if orderId is None:
                if not 'createOrder' in exg.has or not exg.has['createOrder']:
                    return f'createOrder() not available for this exchange'
                del self.data['id'] #remove the id from the order data coz createOrder() doesnt handle it
            else:
                if not 'editOrder' in exg.has or not exg.has['editOrder']:
                    return f'editOrder() not available for this exchange'

                #TODO check side of new and old orders (aka when an id is present) are the same, otherwise ccxt error (mex: immediate liquidation error)
            ### END ORDER ID HANDLING ###

            
            #Mex Specifik: nb of contracts to order (int) == order amount * order price
            if self.data['type'] in ['Market', 'Limit']:
                if self.data['price'] is None or self.data['type'] is 'Market': #no price, aka market order
                    marketPrice = desk.do_fetchMarketPrice(symbol = self.data['symbol'])
                    price = (marketPrice['bid'] + marketPrice['ask'])/2
                else:
                    price = self.data['price']

                self.data['amount'] = int(self.data['amount'] * price)

                if leverage > 1 and (not hasattr(exg, 'privatePostPositionLeverage')): #working on bitmex, check other exchanges
                    return f'privatePostPositionLeverage() not available for this exchange'

            
                #first set the leverage (NB: it changes leverage of existing orders too!)
                response2 = exg.privatePostPositionLeverage({"symbol": exg.markets[self.data['symbol']]['id'], "leverage": leverage})
                logger.msg(str(response2))

            
            elif self.data['type'] in ['Stop']:
                if not self.data['amount'] is None: #don't care if we don't have an amount but if we do we need to transform it into bitmex contracts
                    self.data['amount'] = int(self.data['amount'] * self.data['params']['stopPx'])
                    self.data['amount'] = (1 if self.data['amount'] == 0 else self.data['amount']) #always at least 1 contract for the order and handle negative values

            elif self.data['type'] in ['StopShort', 'StopLong']:
                marketPrice = desk.do_fetchMarketPrice(symbol = self.data['symbol'])

                #compare to market price
                if self.data['type'] is 'StopShort':
                    if self.data['params']['stopPx'] >= marketPrice['bid']:
                        return f'Error: StopShort value is above market price.'
                elif self.data['type'] is 'StopLong':
                    if self.data['params']['stopPx'] <= marketPrice['ask']:
                        return f'Error: StopLong value is below market price.'

                #Mex valid order type
                self.data['type'] =  'Stop'

                #Mex contracts transformation
                self.data['amount'] = int(self.data['amount'] * self.data['params']['stopPx'])
                self.data['amount'] = (1 if self.data['amount'] == 0 else self.data['amount']) #always at least 1 contract for the order and handle negative values

            #second post/update order
            if orderId is None:
                response = exg.createOrder(**dict(self.data))
            else:
                response = exg.editOrder(**dict(self.data))
                
            orderId = response['id']
            logger.msg(str(response))

            return 'order_id: ' + orderId

        except ccxt.BaseError as error:
            return error.args[0]

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

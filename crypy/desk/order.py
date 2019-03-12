#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click

try:
    from ..euc import ccxt
except (ImportError, ValueError, ModuleNotFoundError):
    from crypy.euc import ccxt

class Order():
    """
    Order class WIP
    abstract
    """
    struct = {
        'symbol' : 'TBD',
        'side': 'buy|sell',
        'type': 'limit(default)|market [future: |stop limit|stop market|take profit|traling stop]', #TODO other useful types need to overide exchange params https://github.com/ccxt/ccxt/wiki/Manual#overriding-unified-api-params
        'amount': 'TBD',
        'price': 'TBD',
        'leverage': '1->5(default)',
        'expiracy': 'none(default)|TBD'
    }

    def __init__(self, side, symbol, type, leverage, expiracy, amount, price):
        #TODO(future): Note, that some exchanges will not accept market orders (they allow limit orders only).
        #if exchange.has['createMarketOrder']:

        self.data = {
            'symbol' : symbol,
            'type' : type,
            'side' : side,
            'amount' : amount,
            'price' : price
        }
        ## TODO overrides for other orders
        #params = {
        #    'stopPrice': 123.45,  # your stop price
        #    'type': 'stopLimit',
        #}

    def showData(self): 
        for k, v in self.data.items():
            print(f"¤ {k} -> {v}")

    def execute(self):
        try:
            #TODO: MAYBE we should think about passing the exchange to the order class directly on class instanciation and use one instance ?
            desk = click.get_current_context().obj
            exg = desk.exchange
            if not 'createOrder' in exg.has or not exg.has['createOrder']:
                return f'createOrder() not available for this exchange'

            #TODO MEX: nb of contracts to buy == order value * order price
            response = exg.createOrder(**dict(self.data))

            filename = 'exg_' + desk.exchangeName + '_orders.txt'
            file = open( filename, 'a')
            print (response, file = file)
            file.close()
            #TODO SAVE (how/where)

            orderId = response['id']
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
        orderbook = click.get_current_context().obj._ccxtFetchXXX('fetchL2OrderBook', symbol = symbol, limit = limit)
        return orderbook #TODO better format i guess

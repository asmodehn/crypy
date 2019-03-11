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
            success = click.get_current_context().obj.exchange.createOrder(**dict(self.data))
            return 'order_id: ' + success['id']
            #TODO SAVE (how/where)

        except ccxt.BaseError as error:
            return error.args[0]

    @staticmethod
    def cancel(order_ids):
        #TODO
        print(order_ids)
        print(">> TODO <<")

    @staticmethod
    def fetchL2OrderBook(symbol, limit):
        orderbook = click.get_current_context().obj._ccxtFetchXXX('fetchL2OrderBook', symbol = symbol, limit = limit)
        return orderbook #TODO better format i guess

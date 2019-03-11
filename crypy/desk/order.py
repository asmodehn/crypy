#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click

class Order():
    """
    Order class WIP
    abstract
    """
    struct = {
        'id' : 'TBD',
        'side': 'long|short',
        'type': 'limit(default)|market|stop loss|take profit',
        'amount': 'TBD',
        'price': 'TBD',
        'leverage': '1->5(default)',
        'expiracy': 'none(default)|TBD'
    }

    def __init__(self, side, ticker, order_type, leverage, expiracy, amount, price):
        self.data = self.struct   # Copy
        self.data['side'] = side  # TODO make self.data.side immutable after __init__
        self.data['type'] = order_type 
        self.data['leverage'] = leverage 
        self.data['expiracy'] = expiracy 
        self.data['amount'] = amount 
        self.data['price'] = price 
        self.ticker = ticker

    def showData(self): 
        for k, v in self.data.items():
            print(f"¤ {k} -> {v}")

    def execute(self):
        #TODO link to exchange execute operation
        self.data['id'] = 'OU47YA-GYBTO-SRS2IJ' #TODO real orderID
        wholeData[self.ticker]['orders'].append(self.data)
        return self.data['id']

    @staticmethod
    def cancel(order_ids):
        #TODO
        print(order_ids)
        print(">> TODO <<")

    @staticmethod
    def fetchL2OrderBook(symbol, limit):
        orderbook = click.get_current_context().obj._ccxtFetchXXX('fetchL2OrderBook', symbol = symbol, limit = limit)
        return orderbook #TODO better format i guess

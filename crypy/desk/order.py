#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from ..euc import ccxt
except (ImportError, ValueError, ModuleNotFoundError):
    from crypy.euc import ccxt


class Order:
    """
    Order class WIP
    abstract
    """

    def __init__(self, side, symbol, type, leverage = None, display_qty = None, stop_px = None, peg_offset_value = None, peg_price_type = None, exec_inst = None, expiracy = None, amount = None, price = None, id = None):
        #TODO(future): Note, that some exchanges will not accept market orders (they only allow limit orders).

        self.data = {
            'symbol' : symbol,
            'type' : type,
            'side' : side,
            'amount' : amount,
            'price' : price,
            'leverage': leverage,
            'params' : {
                'stopPx': stop_px,
                "execInst" : exec_inst,
                "displayQty" : display_qty,
                "pegOffsetValue" : peg_offset_value,
                "pegPriceType" : peg_price_type
             }
        }

        if id is not None:
            self.data['id'] = id

        #TODO check side of new and old orders (aka when an id is present) are the same, otherwise ccxt error (mex: immediate liquidation error)


    def format(self, marketPrice):
        #TODO error handling
            
        ### TYPE handling ###
        if self.data['type'] in ['Market', 'Limit']:

            if self.data['type'] == 'Market': #market order

                if self.data['price'] is None: #market order -> 'real' Market order
                    price = (marketPrice['bid'] + marketPrice['ask'])/2

                else: #stop-buy|sell and take-profit-buy|sell orders
                    #stop/tp price
                    price = self.data['price']
                    self.data['params']['stopPx'] = price
                    del self.data['price']

                    self.data['params']['execInst'] = 'IndexPrice'
                    
                    #Mex valid order type
                    if self.data['side'] is 'buy':
                        if price >= marketPrice['ask']: #stop-buy
                            self.data['type'] =  'Stop'
                        elif price <= marketPrice['bid']: #tp-buy
                            self.data['type'] =  'MarketIfTouched'
                    elif self.data['side'] is 'sell':
                        if price >= marketPrice['ask']: #tp-sell
                            self.data['type'] =  'MarketIfTouched'
                        elif price <= marketPrice['bid']: #stop-sell
                            self.data['type'] =  'Stop'


            else: #limit order [TODO(future) 'StopLimit' and take profit limit ('LimitIfTouched') orders maybe]
                if 'price' not in self.data or self.data['price'] is None:
                    return f'Error: limit order need a price value'
                price = self.data['price']


            
        elif self.data['type'] in ['Stop', 'MarketIfTouched']: #Stop & Take profit order
            if not self.data['amount'] is None: #don't care if we don't have an amount but if we do we need to transform it into bitmex contracts
                price = self.data['params']['stopPx']


        elif self.data['type'] in ['Pegged']: #trailing stop order
            #Mex valid order type
            self.data['type'] =  'Stop'

            if not self.data['amount'] is None:  #don't care if we don't have an amount but if we do we need to transform it into bitmex contracts
                price = (marketPrice['bid'] + marketPrice['ask'])/2 + self.data['params']['pegOffsetValue'] #add offset to market price
        ### end TYPE handling ###

        ### AMOUNT handling ###
        #Mex Specifik: nb of contracts to order (int) == order amount * order price
        if self.data['amount'] is not None:
            self.data['amount'] = self._mexContractAmount(currencyAmount = self.data['amount'], currencyPrice = price)
        ### end AMOUNT handling ###
    
    @staticmethod
    def _mexContractAmount(currencyAmount, currencyPrice):
        contractAmount = int(currencyAmount * currencyPrice) #rounded
        contractAmount = (1 if contractAmount == 0 else contractAmount) #always at least 1 contract for the order and handle negative values
        return contractAmount

    def showData(self): 
        for key, value in self.data.items():
            if type(value) is dict:
                print(f" ○ {key}:")
                for subKey, subValue in value.items():
                    print(f"    • {subKey}: {subValue}")
            else:
                print(f" ○ {key}: {value}")

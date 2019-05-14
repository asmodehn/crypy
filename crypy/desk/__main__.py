#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from crypy.desk.desk_cli import cli_root_group as cli
#from crypy.desk.capital_cli import capital_group
#from crypy.desk.order_cli import order_group

import asyncio

import crypy.desk.global_vars as gv  #TODO Validate it first
from crypy.desk.order import Order
from crypy.config import resolve, ExchangeSection

"""Entrypoint for the desk subpackage
Manages one (currently) exchange, via CLI
"""

async def asyncLong():
    print('order creation starting')

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

    side = 'buy'
    type = 'Limit'
    symbol = gv.ticker2symbol[ticker]
    amount = 0.5
    price = marketPrice['bid'] - 100
    mexAmount = Order._mexContractAmount(currencyAmount = amount, currencyPrice = price)

    order = Order(
        symbol = symbol,
        side = side,
        type = type,
        leverage = leverage,
        display_qty = display_qty,
        stop_px = stop_px,
        peg_offset_value = peg_offset_value,
        peg_price_type = peg_price_type,
        exec_inst = exec_inst,
        expiracy = expiracy,
        id = None,
        amount = amount,
        price = price
    )

    orderValidation = order.format(marketPrice)

    await asyncio.sleep(1) #TEMP
    return 'order is valid, create it now'

if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    try:
        ret = event_loop.run_until_complete(
            asyncLong()
        )
        print(f"Returned: {ret}")

    finally:
        event_loop.close()

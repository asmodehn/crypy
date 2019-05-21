#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from crypy.desk.desk_cli import cli_root_group as cli
#from crypy.desk.capital_cli import capital_group
#from crypy.desk.order_cli import order_group

import asyncio

import crypy.desk.global_vars as gv
from crypy.desk.desk import Desk
from crypy.desk.order import Order

import crypy.config

"""Entrypoint for the desk subpackage
Manages one (currently) exchange, via CLI
"""

async def asyncLong():
    print('order creation starting')

    #exchangeName = "testnet.bitmex" #TODO temp in the end will need to test every and all exchanges
    #ticker = 'BTCUSD' #TODO temp in the end we will need to handle all traded pair for the exchange

    exchange = gv.defEXCHANGE
    ticker = gv.defPAIR

    config = crypy.config.Config()  # Loading config early to customize choice based on it.
    exchange_config = config.sections[exchange]

    print('Desk creation starting')
    async with Desk(conf=exchange_config) as desk:
        print('Desk creation done')

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
        order_type = 'Limit'
        symbol = gv.ticker2symbol[ticker]
        amount = 0.5

        print('fetching market price starting')
        marketPrice = await desk.do_fetchMarketPrice(symbol = gv.ticker2symbol[ticker])
        print('fetching market price done')
        price = marketPrice['bid'] - 250
        mexAmount = Order._mexContractAmount(currencyAmount = amount, currencyPrice = price)


        print('order creation starting')
        order = await desk.create_order(symbol=symbol, side=side, order_type=order_type, leverage=leverage,
                                      display_qty=display_qty, stop_px=stop_px, peg_offset_value= peg_offset_value, peg_price_type=peg_price_type, exec_inst=exec_inst,
                                      expiracy=expiracy,
                                      amount=amount,
                                      price=price)
        print('order creation done')


        print('order formatting starting')
        order.format(marketPrice = marketPrice)
        print('order formatting done')


        print('order execution starting')
        print(await desk.execute_order(order))
        print('order execution done')

        return 'order is passed'


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    try:
        ret = event_loop.run_until_complete(
            asyncLong()
        )
        print(f"Returned: {ret}")

    finally:
        event_loop.close()

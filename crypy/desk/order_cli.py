#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import functools
import os
import sys

import click
import prompt_toolkit

#from dataclasses import asdict
#from collections import OrderedDict

import datetime

import crypy.desk.global_vars as gv

from .order import Order
from .desk_cli import cli_root_group

desk = None

### CLI PAIR Sub Commands
@cli_root_group.group('pair')
@click.option('-t', '--ticker', default=gv.defPAIR, type=str, show_default=True)  #TODO define valid pair tickers per exchange
@click.pass_context
def order_group(ctx, ticker):
    """
    Trading a specific pair defined by its ticker
    """
    click.echo(f"PAIR: {ticker}")
    global desk
    if desk is None:
        desk = ctx.obj['desk']
    desk.ticker = ticker


def order_options_all(ctx):
    #click.option('--exec-inst', type=click.Choice(['ParticipateDoNotInitiate', 'AllOrNone', 'MarkPrice', 'IndexPrice', 'LastPrice', 'Close', 'ReduceOnly', 'Fixed']), show_default=True, help="Optional execution instructions. 'AllOrNone' instruction requires display_qty to be 0. 'MarkPrice', 'IndexPrice' or 'LastPrice' instruction valid for 'Stop', 'StopLimit', 'MarketIfTouched', and 'LimitIfTouched' orders.")(ctx)
    click.option('-exp', '--expiracy', type=str, default='none', show_default=True)(ctx) #TODO use it #todo replace by timeInForce on mex
    click.option('-id', '--id', type=str, default=None, help="id of order to update")(ctx)
    return ctx

def order_options_shortslongs(ctx):
    click.option('-ot', '--order-type', default='Limit', type=click.Choice(['Limit', 'Market']), show_default=True)(ctx) #NB: limit & market are default order types for all exchanges, others are exchange specific   
    #click.option('-lv', '--leverage', type=click.IntRange(1, 5), default=1, show_default=True)(ctx) #kraken
    click.option('-lv', '--leverage', type=click.IntRange(0, 100), default=5, show_default=True)(ctx) #bitmex leverage value: a number between 0.01 and 100. Send 0 to enable cross margin.
    click.option('--display-qty', type=int, help="Optional quantity to display in the book. Use 0 for a fully hidden order.")(ctx)
    click.argument('price', nargs=1, type=float, required=False)(ctx)
    click.argument('amount', nargs=1, type=float, required=True)(ctx)
    return ctx

def order_options_stops(ctx):
    click.option('--side', type=click.Choice(['sell', 'buy']), help="Order side.")(ctx)
    click.option('--full', type=bool, is_flag=True, default=False, show_default=True, help="Full Stop Loss and close every existing order on pair. NB: this option have precedence over amount if set.")(ctx)
    #click.option('--peg-offset-value', type=int, help="Optional trailing offset from the current price; use a negative offset for stop-sell orders and buy-if-touched orders. Optional offset from the peg price for 'Pegged' orders.")(ctx)
    #click.option('--peg-price-type', type=click.Choice(['LastPeg', 'MidPricePeg', 'MarketPeg', 'PrimaryPeg', 'TrailingStopPeg']), show_default=True, help="Optional peg price type.")(ctx)
    click.argument('amount', nargs=1, type=float, required=False)(ctx)
    return ctx

# OR use functools.partial
def make_order(ticker, order_type, expiracy, id = None, amount = None, price = None, peg_offset_value = None, peg_price_type = None, leverage = None, display_qty = None, stop_px = None, exec_inst = None):

    def partial(side):
        #nonlocal ticker, order_type, leverage, display_qty, stop_px, peg_offset_value, peg_price_type, exec_inst, expiracy, id, amount, price

        global desk
        symbol = gv.ticker2symbol[ticker]

        order = Order(exchange = desk.exchange, symbol=symbol, side=side, type=order_type, leverage=leverage, display_qty=display_qty, stop_px=stop_px, peg_offset_value=peg_offset_value, peg_price_type=peg_price_type, exec_inst=exec_inst, expiracy=expiracy, id=id, amount=amount, price=price)
        
        orderValidation = order.format(marketPrice = desk.do_fetchMarketPrice(symbol = symbol))
        if orderValidation is not None:
            return orderValidation
        
        if id is None:
            click.echo(f'Do you want to execute the following {side.upper()} on {ticker} ?') #TODO show SHORT instead of SELL and LONG instead of BUY
        else:
            click.echo(f'Do you want to change order {id} with the following {side.upper()} on {ticker} ?') #TODO show SHORT instead of SELL and LONG instead of BUY

        order.showData()

        if click.confirm('Please confirm' + ( ' (NB: if there are existing orders for the pair, it\'ll change their leverage also)' if (not leverage is None and leverage > 1) else '')): #abort (but don't die!) here if No is selected (default) otherwise continue code below
            return order.execute()
        else:
            return "order execution aborted"

    return partial


@order_group.command()
@order_options_all
@order_options_shortslongs
@click.pass_context
def short(ctx, order_type, leverage, display_qty, expiracy, id, amount, price):
    """
    Pair: Create/Update a SHORT order
    """
    side = "sell" #ccxt value
    print(make_order(ticker = desk.ticker, order_type = order_type, leverage=leverage, display_qty=display_qty, expiracy=expiracy, id = id, amount=amount, price=price)(side=side))

@order_group.command()
@order_options_all
@order_options_shortslongs
@click.pass_context
def long(ctx, order_type, leverage, display_qty, expiracy, id, amount, price):
    """
    Pair: Create/Update a LONG order
    """
    side = "buy" #ccxt value
    print(make_order(ticker = desk.ticker, order_type = order_type, leverage=leverage, display_qty=display_qty, expiracy=expiracy, id = id, amount=amount, price=price)(side=side))

@order_group.command()
@order_options_all
@order_options_stops
@click.argument('price', nargs=1, type=float, required=True)
@click.pass_context
def stop(ctx, side, full, expiracy, id, amount, price):
    """
    Pair: Set/Update a stop for a position (WARNING: ATM be careful if no position and with the --side option which might trigger a Market order (TODO abstract this))
    """
    exec_inst = 'IndexPrice'
    if full :
        exec_inst += ',Close'
        amount = None
    order_type = 'Stop'
    print(make_order(ticker = desk.ticker, order_type = order_type, stop_px=price, exec_inst=exec_inst, expiracy=expiracy, id = id, amount=amount)(side=side))

@order_group.command()
@order_options_all
@order_options_stops
@click.argument('offset-price', nargs=1, type=float, required=True)
@click.pass_context
def trailing_stop(ctx, side, full, expiracy, id, amount, offset_price):
    """
    Pair: Set/Update a trailing stop for a position (WARNING: ATM be careful if no position and with the --side option which might trigger a Market order (TODO abstract this))
    """
    exec_inst = 'IndexPrice'
    if full :
        exec_inst += ',Close'
        amount = None
    order_type = 'Pegged'
    peg_price_type = 'TrailingStopPeg'
    peg_offset_value=offset_price
    print(make_order(ticker = desk.ticker, order_type = order_type, peg_offset_value=peg_offset_value, peg_price_type=peg_price_type, exec_inst=exec_inst, expiracy=expiracy, id = id, amount=amount)(side=side))

@order_group.command()
@order_options_all
@order_options_stops
#TODO: amount in % could be useful
@click.argument('price', nargs=1, type=float, required=True)
@click.pass_context
def take_profit(ctx, side, full, expiracy, id, amount, price):
    """
    Pair: Set/Update a take profit order on a position (WARNING: ATM be careful if no position and with the --side option which might trigger a Market order (TODO abstract this))
    """
    exec_inst = 'IndexPrice'
    if full :
        exec_inst += ',Close'
        amount = None
    order_type = 'MarketIfTouched'

    print(make_order(ticker = desk.ticker, order_type = order_type, stop_px=price, exec_inst=exec_inst, expiracy=expiracy, id = id, amount=amount)(side=side))


#TODO: we might need to do trailing-stop-short, trailing-stop-long and trailing-take-profits orders
#TODO think it 'StopLimit' and take profit limit ('LimitIfTouched') orders are useful

@order_group.command()
@click.argument('ids', nargs=-1, type=str)
@click.pass_context
def cancel_order(ctx, ids):
    """
    Pair: cancel order(s)
    """
    Order.cancel(exchange=desk.exchange, order_ids=ids)

#TODO cancel all orders

@order_group.command()
@click.option('-l', '--limit', type=int, default=7, show_default=True)
@click.pass_context
def orderbook(ctx, limit):
    """
    Pair: L2 orderbook
    """
    print( Order.fetchL2OrderBook(desk = desk, symbol = gv.ticker2symbol[desk.ticker], limit = limit) )

@order_group.command()
@click.option('-s', '--since', type=datetime, show_default=True)
@click.option('-l', '--limit', type=int, default=25, show_default=True)
@click.pass_context
def last_trades(ctx, since, limit):
    """
    Pair: list of last trades (not user related)
    """
    print( desk.do_fetchTrades(symbol = gv.ticker2symbol[desk.ticker], since = since, limit = limit, customParams = {}) ) #todo customparams for exchange if needed

@order_group.command()
@click.option('-tf', '--timeframe', default='1m', type=click.Choice(['1m', '3m', '15m', '30m', '1h', '2H', '4H', '6H', '12H', '1D', '3D', '1W', '1M']), show_default=True, help="timeframe in minutes") #TODO choices must depend on exchange i suppose
@click.option('-s', '--since', type=datetime, show_default=True)
@click.option('-l', '--limit', type=int, default=50, show_default=True)
@click.pass_context
def ohlcv(ctx, timeframe, since, limit):
    """
    Pair: OHLCV data for interval in minutes
    """
    #print(gv.ticker2symbol[ctx.obj.ticker])
    print(desk.do_fetchOHLCV(symbol = gv.ticker2symbol[desk.ticker], timeframe = timeframe, since = since, limit = limit, customParams = {}) ) #todo customparams for exchange if needed

@order_group.command()
@click.pass_context
def market_price(ctx):
    """
    Pair: Current Market Price
    """
    print( 'market price: ' + str(desk.do_fetchMarketPrice(symbol = gv.ticker2symbol[desk.ticker])) )
    
@order_group.command()
@click.argument('what', type=click.Choice(['data', 'orders-all', 'orders-open', 'orders-closed', 'positions', 'trades']), default='data')
#TODO limit argument
@click.pass_context
def list(ctx, what):
    """Pair: (user) information"""
    print( desk.do_list(what = what, symbol = gv.ticker2symbol[desk.ticker], customParams = {}) )  #todo customparams for exchange if needed


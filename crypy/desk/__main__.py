#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import functools
import os
import sys

import click
from click_repl import repl as crepl
import prompt_toolkit

#from dataclasses import asdict
#from collections import OrderedDict

import datetime

import crypy.desk.global_vars as gv
from crypy.desk.desk import Desk
from crypy.desk.order import Order

"""Entrypoint for the desk subpackage
Manages one (currently) exchange, via CLI
"""

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--h', '--help', '?'])

### CLI Commands (Root)
@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.option('-e', '--exchange', default=gv.defEXCHANGE, type=click.Choice(dict(gv.exchange_data).keys()), show_default=True) #https://click.palletsprojects.com/en/7.x/options/#choice-options
@click.pass_context
def cli(ctx, exchange):
    # starting repl if no command passed
    if ctx.invoked_subcommand is None:
        prompt_toolkit.shortcuts.clear()
        click.echo(f"-== TRADING CLI ==-")
        click.echo(f"EXCHANGE: {exchange}")
        #ctx.invoke(help) #TODO invoke help cmd on startup
        ctx.exchangeName = exchange #will be available from ctx.parent.exchangeName after repl launched

        #Setup the prompt
        #https://python-prompt-toolkit.readthedocs.io/en/stable/pages/reference.html?prompt_toolkit.shortcuts.Prompt#prompt_toolkit.shortcuts.PromptSession
        prompt_kwargs = {
            'message': f"{exchange}> ",
            'history': prompt_toolkit.history.FileHistory(os.path.join(sys.path[0], 'crypy.hist')), #TODO don't use os.path
            'auto_suggest': prompt_toolkit.auto_suggest.AutoSuggestFromHistory(),
            'wrap_lines': True,
            'bottom_toolbar': [
                #('class:bottom-toolbar-logo', ' Ϟ ') #TODO setup
            ]
        }

        # launching repl
        crepl(ctx, prompt_kwargs=prompt_kwargs, allow_system_commands = False)
        

    # otherwise invoke the specified subcommand (default behavior)
    else:
        ctx.obj = Desk(exchange=ctx.parent.exchangeName)

@cli.command()
@click.pass_obj
def exchange_info(ctx):
    """print exchange info to file exg_%EXCHANGE_NAME%.txt"""
    print(ctx.do_getExchangeInfo())

@cli.command()
@click.argument('what', type=click.Choice(['data', 'orders', 'positions', 'trades']), default='data')
#TODO limit argument
@click.pass_obj
def list(ctx, what):
    """display all followed pairs informations"""
    print( ctx.do_list(what = what, customParams = {}) )  #todo customparams for exchange if needed

@cli.command()
@click.pass_context
def exit(ctx):
    """exit app by using :exit, :q, :quit"""
    print("to exit just type :exit, :q, :quit")
    #ctx.invoke(repl.exit)
    #TODO find a way to run the fucking cmd
    
@cli.command()
@click.pass_context
def balance(ctx):
    """
    Get user balance (private data)
    """
    print( ctx.obj.do_fetchBalance( customParams = {}) ) #todo customparams for exchange if needed

@cli.command()
@click.pass_context
def balance_total(ctx):
    """
    Get user total balance (private data)
    """
    print( ctx.obj.do_fetchTotalBalance( customParams = {}) ) #todo customparams for exchange if needed

@cli.command()
@click.pass_context
def balance_free(ctx):
    """
    Get user free balance (private data)
    """
    print( ctx.obj.do_fetchFreeBalance( customParams = {}) ) #todo customparams for exchange if needed

@cli.command()
@click.pass_context
def balance_used(ctx):
    """
    Get user used balance (private data)
    """
    print( ctx.obj.do_fetchUsedBalance( customParams = {}) ) #todo customparams for exchange if needed

@cli.command()
@click.pass_context
def balance_partial(ctx):
    """
    Get user partial? balance (private data)
    """
    print( ctx.obj.do_fetchPartialBalance( customParams = {}) ) #todo customparams for exchange if needed


@cli.command()
@click.option('-a', '--assets', type=str, default='all', show_default=True, help='comma delimited list of assets to restrict output to')
@click.option('-t', '--type', type=click.Choice(['all', 'deposit', 'withdrawal', 'trade', 'margin']), default='all', show_default=True, help="restrict type of ledger to retrieve")
@click.option('-s', '--since', type=datetime, show_default=True)
@click.option('-l', '--limit', type=int, default=25, show_default=True)
@click.pass_context
def ledger(ctx, assets, type, since, limit):
    """
    Get user asset ledger (private data)
    """
    #todo use assets and type params (possible w ccxt ? maybe through "code" arg ?)
    print( ctx.obj.do_fetchLedger( code = None, since = since, limit = limit, customParams = {}) ) #todo code for exchange if needed #todo customparams for exchange if needed


#@cli.command()
#@click.option('-f', '--from-address', type=str, show_default=True, help="address to withdrawal from")
#@click.option('-t', '--to-address', type=str, show_default=True, help="address to deposit to")
#@click.option('-a', '--amount', type=float, default='all', show_default=True, help="amount to transfer")
#@click.pass_context
#def transfer(ctx, from_address, to_address, amount):
#    """
#    Transfer from address to address TODO (private data)
#    """
#    print(">> TODO <<")



### CLI PAIR Sub Commands
@cli.group()
@click.option('-t', '--ticker', default=gv.defPAIR, type=str, show_default=True)  #TODO define valid pair tickers per exchange
@click.pass_context
def pair(ctx, ticker):
    """
    Trading a specific pair defined by its ticker
    """
    click.echo(f"PAIR: {ticker}")
    ctx.obj.ticker = ticker


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

        desk = click.get_current_context().obj
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


@pair.command()
@order_options_all
@order_options_shortslongs
@click.pass_context
def short(ctx, order_type, leverage, display_qty, expiracy, id, amount, price):
    """
    Pair: Create/Update a SHORT order
    """
    side = "sell" #ccxt value
    print(make_order(ticker = ctx.obj.ticker, order_type = order_type, leverage=leverage, display_qty=display_qty, expiracy=expiracy, id = id, amount=amount, price=price)(side=side))
    
    ##TEMP DEBUG
    #ctx.invoke(list, what='orders')


@pair.command()
@order_options_all
@order_options_shortslongs
@click.pass_context
def long(ctx, order_type, leverage, display_qty, expiracy, id, amount, price):
    """
    Pair: Create/Update a LONG order
    """
    side = "buy" #ccxt value
    print(make_order(ticker = ctx.obj.ticker, order_type = order_type, leverage=leverage, display_qty=display_qty, expiracy=expiracy, id = id, amount=amount, price=price)(side=side))

    ##TEMP DEBUG
    #ctx.invoke(list, what='orders')

@pair.command()
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
    print(make_order(ticker = ctx.obj.ticker, order_type = order_type, stop_px=price, exec_inst=exec_inst, expiracy=expiracy, id = id, amount=amount)(side=side))

    ##TEMP DEBUG
    #ctx.invoke(list, what='orders')

@pair.command()
@order_options_all
@order_options_stops
@click.argument('offset-price', nargs=1, type=float, required=True)
@click.pass_context
def trailing_stop(ctx, side, expiracy, id, amount, offset_price):
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
    print(make_order(ticker = ctx.obj.ticker, order_type = order_type, peg_offset_value=peg_offset_value, peg_price_type=peg_price_type, exec_inst=exec_inst, expiracy=expiracy, id = id, amount=amount)(side=side))

@pair.command()
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

    print(make_order(ticker = ctx.obj.ticker, order_type = order_type, stop_px=price, exec_inst=exec_inst, expiracy=expiracy, id = id, amount=amount)(side=side))


#TODO: we might need to do trailing-stop-short, trailing-stop-long and trailing-take-profits orders
#TODO think it 'StopLimit' and take profit limit ('LimitIfTouched') orders are useful

@pair.command()
@click.argument('ids', nargs=-1, type=str)
@click.pass_context
def cancel_order(ctx, ids):
    """
    Pair: cancel order(s)
    """
    Order.cancel(order_ids=ids)

#TODO cancel all orders

@pair.command()
@click.option('-l', '--limit', type=int, default=7, show_default=True)
@click.pass_context
def orderbook(ctx, limit):
    """
    Pair: L2 orderbook
    """
    print( Order.fetchL2OrderBook(desk = ctx, symbol = gv.ticker2symbol[ctx.obj.ticker], limit = limit) )

@pair.command()
@click.option('-s', '--since', type=datetime, show_default=True)
@click.option('-l', '--limit', type=int, default=25, show_default=True)
@click.pass_context
def last_trades(ctx, since, limit):
    """
    Pair: list of last trades (not user related)
    """
    print( ctx.obj.do_fetchTrades(symbol = gv.ticker2symbol[ctx.obj.ticker], since = since, limit = limit, customParams = {}) ) #todo customparams for exchange if needed

@pair.command()
@click.option('-tf', '--timeframe', default='1m', type=click.Choice(['1m', '3m', '15m', '30m', '1h', '2H', '4H', '6H', '12H', '1D', '3D', '1W', '1M']), show_default=True, help="timeframe in minutes") #TODO choices must depend on exchange i suppose
@click.option('-s', '--since', type=datetime, show_default=True)
@click.option('-l', '--limit', type=int, default=50, show_default=True)
@click.pass_context
def ohlcv(ctx, timeframe, since, limit):
    """
    Pair: OHLCV data for interval in minutes
    """
    #print(gv.ticker2symbol[ctx.obj.ticker])
    print( ctx.obj.do_fetchOHLCV(symbol = gv.ticker2symbol[ctx.obj.ticker], timeframe = timeframe, since = since, limit = limit, customParams = {}) ) #todo customparams for exchange if needed

@pair.command()
@click.pass_context
def market_price(ctx):
    """
    Pair: Current Market Price
    """
    print( 'market price: ' + str(ctx.obj.do_fetchMarketPrice(symbol = gv.ticker2symbol[ctx.obj.ticker])) )
    
@pair.command()
@click.argument('what', type=click.Choice(['data', 'orders', 'positions', 'trades']), default='data')
#TODO limit argument
@click.pass_context
def list(ctx, what):
    """Pair: (user) information"""
    print( ctx.obj.do_list(what = what, symbol = gv.ticker2symbol[ctx.obj.ticker], customParams = {}) )  #todo customparams for exchange if needed


if __name__ == '__main__':
    #try:
        cli()
    #except:
    #     pass

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
@click.pass_obj
def list(ctx, what):
    """display all followed pairs informations"""
    ctx.do_list(what)

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


@cli.command()
@click.option('-f', '--from-address', type=str, show_default=True, help="address to withdrawal from")
@click.option('-t', '--to-address', type=str, show_default=True, help="address to deposit to")
@click.option('-a', '--amount', type=float, default='all', show_default=True, help="amount to transfer")
@click.pass_context
def transfer(ctx, from_address, to_address, amount):
    """
    Transfer from address to address TODO (private data)
    """
    print(">> TODO <<")



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


def order_options(ctx):
    click.option('-ot', '--order-type', default='limit',
                  type=click.Choice(['limit', 'market']), show_default=True)(ctx)
    click.option('-lv', '--leverage', type=click.IntRange(1, 5), default=1, show_default=True)(ctx)
    click.option('-exp', '--expiracy', type=str, default='none',
                 show_default=True)(ctx)  # TODO use it #TODO handle datetime format
                                          # #(https://click.palletsprojects.com/en/7.x/options/#callbacks-for-validation)
    click.argument('amount_price', nargs=2, type=float)(ctx)

    return ctx


# OR use functools.partial
def make_order(ticker, order_type, leverage, expiracy, amount, price):

    def partial(side):
        nonlocal ticker, order_type, leverage, expiracy, amount, price

        click.echo(f'Do you want to execute the following {side.upper()} on {ticker} ?')

        order = Order(symbol=gv.ticker_symbol[ticker], side=side, type=order_type, leverage=leverage, expiracy=expiracy, amount=amount, price=price)
        order.showData()

        if click.confirm('Please confirm'): #abort (but don't die) here if No is selected (default) otherwise continue code below
            return order.execute()

    return partial


@pair.command()
@order_options
@click.pass_context
def short(ctx, order_type, leverage, expiracy, amount_price):
    """
    Shorting a pair
    """
    side = "sell" #ccxt value
    print(make_order(ticker = ctx.obj.ticker, order_type = order_type, leverage = leverage, expiracy = expiracy, amount=amount_price[0], price=amount_price[1])(side=side))
    
    ##TEMP DEBUG
    #ctx.invoke(list, what='orders')


@pair.command()
@order_options
@click.pass_context
def long(ctx, order_type, leverage, expiracy, amount_price):
    """
    Longing a pair
    """
    side = "buy" #ccxt value
    print(make_order(ticker = ctx.obj.ticker, order_type = order_type, leverage = leverage, expiracy = expiracy, amount=amount_price[0], price=amount_price[1])(side=side))

    ##TEMP DEBUG
    #ctx.invoke(list, what='orders')


@pair.command()
@click.argument('ids', nargs=-1, type=str)
@click.pass_context
def cancel_order(ctx, ids):
    """
    Pair cancel order(s)
    """
    Order.cancel(order_ids=ids)

@pair.command()
@click.option('-l', '--limit', type=int, default=7, show_default=True)
@click.pass_context
def orderbook(ctx, limit):
    """
    Pair L2 orderbook
    """
    print( Order.fetchL2OrderBook(symbol = gv.ticker_symbol[ctx.obj.ticker], limit = limit) )

@pair.command()
@click.option('-s', '--since', type=datetime, show_default=True)
@click.option('-l', '--limit', type=int, default=25, show_default=True)
@click.pass_context
def last_trades(ctx, since, limit):
    """
    Pair list of last trades TODO
    """
    print(">> TODO <<")

@pair.command()
@click.option('-tf', '--timeframe', default='1m', type=click.Choice(['1m', '3m', '15m', '30m', '1h', '2H', '4H', '6H', '12H', '1D', '3D', '1W', '1M']), show_default=True, help="timeframe in minutes") #TODO choices must depend on exchange i suppose
@click.option('-s', '--since', type=datetime, show_default=True)
@click.option('-l', '--limit', type=int, default=50, show_default=True)
@click.pass_context
def ohlcv(ctx, timeframe, since, limit):
    """
    Pair ohlcv data for interval in minutes
    """
    #print(gv.ticker_symbol[ctx.obj.ticker])
    print( ctx.obj.do_fetchOHLCV(symbol = gv.ticker_symbol[ctx.obj.ticker], timeframe = timeframe, since = since, limit = limit, customParams = {}) ) #todo customparams for exchange if needed
    

if __name__ == '__main__':
    cli()
    
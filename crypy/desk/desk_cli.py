#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import functools
import os
import sys
import asyncio

import click
import prompt_toolkit

#from dataclasses import asdict
#from collections import OrderedDict

import datetime

import crypy.config

import crypy.desk.global_vars as gv
from crypy.desk.desk import Desk
from crypy.desk.order import Order
from crypy.desk import repl

"""Entrypoint for the desk subpackage
Manages one (currently) exchange, via CLI
"""

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--h', '--help', '?'])

desk = None

# Loading config early to customize choice based on it.
config = crypy.config.Config()

### CLI Commands (Root)
@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.option('-e', '--exchange', default=gv.defEXCHANGE, type=click.Choice(config.sections.keys()), show_default=True) #https://click.palletsprojects.com/en/7.x/options/#choice-options
@click.pass_context
def cli_root_group(ctx, exchange):
    #ensure that ctx.obj exists and is a dict
    ctx.ensure_object(dict)

    global desk
    if desk is None:
        exchange_config = config.sections[exchange]
        desk = ctx.obj['desk'] = ctx.obj.get('desk', Desk(conf=exchange_config))

    # starting repl if no command passed
    if ctx.invoked_subcommand is None:
        crepl = repl.start_repl(ctx, exchange)

    # otherwise invoke the specified subcommand (default behavior)

@cli_root_group.command()
@click.pass_obj
def exchange_info(obj):
    """print exchange info to file exg_%EXCHANGE_NAME%.txt"""
    print(desk.do_getExchangeInfo())

@cli_root_group.command()
@click.argument('what', type=click.Choice(['data', 'orders-all', 'orders-open', 'orders-closed', 'positions', 'trades']), default='data')
@click.pass_obj
def list(obj, what):
    """display all followed pairs informations"""
    print( desk.do_list(what = what, customParams = {}) )  #todo customparams for exchange if needed

@cli_root_group.command()
@click.pass_context
def exit(ctx):
    """exit app by using :exit, :q, :quit"""
    print("to exit just type :exit, :q, :quit")
    #ctx.invoke(repl.exit)
    #TODO find a way to run the fucking cmd
    
@cli_root_group.command()
@click.argument('part', type=click.Choice(['total', 'free', 'used']), default=None, required = False)
@click.pass_context
async def balance(ctx, part):
    """
    Get user balance (private data)
    """
    print( await desk.do_fetchBalance( part = part, customParams = {}) ) #todo customparams for exchange if needed


@cli_root_group.command()
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
    print( desk.do_fetchLedger( code = None, since = since, limit = limit, customParams = {}) ) #todo code for exchange if needed #todo customparams for exchange if needed


#@cli_root_group.command()
#@click.option('-f', '--from-address', type=str, show_default=True, help="address to withdrawal from")
#@click.option('-t', '--to-address', type=str, show_default=True, help="address to deposit to")
#@click.option('-a', '--amount', type=float, default='all', show_default=True, help="amount to transfer")
#@click.pass_context
#def transfer(ctx, from_address, to_address, amount):
#    """
#    Transfer from address to address TODO (private data)
#    """
#    print(">> TODO <<")


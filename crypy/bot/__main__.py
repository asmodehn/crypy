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

"""Entrypoint for the bot subpackage
Manages one (currently) bot, via CLI
"""




### CLI Commands (Root)
@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    # starting repl if no command passed
    if ctx.invoked_subcommand is None:
        prompt_toolkit.shortcuts.clear()
        click.echo(f"-== BOT CLI ==-")

        # Setup the prompt
        # https://python-prompt-toolkit.readthedocs.io/en/stable/pages/reference.html?prompt_toolkit.shortcuts.Prompt#prompt_toolkit.shortcuts.PromptSession
        prompt_kwargs = {
            'message': f"BOT> ",
            'history': prompt_toolkit.history.FileHistory(os.path.join(sys.path[0], 'bot.hist')),
        # TODO don't use os.path
            'auto_suggest': prompt_toolkit.auto_suggest.AutoSuggestFromHistory(),
            'wrap_lines': True,
            'bottom_toolbar': [
                # ('class:bottom-toolbar-logo', ' Ϟ ') #TODO setup
            ]
        }

        # launching repl
        crepl(ctx, prompt_kwargs=prompt_kwargs, allow_system_commands = False)


    # otherwise invoke the specified subcommand (default behavior)
    else:
        ctx.obj = Desk(exchange=ctx.parent.exchangeName)

@cli.command()
@click.pass_obj
def desk_info(ctx):
    """print exchange info to file exg_%EXCHANGE_NAME%.txt"""
    print(ctx.do_getExchangeInfo())


if __name__ == '__main__':
    try:
        cli()
    except:
         pass

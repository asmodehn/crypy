#!/usr/bin/env python
# -*- coding: utf-8 -*-


import click
import prompt_toolkit

#from dataclasses import asdict
#from collections import OrderedDict


import crypy.config

import crypy.desk.global_vars as gv
from crypy.pair_manager.pair_manager import Manager
from crypy.pair_manager import repl #TODO have it inside its own package for common UI stuffs

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--h', '--help', '-?'])

manager = None

# Loading config early to customize choice based on it.
config = crypy.config.Config()

### CLI Commands (Root)
@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.option('-e', '--exchange', default=gv.defEXCHANGE, type=click.Choice(config.sections.keys()), show_default=True) #https://click.palletsprojects.com/en/7.x/options/#choice-options
@click.pass_context
def cli_root_group(ctx, exchange):
    #ensure that ctx.obj exists and is a dict
    ctx.ensure_object(dict)

    global manager
    if manager is None:
        exchange_config = config.sections[exchange]
        manager = ctx.obj['manager'] = ctx.obj.get('manager', Manager(conf=exchange_config))
    # starting repl if no command passed
    if ctx.invoked_subcommand is None:
        crepl = repl.start_repl(ctx, exchange)

    # otherwise invoke the specified subcommand (default behavior)

@cli_root_group.command()
@click.pass_obj
def info(obj):
    print(manager.info())

import click
import prompt_toolkit

import crypy.desk.global_vars as gv

from .price_action import Price_Action
from .pair_manager_cli import cli_root_group


manager = None

### CLI PRICE ACTION Sub Commands
@cli_root_group.group('pa')
@click.pass_context
def price_action_group(ctx):
    """
    Managing price action for the pair
    """
    click.echo(f"Price Action")
    global manager
    if manager is None:
        manager = ctx.obj['manager']

@price_action_group.command()
@click.pass_context
def info(ctx):
    """
    """
    PA = Price_Action(manager)
    print(PA.info())

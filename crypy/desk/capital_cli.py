import click
import prompt_toolkit

import crypy.desk.global_vars as gv

from .capital import Capital
from .desk_cli import cli_root_group


desk = None

### CLI CAPITAL manager Sub Commands
@cli_root_group.group('capital')
@click.pass_context
def capital_group(ctx):
    """
    Managing capital for the exchange (all pairs)
    """
    click.echo(f"Capital")
    global desk
    if desk is None:
        desk = ctx.obj['desk']

@capital_group.command()
@click.pass_context
def balance(ctx):
    """
    """
    capital = Capital(desk)
    print(capital.getBalance())

@capital_group.command()
@click.pass_context
def tradableAmount(ctx):
    """
    """
    capital = Capital(desk)
    print(capital.getTradableAmount())

@capital_group.command()
@click.pass_context
def status(ctx):
    """
    TODO probably the default function for the group
    """
    capital = Capital(desk)
    print(capital.getStatus())


@capital_group.command()
@click.pass_context
def receive(ctx):
    """
    """
    capital = Capital(desk)
    print(capital.receiveCapital())


@capital_group.command()
@click.pass_context
def updateModelFromTrader(ctx):
    """
    """
    capital = Capital(desk)
    print(capital.updateModelFromTrader())

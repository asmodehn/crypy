"""
Main entry point for crypy
This should interface the comand line with async functions
"""

import click
import trio

from crypy import supervisor


import click

@click.group()
def other_exchange():
    raise NotImplementedError

@other_exchange.command()
def cmd1():
    """Command on cli1"""
    raise NotImplementedError


Kraken_Supervisor = None

@click.group(invoke_without_command=True)
@click.option('--tier', default=3)
@click.option('--retry', default=.5)
@click.option('--crlsleep', default=5)
@click.pass_context
def kraken(ctx):
    global Kraken_Supervisor
    Kraken_Supervisor = supervisor.Supervisor()
    if ctx.invoked_subcommand is None:
        # default command
        kraken_watch(ctx)
    # otherwise invoke the specified subcommand

@kraken.command()
def kraken_watch():
    trio.run(Kraken_Supervisor())


@kraken.command()
def target():
    """
    Pass a trade target (with acceptable risk) to a supervisor.
    Letting the supervisor decide which strategy to adopt to reach the target.
    """
    raise NotImplementedError
    trio.run(Kraken_Supervisor())


cli = click.CommandCollection(sources=[kraken, other_exchange])

if __name__ == '__main__':
    cli()



# Create one supervisor per exchange






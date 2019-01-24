"""
Main entry point for crypy
This should interface the command line with async functions
"""
# Running a pair in one process from command line
# Note the process interface is more complex to use, but more reliable.
# Goal is to provide a process interface (supporting death and rebirth)
# and internally using a usual python API.
# this __main__ file should provide all that's needed for the process interface to be used.

import click

import crypy.config

import crypy.euc


@click.group(name='bitmex', invoke_without_command=True)
@click.option('--test', default=True)
@click.pass_context
def bitmex(ctx, test=True):
    bitmex_host = 'testnet.bitmex.com' if test else 'bitmex.com'

    # TODO : command line options override config
    bitmex_config = dict(crypy.config.config().items(bitmex_host))

    ctx.bitmex = crypy.euc.ccxt.bitmex(bitmex_config)

    if ctx.invoked_subcommand is None:
        # default command
        bitmex_balance(ctx)
    # otherwise invoke the specified subcommand (default behavior)


@bitmex.command(name='balance')
@click.pass_context
def bitmex_balance(ctx):
    """Balance from bitmex"""
    print(ctx.bitmex.fetch_balance())


@click.group(name='kraken', invoke_without_command=True)
# @click.option('--tier', default=3)
# @click.option('--retry', default=.5)
# @click.option('--crlsleep', default=5)
@click.pass_context
def kraken(ctx):
    # TODO : command line options override config
    kraken_config = dict(crypy.config.config().items('kraken.com'))

    ctx.kraken = crypy.euc.ccxt.kraken(kraken_config)

    if ctx.invoked_subcommand is None:
        # default command
        kraken_balance(ctx)
    # otherwise invoke the specified subcommand (default behavior)


@kraken.command(name='balance')
@click.pass_context
def kraken_balance(ctx):
    print(ctx.kraken.fetch_balance())


cli = click.CommandCollection(sources=[kraken, bitmex])

if __name__ == '__main__':
    cli()




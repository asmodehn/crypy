# Running an excahnge in one process from command line
# Note the process interface is more complex to use, but more reliable.
# Goal is to provide a process interface (supporting death and rebirth)
# and internally using a usual python API.
# this __main__ file should provide all that's needed for the process interface to be used.
import os
import sys

import click
from click_repl import repl as crepl
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

import crypy.config
import crypy.pair
import crypy.euc


aliases = {
    'kraken.com': ['kraken', ],
    'testnet.bitmex.com': ['testnet', 'testnet-bitmex'],  #TODO ccxt test ?
    'bitmex.com': ['bitmex', ],
}

implementations = {
    'kraken.com': lambda exc: crypy.euc.ccxt.kraken(exc),
    'testnet.bitmex.com': lambda exc: crypy.euc.ccxt.bitmex(exc), #TODO ccxt test ?
    'bitmex.com': lambda exc: crypy.euc.ccxt.bitmex(exc),
}

# Making sure we dont miss anything here
assert aliases.keys() == implementations.keys()


@click.group(name='exchange', invoke_without_command=True)
@click.option('-e', '--exchange', type=click.Choice(['kraken', 'testnet-bitmex', 'bitmex']), default='kraken')
@click.option('-v', '--verbose', is_flag=True, default=False)
@click.pass_context
def exchange_cli(ctx, exchange=None, verbose=False):

    exchange = 'kraken' if exchange is None else exchange

    # finding the actual config name for this alias
    for e, a in aliases.items():
        if exchange in a:
            exchange = e
            break

    config = dict(crypy.config.config().items(exchange))

    config['verbose'] = verbose

    ctx.obj = {
        'exchange': implementations[exchange](config),
    }


    # starting repl if no command passed
    if ctx.invoked_subcommand is None:
        prompt_kwargs = {
            'message': u'crypy> ',
            'history': FileHistory(os.path.join(sys.path[0], 'crypy.hist')),
            'auto_suggest': AutoSuggestFromHistory()
        }

        # launching repl
        crepl(ctx, prompt_kwargs=prompt_kwargs)


    # otherwise invoke the specified subcommand (default behavior)


@exchange_cli.command(name='tradable')
# We can show one or more, default to graph.
#TODO : more views
@click.option('-v', '--verbose', is_flag=True, default=False)
@click.pass_obj
def markets(obj, verbose=False):

    from pprint import pprint

    markets = {d.get('id'): d for d in obj.get('exchange').fetch_markets() if d.get('active')}

    pprint(markets)


if __name__ == '__main__':
    exchange_cli()

# Running a pair in one process from command line
# Note the process interface is more complex to use, but more reliable.
# Goal is to provide a process interface (supporting death and rebirth)
# and internally using a usual python API.
# this __main__ file should provide all that's needed for the process interface to be used.

import click

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


# "-p BTCEUR -e kraken -tf min --agregate 3"


@click.group(name='pair', invoke_without_command=True)
@click.option('-p', '--pair', default='ETH/EUR')
@click.option('-e', '--exchange', type=click.Choice(['kraken', 'testnet-bitmex', 'bitmex']), default='kraken')
@click.pass_context
def pair_cli(ctx, pair=None, exchange=None):

    pair = 'ETH/EUR' if pair is None else pair
    exchange = 'kraken' if exchange is None else exchange

    # finding the actual config name for this alias
    for e, a in aliases.items():
        if exchange in a:
            exchange = e
            break

    config = dict(crypy.config.config().items(exchange))

    ctx.obj = {
        'exchange': implementations[exchange](config),
        'pair': pair,
    }

    if ctx.invoked_subcommand is None:
        # default command
        ctx.invoke(ohlcv)
    # otherwise invoke the specified subcommand (default behavior)


@pair_cli.command(name='ohlcv')
@click.option('--timeframe', default='1h')
@click.option('--aggregate', default=3)
@click.option('--graph', default=True)  # various views are implemented as options.
@click.pass_obj
def ohlcv(obj, timeframe=None, aggregate=None, graph=True):

    timeframe = '1h' if timeframe is None else timeframe
    aggregate = 3 if aggregate is None else aggregate

    # each ohlcv candle is a list of [ timestamp, open, high, low, close, volume ]
    index = 4  # use close price from each ohlcv candle

    # get a list of ohlcv candles
    ohlcv = obj.get('exchange').fetch_ohlcv(obj.get('pair'), timeframe)

    last = ohlcv[len(ohlcv) - 1][index]  # last closing price

    # get the ohlCv (closing price, index == 4)
    series = [x[index] for x in ohlcv]

    if graph:
        print("\n" + obj.get('pair') + ' ' + timeframe + ' chart:')

        last = crypy.pair.chart(series)

        print("\n" + obj.get('exchange').name + " ₿ = $" + str(last) + "\n")  # print last closing price

    return last


if __name__ == '__main__':
    pair_cli()

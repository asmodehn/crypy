#import functools
import os
import sys
import json

import click
from click_repl import repl as crepl
import prompt_toolkit

#from dataclasses import asdict
#from collections import OrderedDict

import datetime

try:
    from ..euc import ccxt
    from .. import config
except (ImportError, ValueError):
    from crypy.euc import ccxt
    from crypy import config

defEXCHANGE = "testnet.bitmex"
defPAIR = "ETHUSD"
exchange_data = {
    "kraken": { 'confSection': "kraken.com", 'ccxtName': "kraken"},
    "bitmex": { 'confSection': "bitmex.com", 'ccxtName': "bitmex"},
    "testnet.bitmex": { 'confSection': "testnet.bitmex.com", 'ccxtName': "bitmex", 'test': True }
}
ticker_symbol = {
    'ETHUSD': 'ETH/USD',
    'XBTUSD': 'XBT/USD',
    'ETHEUR': 'ETH/EUR',
    'BTCUSD': 'BTC/USD',
    'BTCEUR': 'BTC/EUR',
    'ETHBTC': 'ETH/BTC'
    #TBC
} #todo handle multiple symbol for pair if needed

time_second = {
    '1m': 60, '3m': 180, '15m': 900, '30m': 1800, '1h': 3600, '2H': 7200, '4H': 14400, '6H': 21600, '12H': 43200, '1D': 86400, '3D': 259200, '1W': 604800, '1M': 2592000
    } #warning 1M == 30days

#nb: will be gotten from the bot in the end
#nb2 link to exchange first
wholeData = {
    'ETHUSD': {
        'data': {
            'value': 105,
            'indicators': { 'rsi': 52.01, 'ew': 'five of five of 1 up' },
            #### TIMEFRAME for data ??  ####
            'orderbook': []
        },
        'positions': [{
                'side': 'short',
                'amount': 60,
                'price': 92.19,
                'leverage': 5,
                'p/l %': 10,
                'p/l': 800
            }],
        'orders': [{
                'id': '12312155156156',
                'side': 'short',
                'type': 'limit',
                'amount': 30,
                'price': 92,
                'leverage': 5,
                'expiracy': '1 hour'
            },
            {
                'id': '2212155156156',
                'side': 'short',
                'type': 'limit',
                'amount': 35,
                'price': 96,
                'leverage': 5
            }],
        'trades': [{
                'id': '1212155156156',
                'side': 'short',
                'type': 'limit',
                'amount': 35,
                'price': 96,
                'leverage': 5,
                'datetime': '2018/05/02 15:32:12'
            },
            {
                'id': '1212155156157',
                'side': 'long',
                'type': 'limit',
                'amount': 35,
                'price': 95,
                'leverage': 5,
                'datetime': '2018/09/02 15:32:12'
            }]
    },
    'ETHEUR': {
        'data': {
            'value': 100,
            'indicators': { 'rsi': 49.01, 'ew': 'five of five of 1 up' },
            #### TIMEFRAME for data ??  ####
            'orderbook': []
        },
        'positions': [{
                'side': 'short',
                'amount': 60,
                'price': 94.19,
                'leverage': 5,
                'p/l %': 10,
                'p/l': 800
            }],
        'orders': [{
                'id': '1212155176156',
                'side': 'short',
                'type': 'limit',
                'amount': 30,
                'price': 86,
                'leverage': 5,
                'expiracy': '1 hour'
            },
            {
                'id': '1214155156156',
                'side': 'short',
                'type': 'limit',
                'amount': 34,
                'price': 76,
                'leverage': 10
            }],
        'trades': [{
                'id': '1219155156156',
                'side': 'short',
                'type': 'limit',
                'amount': 35,
                'price': 53,
                'leverage': 5,
                'datetime': '2018/05/02 16:32:12'
            },
            {
                'id': '1422155156156',
                'side': 'long',
                'type': 'limit',
                'amount': 35,
                'price': 89,
                'leverage': 5,
                'datetime': '2018/09/02 15:34:12'
            }]
    }
}

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--h', '--help'])

class Desk(object):
    def __init__(self, conf: config.Config = None, exchange=defEXCHANGE):
        self.config = conf if conf is not None else config.Config()
        self.exchangeName = (exchange or defEXCHANGE)
        exgData = exchange_data[self.exchangeName] #TODO check existance
        self.exchange = getattr(ccxt, exgData['ccxtName'])(self.config.sections[exgData['confSection']].asdict()) #TODO check exchange id existing in CCXT
        if 'test' in exgData and exgData['test']:
            self.exchange.urls['api'] = self.exchange.urls['test']  #switch the base URL to test net url
        
        self.exchange.loadMarkets(True) #preload market data. NB: forced reloading w reload=True param, do we want to always do that ? #https://github.com/ccxt/ccxt/wiki/Manual#loading-markets

    def do_getExchangeInfo(self):
        filename = 'exg_' + exchange_data[self.exchangeName]['confSection'] + '.txt'
        file = open( filename, 'w')
        print ("### HAS ###", file = file)
        print (str(self.exchange.has).replace(', ', ', \r\n'), file = file)
        print ("\r\n### SYMBOLS ###", file = file)
        print (str(self.exchange.symbols).replace(', ', ', \r\n'), file = file)
        print ("\r\n### FULL EXCHANGE DATA ###", file = file)
        print (dir(self.exchange), file = file)  #List exchange available methods
        file.close()
        #Exchange properties https://github.com/ccxt/ccxt/wiki/Manual#exchange-properties
        return 'Exchange data printed to ' + filename

    def do_list(self, arg):
        arg = "data" if arg is '' else arg
        what = {
            'data': 'data',
            'orders': 'orders',
            'positions': 'positions',
            'trades': 'trades'
        }.get(arg, "data")
        for pair in wholeData:
            print(f"{pair} {what}: {str(wholeData[pair][what])}")
    
    def _ccxtFetchXXX(self, ccxtMethod, **kwargs):
        """ccxt fetchXXX wrapper"""
        exg = self.exchange
        if not ccxtMethod in exg.has or not exg.has[ccxtMethod]:
            return f'{ccxtMethod} not available for this exchange'

        try:
            #Do we need to (re)load market everytime to get accurate data?
            ret = getattr(exg, ccxtMethod)(**kwargs)
            return ret

        except ccxt.BaseError as error:
            return error.args[0]

    def do_fetchOHLCV(self, symbol, timeframe, since, limit, customParams = {}):
        #Get data
        tohlcv = self._ccxtFetchXXX('fetchOHLCV', symbol = symbol, timeframe = timeframe, limit = limit, params = customParams) #, since = (exg.seconds()-since)
        #TODO handle exception in return

        #format data into a list
        # initialize a list to store the parsed ohlc data
        tohlcvlist = []

        for period in tohlcv:
            # Initialize an OrderedDict to garantee the column order
            tohlcvdict = dict()
            tohlcvdict["CloseTime"] = Utils.formatTS(period[0])
            tohlcvdict["Open"] = period[1]
            tohlcvdict["High"] = period[2]
            tohlcvdict["Low"] = period[3]
            tohlcvdict["Close"] = period[4]
            tohlcvdict["Volume"] = period[5] #volume in base currency
            tohlcvlist.append(tohlcvdict)

        if not tohlcvlist:
            return
        # Reverse trade list to have the most recent interval at the top
        tohlcvlist = tohlcvlist[::-1]

        return tohlcvlist

    def do_fetchBalance(self, customParams):
        return self._ccxtFetchXXX('fetchBalance', customParams = customParams)
    def do_fetchTotalBalance(self, customParams):
        return self._ccxtFetchXXX('fetchTotalBalance', customParams = customParams)
    def do_fetchFreeBalance(self, customParams):
        return self._ccxtFetchXXX('fetchFreeBalance', customParams = customParams)
    def do_fetchUsedBalance(self, customParams):
        return self._ccxtFetchXXX('fetchUsedBalance', customParams = customParams)
    def do_fetchPartialBalance(self, customParams):
        return self._ccxtFetchXXX('fetchPartialBalance', customParams = customParams)

    def do_fetchLedger(self, code, since, limit, customParams):
        return self._ccxtFetchXXX('fetchLedger', code = code, since = since, limit = limit, customParams = customParams)

### CLI Commands (Root)
@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.option('-e', '--exchange', default=defEXCHANGE, type=click.Choice(dict(exchange_data).keys()), show_default=True) #https://click.palletsprojects.com/en/7.x/options/#choice-options
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
@click.argument('what', default='data')
@click.pass_obj
def list(ctx, what):
    """display all followed pairs informations

    @param:
        data {default}: for data
        orders: for orders
        positions: for positions
        trades: for past trades
    """
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


class Order():
    """
    Order class WIP
    abstract
    """
    struct = {
        'id' : 'TBD',
        'side': 'long|short',
        'type': 'limit(default)|market|stop loss|take profit',
        'amount': 'TBD',
        'price': 'TBD',
        'leverage': '1->5(default)',
        'expiracy': 'none(default)|TBD'
    }

    def __init__(self, side, ticker, order_type, leverage, expiracy, amount, price):
        self.data = self.struct   # Copy
        self.data['side'] = side  # TODO make self.data.side immutable after __init__
        self.data['type'] = order_type 
        self.data['leverage'] = leverage 
        self.data['expiracy'] = expiracy 
        self.data['amount'] = amount 
        self.data['price'] = price 
        self.ticker = ticker

    def showData(self): 
        for k, v in self.data.items():
            print(f"¤ {k} -> {v}")

    def execute(self):
        #TODO link to exchange execute operation
        self.data['id'] = 'OU47YA-GYBTO-SRS2IJ' #TODO real orderID
        wholeData[self.ticker]['orders'].append(self.data)
        return self.data['id']

    @staticmethod
    def cancel(order_ids):
        #TODO
        print(order_ids)
        print(">> TODO <<")

    @staticmethod
    def fetchL2OrderBook(symbol, limit):
        orderbook = click.get_current_context().obj._ccxtFetchXXX('fetchL2OrderBook', symbol = 'ETH/USD', limit = limit)
        return orderbook #TODO better format i guess


### CLI PAIR Sub Commands
@cli.group()
@click.option('-t', '--ticker', default=defPAIR, type=str, show_default=True)  #TODO define valid pair tickers per exchange
@click.pass_context
def pair(ctx, ticker):
    """
    Trading a specific pair defined by its ticker
    """
    click.echo(f"PAIR: {ticker}")
    ctx.obj.ticker = ticker


def order_options(ctx):
    click.option('-ot', '--order-type', default='limit',
                  type=click.Choice(['limit', 'market', 'stop loss', 'take profit']), show_default=True)(ctx)
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

        order = Order(ticker=ticker, side=side, order_type=order_type, leverage=leverage, expiracy=expiracy, amount=amount, price=price)
        order.showData()

        click.confirm('Please confirm', abort=True) #die here if No is selected (default) otherwise continue code below

        return order.execute()

    return partial


@pair.command()
@order_options
@click.pass_context
def short(ctx, order_type, leverage, expiracy, amount_price):
    """
    Shorting a pair
    """
    side = "short"
    print(make_order(ticker = ctx.obj.ticker, order_type = order_type, leverage = leverage, expiracy = expiracy, amount=amount_price[0], price=amount_price[1])(side=side))
    
    #TEMP DEBUG
    ctx.invoke(list, what='orders')


@pair.command()
@order_options
@click.pass_context
def long(ctx, order_type, leverage, expiracy, amount_price):
    """
    Longing a pair
    """
    side = "long"
    print(make_order(ticker = ctx.obj.ticker, order_type = order_type, leverage = leverage, expiracy = expiracy, amount=amount_price[0], price=amount_price[1])(side=side))

    #TEMP DEBUG
    ctx.invoke(list, what='orders')


@pair.command()
@click.argument('ids', nargs=-1, type=str)
@click.pass_context
def cancel_order(ctx, ids):
    """
    Pair cancel order(s) TODO
    """
    order = Order.cancel(order_ids=ids)

@pair.command()
@click.option('-l', '--limit', type=int, default=7, show_default=True)
@click.pass_context
def orderbook(ctx, limit):
    """
    Pair L2 orderbook
    """
    print( Order.fetchL2OrderBook(symbol = ticker_symbol[ctx.obj.ticker], limit = limit) )

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
    #print(ticker_symbol[ctx.obj.ticker])
    print( ctx.obj.do_fetchOHLCV(symbol = ticker_symbol[ctx.obj.ticker], timeframe = timeframe, since = since, limit = limit, customParams = {}) ) #todo customparams for exchange if needed
    

class Utils:
    def formatTS(msts):
        """Format a UNIX timestamp in millesecond to truncated ISO8601 format"""
        #TODO look into import arrow https://github.com/crsmithdev/arrow
        return datetime.datetime.utcfromtimestamp(msts/1000).strftime("%Y-%m-%d %H:%M:%S")


    def ppJSON(res):
        """Pretty-print a JSON result"""
        if res is not None:
            print(json.dumps(res, indent=2))

if __name__ == '__main__':
    cli()
    
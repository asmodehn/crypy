import functools

import click

defEXCHANGE = "kraken"
defPAIR = "ETHUSD"

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

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

class Desk(object):
    def __init__(self, exchange=defEXCHANGE):
        self.exchange = (exchange or defEXCHANGE)

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


### CLI Commands (Root)
@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('-e', '--exchange', default=defEXCHANGE, type=str, show_default=True) #https://click.palletsprojects.com/en/7.x/options/#choice-options
@click.pass_context
def cli(ctx, exchange):
    click.echo(f"-== TRADING CLI ==-")
    click.echo(f"EXCHANGE: {exchange}")
    ctx.obj = Desk(exchange)

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



class Order():
    """
    Order class WIP
    abstract
    """
    struct = {
        'side': 'long|short',
        'type': 'limit(default)|market|stop loss|take profit',
        'amount': 'TBD',
        'price': 'TBD',
        'leverage': '1->5(default)',
        'expiracy': 'none(default)|TBD'
    }

    def __init__(self, side, ticker, order_type, leverage, expiracy, amount, price):
        self.data = self.struct   # copy
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
        #TODO pass order to wholeData
        #TODO real orderID
        #TODO link to exchange ops
        self.data['id'] = 'OU47YA-GYBTO-SRS2IJ'
        wholeData[self.ticker]['orders'].append(self.data)
        return self.data['id']


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


if __name__ == '__main__':
    cli()

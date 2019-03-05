import click

import copy
import types

defEXCHANGE = "kraken"
defPAIR = "ETHUSD"

#nb: will be gotten from the bot in the end
#nb2 link to exchange first
wholeData = {
    'ETHUSD': {
        'data': {
            'value': 105,
            'indicators': { 'rsi': 52.01, 'ew': 'five of five of 1 up' },
            #### TIMEFRAME for data ?? ####
            'orderbook': []
        },
        'positions': [
            {
                'side': 'short',
                'amount': 60,
                'price': 92.19,
                'leverage': 5,
                'p/l %': 10,
                'p/l': 800
            }
        ],
        'orders': [
            {
                'side': 'short',
                'type': 'limit',
                'amount': 30,
                'price': 92,
                'leverage': 5,
                'expiracy': '1 hour'
            },
            {
                'side': 'short',
                'type': 'limit',
                'amount': 35,
                'price': 96,
                'leverage': 5
            }
        ],
        'trades': [
            {
                'side': 'short',
                'type': 'limit',
                'amount': 35,
                'price': 96,
                'leverage': 5,
                'datetime': '2018/05/02 15:32:12'
            },
            {
                'side': 'long',
                'type': 'limit',
                'amount': 35,
                'price': 95,
                'leverage': 5,
                'datetime': '2018/09/02 15:32:12'
            }
        ]
    },
    'ETHEUR': {
        'data': {
            'value': 100,
            'indicators': { 'rsi': 49.01, 'ew': 'five of five of 1 up' },
            #### TIMEFRAME for data ?? ####
            'orderbook': []
        },
        'positions': [
            {
                'side': 'short',
                'amount': 60,
                'price': 94.19,
                'leverage': 5,
                'p/l %': 10,
                'p/l': 800
            }
        ],
        'orders': [
            {
                'side': 'short',
                'type': 'limit',
                'amount': 30,
                'price': 86,
                'leverage': 5,
                'expiracy': '1 hour'
            },
            {
                'side': 'short',
                'type': 'limit',
                'amount': 34,
                'price': 76,
                'leverage': 10
            }
        ],
        'trades': [
            {
                'side': 'short',
                'type': 'limit',
                'amount': 35,
                'price': 53,
                'leverage': 5,
                'datetime': '2018/05/02 16:32:12'
            },
            {
                'side': 'long',
                'type': 'limit',
                'amount': 35,
                'price': 89,
                'leverage': 5,
                'datetime': '2018/09/02 15:34:12'
            }
        ]
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


### CLI Commands
@click.group()
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

    def __init__(self, side):
        self.data = self.struct   # copy
        self.data['side'] = side  # TODO make self.data.side immutable after __init__
        self.changes = []

        def changekey(key):
            def changeval(me, val):
                me.changes += [(key, val)]
                # TODO value checking
                # TODO defaults
            return changeval

        for k in self.data.keys():
            change_cmd = types.MethodType(changekey(k), self)
            setattr(self, 'do_' + k, change_cmd)

        #super().__init__(prompt_apd if prompt_apd is None else prompt_apd)

    
        # opening
        print("--> format: ")
        for k, v in self.data.items():
            print(f"¤ {k} -> {v}")

    #    super().preloop()

    #def postloop(self):
    #    try:
    #        update = input(f"Do you want to {self.data['side'].upper()} the current pair (TODO display pair) w the following order (TODO display order info) ? [y/n]")
    #        if update not in ['n', 'no']:
    #            self.apply_changes(self.data)
    #    except EOFError:
    #        print("Everything has been cancelled, input has been closed.")

    #    super().postloop()

    #def apply_changes(self, mut_d):
    #    for c in self.changes:
    #        # apply changes
    #        mut_d[c[0]] = c[1]

    #def do_undo(self, arg):
    #    self.changes.pop()

    def do_show(self, arg):
        c = copy.deepcopy(self.data)
        self.apply_changes(c)

        for k, v in c.items():
            print(f"¤ {k} -> {v}")


class Short(Order):
    """
    Short class
    """
    def __init__(self):
        super().__init__(side="short")

class Long(Order):
    """
    Long class
    """
    def __init__(self):
        super().__init__(side="long")


### CLI PAIR Sub Commands
@cli.group()
@click.option('-t', '--ticker', default=defPAIR, type=str, show_default=True)  #TODO define valid pair
@click.pass_obj
def pair(ctx, ticker):
    """
    Trading a specific pair defined by its ticker
    """
    click.echo(f"PAIR: {ticker}")
    ctx.ticker = ticker

@pair.command()
@click.pass_obj
def short(ctx):
    """
    Shorting a pair
    """
    click.echo(f'defining short order on {ctx.ticker}')
    Short()

if __name__ == '__main__':
    cli()


#Example USAGE ATM:
#python cli2.py --exchange %exchange_name% list [data|orders|positions|trades]
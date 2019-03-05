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

@click.group()
def Desk():
    pass

@click.command()
@click.argument('what')
def list(what):
    """display all followed pairs informations

    @param:
        data {default}: for data
        orders: for orders
        positions: for positions
        trades: for past trades
    """
    arg = "data" if arg is '' else arg
    what = {
        'data': 'data',
        'orders': 'orders',
        'positions': 'positions',
        'trades': 'trades'
    }.get(arg, "data")
    for pair in wholeData:
        print(f"{pair} {what}: {str(wholeData[pair][what])}")    

@click.command()
def pair():
    """
    Uses a specific pair. Choose one of [ETHUSD, ETHEUR]
    """
    click.echo('pair used')

Desk.add_command(list)
Desk.add_command(pair)

if __name__ == '__main__':
    Desk()


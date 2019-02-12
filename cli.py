import cmd
import os
import random
import sys

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


class StackableCmd(cmd.Cmd):
    # Note the cmd.Cmd super class is shared between subclasses : careful managing it's state...
    def __init__(self, prompt_apd, completekey='tab', stdin=None, stdout=None):
        # managing class state
        self._old_prompt = self.prompt
        self._apd_prompt = prompt_apd
        super().__init__(completekey=completekey, stdin=stdin, stdout=stdout)

    def precmd(self, line):
        return line

    def postcmd(self, stop, line):
        return stop

    def preloop(self):
        # using loop to easily manage the cmd.Cmd state
        # TODO : functional design with immutable state for clarity
        self.prompt = self._old_prompt + self._apd_prompt + ">"

    def postloop(self):
        # using loop to easily manage the cmd.Cmd state
        # TODO : functional design with immutable state for clarity
        self.prompt = self.prompt.split('>')[:-1]

    def do_exit(self, arg):
        return True

    def do_EOF(self, arg):
        # BROKEN : stdin stays closed ?
        # TODO : fixit
        return True


# class Trader(StackableCmd):
#     def preloop(self):
#         print("entering position")
#
#     def postloop(self):
#         print("exiting position")
#
# class Holder(StackableCmd):
#
#     def preloop(self):
#         print("managing assets")
#         with open(os.dup(sys.stdin.fileno()), sys.stdin.mode) as stdin:
#             t = Trader(self.prompt + pair, stdin=stdin)
#
#             t.cmdloop(f"Position on {pair}")


class Pair(StackableCmd):
    def __init__(self, prompt_apd: str, usedPair: str = None):
        self.usedPair = defPAIR if usedPair is None else usedPair.upper()

        # minimum of validation
        if self.usedPair not in wholeData.keys():
            raise RuntimeError("Unknown Pair")

        super().__init__(prompt_apd=prompt_apd)

    def preloop(self):
        print("managing pair " + self.usedPair)
        super().preloop()

    # all commands below are subcommand available when the pair is define above
    def do_list_data(self):
        print(f"displaying {self.usedPair} infos (price, graph, analisys, indicators)")
        print(wholeData[self.usedPair].data)

    def do_orders(self, arg):
        print(f"displaying {self.usedPair} current orders")
        print(wholeData[self.usedPair].get('orders'))

    def do_list_positions(self):
        print(f"displaying {self.usedPair} current positions")
        print(wholeData[self.usedPair].positions)

    def do_list_trades(self):
        print(f"displaying {self.usedPair} trades histo")
        print(wholeData[self.usedPair].trades)

    # NB: ALL "OPEN" commands below will need their UPDATE & CANCEL counter parts
    def do_open_long(self, amount, price, type, leverage, expiracy):
        print(f"open {self.usedPair} long position")
        # TODO: allow a target_close_order and a stop_sell_order to be define at the same time and simultaneously executed/canceled (ie the first one executed cancel the other one)

    def do_open_short(self, amount, price, type, leverage, expiracy):
        print(f"open {self.usedPair} short position")
        # TODO: allow a target_close_order and a stop_buy_order to be define at the same time and simultaneously executed/canceled (ie the first one executed cancel the other one)

    def do_open_position_trailing_stop_percent(self, percent):
        print(f"define {self.usedPair} trailing stop in percent")
        # todo linkable/delinkable to targets_values #todo? mutually exclusive w stop_value

    def do_open_position_trailing_stop_value(self, value):
        print(f"define {self.usedPair} trailing stop value")
        # todo linkable/delinkable to targets_values #todo? mutually exclusive w stop_percent

    def do_open_position_targets_values(self, values, percents):
        print(f"define {self.usedPair} target values|percents (nb: must support both arrays and number as params)")
        # todo linkable/delinkable to trailing_stop_XXX


# Desk is not a stackable command.
# it is the main entry point to all the other (sub/stackable) commands
class Desk(cmd.Cmd):

    def __init__(self, prompt=None):

        self.prompt = ("desk" if prompt is None else prompt) + ">"
        super().__init__()

    def do_list_positions(self):
        print(f"list all current positions for all pairs")
    def do_list_orders(self):
        print(f"list all current orders for all pairs")
    def do_list_trades(self):
        print(f"list all past trades for all pairs")


    def do_exit(self, arg):
        return True

    def do_EOF(self, arg):
        # BROKEN : stdin stays closed ?
        # TODO : fixit
        return True


    def do_pair(self, pair="ETHUSD"):
        """
        Uses a specific pair. Choose one of [ETHUSD, ETHEUR]
        """
        Pair.prompt = self.prompt  # patching class prompt, as beginning of the prompt stack
        pair = defPAIR if pair is '' else pair.upper()
        t = Pair(prompt_apd=pair, usedPair=pair)
        t.cmdloop()


'''
    def do_invest(self, asset="EUR"):

        with open(os.dup(sys.stdin.fileno()), sys.stdin.mode) as stdin:
            h = Holder(self.prompt + asset, stdin=stdin)
            c = random.randint(0,255)
            h.cmdloop(f"Assets : {c} {asset}")

    def do_trade(self, pair=defPAIR):

        with open(os.dup(sys.stdin.fileno()), sys.stdin.mode) as stdin:
            t = Trader(self.prompt + pair, stdin=stdin)
            t.cmdloop("Trading ETHUSD")
'''

# prototype of command user interface
if __name__ == '__main__':

    try:
        d = Desk(sys.argv[1])
    except Exception:
        d = Desk("kraken")
    d.cmdloop("Welcome !")



import cmd
import copy
import types

import functools
import os
import random
import sys

from ast import literal_eval

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


class Truc(StackableCmd):
    """
    undoable changes in a dict
    """

    def __init__(self, prompt_apd: str = None, data=None):
        self.data = {} if data is None else data
        self.changes = []

        def changekey(key):
            def changeval(me, val):
                me.changes += [(key, val)]
            return changeval

        for k in data.keys():
            change_cmd = types.MethodType(changekey(k), self)
            setattr(self, 'do_' + k, change_cmd)

        super().__init__(prompt_apd="truc" if prompt_apd is None else prompt_apd)

    def preloop(self):
        # opening
        print("opening data : ")
        for k, v in self.data.items():
            print(f"-{k} -> {v}")

        super().preloop()

    def postloop(self):

        try:
            update = input("update? [y/n]")
            if update not in ['n', 'no']:
                self.apply_changes(self.data)
        except EOFError:
            print("Everything has been cancelled, input has been closed.")

        super().postloop()

    def apply_changes(self, mut_d):
        for c in self.changes:
            # apply changes
            mut_d[c[0]] = c[1]

    def do_undo(self, arg):
        self.changes.pop()

    def do_show(self, arg):
        c = copy.deepcopy(self.data)
        self.apply_changes(c)

        for k, v in c.items():
            print(f"-{k} -> {v}")


class Pair(StackableCmd):
    def __init__(self, prompt_apd: str, usedPair: str = None):
        self.usedPair = defPAIR if usedPair is None else usedPair.upper()

        # minimum of validation
        if self.usedPair not in wholeData.keys():
            raise RuntimeError("Unknown Pair")

        super().__init__(prompt_apd=prompt_apd)

    def preloop(self):
        print("using pair " + self.usedPair)
        super().preloop()

    def do_list(self, arg):
        """display current pair informations
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

        print( f"{self.usedPair} {what}: {str(wholeData[self.usedPair][what])}" )

    # NB: ALL "OPEN" commands below will need their UPDATE & CANCEL counter parts
    def do_long(self, type, amount, price, leverage, expiracy):
        print(f"open {self.usedPair} long position")
        # TODO: allow a target_close_order and a stop_sell_order to be define at the same time and simultaneously executed/canceled (ie the first one executed cancel the other one)

    def do_short(self, arg="(type, amount, price, leverage, expiracy)"):
        print(f"open {self.usedPair} short position")
        print(arg)  #arg {"type": "limit", "amount": 50, "price":  100, "leverage": 5}
        info = literal_eval(arg)
        default = {"type": "limit", "amount": 50, "price":  100, "leverage": 5}
        arg if arg is not None else default
        print(info)

        wholeData[self.usedPair]['orders'].append({
            'side': 'short',
            'type': info.type,
            'amount': info.amount,
            'price': info.price,
            'leverage': info.leverage,
            'expiracy': info.expiracy if info.expriracy is not None else 'None'
        })
        # TODO confirmation
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

    def do_exit(self, arg):
        return True

    def do_EOF(self, arg):
        # BROKEN : stdin stays closed ?
        # TODO : fixit
        return True


    def do_list(self, arg):
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
            print( f"{pair} {what}: {str(wholeData[pair][what])}" )

    def do_pair(self, pair="ETHUSD"):
        """
        Uses a specific pair. Choose one of [ETHUSD, ETHEUR]
        """
        Pair.prompt = self.prompt  # patching class prompt, as beginning of the prompt stack
        pair = defPAIR if pair is '' else pair.upper()
        t = Pair(prompt_apd=pair, usedPair=pair)
        t.cmdloop()

    def do_truc(self, arg):

        # using stub data
        arg = {
            'machin': 42,
            'truc' : 'is the',
            'bidule': 'answer'
        }

        Truc.prompt = self.prompt  # patching class prompt, as beginning of the prompt stack
        t = Truc(data = arg)
        t.cmdloop()

        print("new data : ")
        print(arg)


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



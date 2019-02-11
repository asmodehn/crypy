import cmd
import os
import random
import sys

defPAIR = "ETHUSD"

class StackableCmd(cmd.Cmd):
    def __init__(self, prompt, completekey='tab', stdin=None, stdout=None):
        self.prompt = prompt + ">"
        super().__init__(completekey=completekey, stdin=stdin, stdout=stdout)

    def precmd(self, line):
        return line

    def postcmd(self, stop, line):
        return stop

    def preloop(self):
        pass

    def postloop(self):
        pass

    def do_exit(self, arg):
        return True

    def do_EOF(self, arg):
        # BROKEN : Closes stdin
        # TODO : fixit
        return True


class Trader(StackableCmd):
    def preloop(self):

        print("entering position")

    def postloop(self):

        print("exiting position")


class Holder(StackableCmd):

    def preloop(self):

        print("managing assets")

    def do_trade(self, pair="EUR/ETH"):

        with open(os.dup(sys.stdin.fileno()), sys.stdin.mode) as stdin:
            t = Trader(self.prompt + pair, stdin=stdin)

            t.cmdloop(f"Position on {pair}")


# prototype of command user interface

class Desk(StackableCmd):
    def do_list_positions(self):
        print(f"list all current positions for all pairs")
    def do_list_orders(self):
        print(f"list all current orders for all pairs")
    def do_list_trades(self):
        print(f"list all past trades for all pairs")

    def do_use_pair(self, pair=defPAIR):
        print(f"Trading on {pair}")

    #all commands below are subcommand available when the pair is define above
        def do_list_pair_data(self, pair=defPAIR):
            print(f"displaying {pair} infos (price, graph, analisys, indicators)")

        def do_list_pair_orders(self, pair=defPAIR):
            print(f"displaying {pair} current orders")

        def do_list_pair_positions(self, pair=defPAIR):
            print(f"displaying {pair} current positions")

        def do_list_pair_trades(self, pair=defPAIR):
            print(f"displaying {pair} trades histo")

        # NB: ALL "OPEN" commands below will need their UPDATE & CANCEL counter parts
        def do_open_long(self, pair=defPAIR, amount, price, type, leverage, expiracy):
            print(f"open {pair} long position")
            #TODO: allow a target_close_order and a stop_sell_order to be define at the same time and simultaneously executed/canceled (ie the first one executed cancel the other one)

        def do_open_short(self, pair=defPAIR, amount, price, type, leverage, expiracy):
            print(f"open {pair} short position")
            #TODO: allow a target_close_order and a stop_buy_order to be define at the same time and simultaneously executed/canceled (ie the first one executed cancel the other one)

        def do_open_position_trailing_stop_percent(self, pair=defPAIR, percent):
            print(f"define {pair} trailing stop in percent")
            #todo linkable/delinkable to targets_values #todo? mutually exclusive w stop_value

        def do_open_position_trailing_stop_value(self, pair=defPAIR, value):
            print(f"define {pair} trailing stop value")
            #todo linkable/delinkable to targets_values #todo? mutually exclusive w stop_percent

        def do_open_position_targets_values(self, pair=defPAIR, values, percents):
            print(f"define {pair} target values|percents (nb: must support both arrays and number as params)")
            #todo linkable/delinkable to trailing_stop_XXX



    def do_invest(self, asset="EUR"):

        with open(os.dup(sys.stdin.fileno()), sys.stdin.mode) as stdin:
            h = Holder(self.prompt + asset, stdin=stdin)
            c = random.randint(0,255)
            h.cmdloop(f"Assets : {c} {asset}")

    def do_trade(self, pair=defPAIR):

        with open(os.dup(sys.stdin.fileno()), sys.stdin.mode) as stdin:
            t = Trader(self.prompt + pair, stdin=stdin)
            t.cmdloop("Trading ETHUSD")


if __name__ == '__main__':

    try:
        d = Desk(sys.argv[1])
    except Exception:
        d = Desk("kraken")
    d.cmdloop("Welcome !")



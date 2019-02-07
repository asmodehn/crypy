import cmd
import os
import random
import sys


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

    def do_watch(self, pair="EUR/ETH"):
        print(f"displaying {pair}")

    def do_invest(self, asset="EUR"):

        with open(os.dup(sys.stdin.fileno()), sys.stdin.mode) as stdin:
            h = Holder(self.prompt + asset, stdin=stdin)
            c = random.randint(0,255)
            h.cmdloop(f"Assets : {c} {asset}")

    def do_trade(self, pair="EUR/ETH"):

        with open(os.dup(sys.stdin.fileno()), sys.stdin.mode) as stdin:
            t = Trader(self.prompt + pair, stdin=stdin)
            t.cmdloop("Trading EUR/ETH")


if __name__ == '__main__':

    try:
        d = Desk(sys.argv[1])
    except Exception:
        d = Desk("kraken")
    d.cmdloop("Welcome !")



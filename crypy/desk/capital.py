"""
One capital manager per exchange
ControlFlow is opposite of order
"""

try:
    from ..euc import ccxt
    from .model.balance import BalanceAll
except (ImportError, ValueError, ModuleNotFoundError):
    from crypy.euc import ccxt
    from crypy.desk.model.balance import BalanceAll


class Capital:

    def __init__(self, desk):
        self.desk = desk

        self.open_orders = None  # unknown, not empty.
        self.balance = None

    def update(self):
        """
        Queries the exchange to update local knowledge
        :return:
        """
        #self.open_orders = self.desk.do_()
        self.balance = self.desk.balance
        return self

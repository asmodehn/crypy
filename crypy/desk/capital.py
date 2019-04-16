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

    def getStatus(self, ticker = None):
        """
        Return capital status for a specific ticker or all
        Format TBD
        TODO
        """
        pass

    def getTradableAmount(self, ticker = None):
        """
        Return tradable amount for a ticker or default amount if not specified.
        Depending on Capital Management strategy
        TODO
        """
        pass

    def getBalance(self, ticker = None, tf = None):
        """
        Return beautified balance
        For a specific ticker if defined or all (default)
        If @param tf is specified, additionnaly return PL in value and % for the specified timeframe
        TODO
        """
        return "WIP"

    def updateModelFromTrader(self):
        """
        Update local knowledge using info sent by the trader (order set not filled for a position => capital not yet used but might be, ...)
        TODO
        """
        pass

    def receiveCapital(self, mount, ticker):
        """
        Get capital amount for a ticker in update internal knowledge
        """
        pass
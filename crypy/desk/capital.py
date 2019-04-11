"""
One capital manager per exchange
ControlFlow is opposite of order
"""

from dataclasses import dataclass
import typing

try:
    from ..euc import ccxt
    from .symbol import Currency
except (ImportError, ValueError, ModuleNotFoundError):
    from crypy.euc import ccxt
    from crypy.desk.symbol import Currency


@dataclass(frozen=True)  # prevent accidental change
class Balance:

    free: float
    used: float
    total: float


@dataclass(frozen=True)  # prevent accidental change
class BalanceAll:

    free: typing.Dict[Currency, float]
    used: typing.Dict[Currency, float]
    total: typing.Dict[Currency, float]

    def per_currency(self, currency_list: typing.Optional[typing.List[Currency]] = None):
        balances = {}
        for c in currency_list:

            balances.update({
                c:Balance(
                free=self.free.get(c, 0),
                used=self.used.get(c, 0),
                total=self.total.get(c, 0)
            )
                             })


class Capital:

    def __init__(self, exchange):
        self.exg = exchange

        self.open_orders = None  # unknown, not empty.
        self.balance = None

    def update(self):
        """
        Queries the exchange to update local knowledge
        :return:
        """
        self.open_orders = self.exg.fetch_open_orders()
        b = self.exg.fetch_balance()
        self.balance = BalanceAll(**{e: b.get(e) for e in ['free', 'used', 'total']})
        return self

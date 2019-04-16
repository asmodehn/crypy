"""
Model for crypto balance
"""

from dataclasses import dataclass
import typing

try:
    from desk.model.symbol import Currency
except (ImportError, ValueError, ModuleNotFoundError):
    from desk.model.symbol import Currency


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

    def per_currency(
        self, currency_list: typing.Optional[typing.List[Currency]] = None
    ):
        balances = {}
        for c in currency_list:

            balances.update(
                {
                    c: Balance(
                        free=self.free.get(c, 0),
                        used=self.used.get(c, 0),
                        total=self.total.get(c, 0),
                    )
                }
            )

        return balances
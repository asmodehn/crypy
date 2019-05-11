import typing
from dataclasses import dataclass, field


class PriceAmount(typing.NamedTuple):
    price: float
    amount: float


@dataclass
class RiskReward:
    """
    A class to evaluate a market through a risk/reward perspective
    """

    stoploss: float
    profit: float
    entry: float

    def risk(self):
        return self.entry - self.stoploss

    def reward(self):
        return self.profit - self.entry

    def __repr__(self):
        return f"{repr(self.reward)}:{repr(self.risk)}"

    def __call__(self, next_value):
        """
        Adjusting the current targets, attempting to keep the same RiskReward Ratio
        :param current: current value
        :param estimated: forecasted value
        :return:
        """

        return adjustment


@dataclass
class Order:
    bids: typing.List[float] = field(default_factory=list)
    asks: typing.List[float] = field(default_factory=list)

    def bid(self, pa: PriceAmount):
        self.bids.append(pa)

    def ask(self, pa: PriceAmount):
        self.asks.append(pa)


@dataclass
class Position:
    """ A class modelizing an open position """

    order: Order

    rr: RiskReward

    def __call__(self, constant_rr=True):
        """ Keep monitoring and adjusting the position """

        # get ohlcv

        # forecast future position (how far?)

        # adjust RR






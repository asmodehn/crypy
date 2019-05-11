import pandas

import typing
from dataclasses import dataclass, field

from .errors import ExchangeError
from .market import Market
from .symbol import Symbol
from .ticker import Ticker


@dataclass
class Exchange:
    """
    The common Exchange interface for all implementations, as a dataclass
    """
    apiKey: typing.Optional[str] = field(default=None, repr=False)
    secret: typing.Optional[str] = field(default=None, repr=False)
    timeout: int = 30000  # TODO : units ?
    ratelimited: bool = True
    verbose: bool = True

    @property
    def markets(self)-> typing.List[Market]:
        return  # TODO : proper and safe error/non-implementation signalling ?

    def tickers(self, slist: typing.List[Symbol]) -> typing.List[Ticker]:
        return [ self.ticker(s) for s in slist ]

    def ticker(self, s: Symbol) -> Ticker:
        return  # TODO : proper and safe error/non-implementation signalling ?

    def ohlcv(self, s: Symbol, timeframe='1d', since=None, limit=None, params=None) -> pandas.DataFrame:
        return  # TODO : proper and safe error/non-implementation signalling ?


exchange_host_id_mapping = {
    "kraken": ["kraken.com"],
    "bitmex": ["testnet.bitmex.com", "bitmex.com"]
}


def exchange(hostname: str = "localhost", impl: str = "ccxt", **kwargs) -> Exchange:
    # dynamically import and initializes the client API implementation library
    import importlib
    impl = importlib.import_module(f"impl.{impl}", package=__package__)

    exgconstruct = None
    for id, h in exchange_host_id_mapping.items():
        if hostname in h:
            assert id in vars(impl)  # make sure the method with the proper id is available
            exgconstruct = getattr(impl, id)
            break

    if exgconstruct is None:
        raise ExchangeError(f"Unsupported implementation {impl} for hostname {hostname}")

    return exgconstruct(**kwargs)

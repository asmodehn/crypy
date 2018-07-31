"""
Provides a class as a common interface for all implemented exchanges API, using delegation.
"""

from enum import Enum


class Exchange_Impl(Enum):
    Bad = 0
    Kraken = 1


# Aliases
Bad = Exchange_Impl.Bad
Kraken = Exchange_Impl.Kraken


class Exchange:
    """
    Exchange class interface
    TODO : review & improve design
    """
    def __init__(self, implementation: Exchange_Impl) -> None:
        if implementation == Exchange_Impl.Kraken:
            from . import kraken
            self.impl = kraken.init_api()
        else:
            from . import bad
            self.impl = bad.init_api()

    def server_time(self):
        dt, unixtime = self.impl.get_server_time()
        return self



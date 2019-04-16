from __future__ import annotations

"""
A supervisor class, to be used in an async context.
One supervisor manages one exchange and its traders
"""
import datetime
import time
from typing import List

import trio
from .exchange import Exchange, Kraken, Bad


class Currency:
    """ Specific object to manipulate currency properly, as a measure unit"""

    def __init__(self, identifier: str) -> None:
        self.identifer = identifier


    def __repr__(self):
        return self.identifer


    def __str__(self):
        return self.identifer



class Supervisor:
    """
    A Supervisor is in charge of watching one exchange. Then:
    - Sends to storage everything that was seen regarding the exchange itself (not each currency pair)
    - Provides an interface for doing exchanges evaluation (TODO : improve that part with simple decision making, to be able to follow and adjust indicators)
    - Logs any trade from exchange to bank and vice versa.
    """

    def __init__(self, exchange: Exchange = Exchange(Bad), *base_currencies: List[Currency]) -> None:
        self.exchange = exchange
        self.base_currency = base_currency


        #discover minimal exchange initialization data.
        # Exchange is accessible or we die.
        with trio.move_on_after(10):
            await self._adjust_time_sync()

        # We need to make sure our base currencies are tradeable

        #self.exchange.get_asset_info()

        #self.exchange.get_asset_pairs()

    def _adjust_time_sync(self):
        """
        Calls the Exchange API to retrieve the server time.
        Stores the time delta between local and remote.
        Amortizes the time differences to minimize requests needed
        and maximize accuracy.
        :return:
        """
        dt, unixtime = self.exchange.get_server_time()
        local_dt = datetime.datetime()
        local_unixtime = time.time()

        # TODO : amortize this...
        self.datetime_delta = local_dt - dt
        self.timedelta = local_unixtime - unixtime

        return 5  # TODO : improve that

    async def _adjust_time(self):
        self._adjust_time_sync()
        # TODO: reschedule for the next time we need to actually check.


    ### PUBLIC ASYNC FRIENDLY INTERFACE ###

    @property
    def datetime(self):
        """Estimate the current time of the exchange, based on the delta periodically calculated"""
        return datetime.datetime() + self.datetime_delta

    @property
    def time(self):
        """Estimate the current time of the exchange, based on the delta periodically calculated"""
        return time.time() + self.timedelta

    async def __call__(self, *args, **kwargs):
        # starts the time proxy
        await self._adjust_time()

        # discover currency pairs


        #async with trio.open_nursery() as nursery:
            # spanws a trader for each currency pair


            #nursery.start_soon(child)
            #nursery.start_soon(child)

            # traders will keep running, and die whenever the currency pair streams dies (cannot be watched any longer) for any reason


            # supervisor can attempt to restart them or not, depending on the error received from the API


        #TMP : Time proxy must go on forever, until we break it...
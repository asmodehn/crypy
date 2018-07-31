"""
Bad Exchange simultion
This is used in test, to verify our assumptions still hold, and until when.

Useful for latency, bandwith, safety, and other real world issues...
"""

import time
import datetime
import random


class BadExchange():

    def __init__(self, max_delay: int =10) -> None:
        """
        Simulating the real world in one class...
        :param max_delay: the maximum delay we want to test for.
        """
        self.max_delay = max_delay

    def get_server_time(self):
        # adding random delay before server time computation
        time.sleep(random.randint(0, self.max_delay//2))
        # adding random delay to our time
        delay = random.randint(-self.max_delay, self.max_delay)
        dt = datetime.datetime.now() + datetime.timedelta(seconds=delay)
        unixtime = time.time() + delay
        # adding random delay after server time computation
        time.sleep(random.randint(0, self.max_delay//2))
        return dt, unixtime


def init_api():
    return BadExchange()


if __name__ == '__main__':
    # Basic read-only test of the interface (using actual exchange - see tests for using mock instead)

    bad = init_api()

    dt, unixtime = bad.get_server_time()
    print("Server Time:")
    print(dt)
    print(unixtime)

    print("Local Time:")
    print(datetime.datetime.now())
    print(time.time())

    #assets = kraken.get_asset_info()
    #print(assets)

    #tradable_pairs = kraken.get_tradable_asset_pairs()
    #print(tradable_pairs)

    #ohlc, data = init_api().get_ohlc_data("EUR", "GBP")
    #print (ohlc)

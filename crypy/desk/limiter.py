import typing

import functools
import time
from . import errors

from requests import HTTPError


"""This module implements rate limiter for function call"""

# https://support.kraken.com/hc/en-us/articles/206548367-What-is-the-API-call-rate-limit-


class CallRateLimitError(Exception):
    pass


class CallProfiler(typing.NamedTuple):
    """
    An immutable data structure to track function calls times.
    """
    last_call: float
    frequency: float = 0.2
    sleep: typing.Callable = time.sleep


def limiter(profiler: CallProfiler = CallProfiler(last_call = time.time())):
    """
    a limiter to use as a decorator.
    :param profiler: A profiler can be passed. useful to limit a group of functions together as one
     The last_call members default to now, to allow adding/removing limiter dynamically
      without triggering a burst of call unintentionally.
    :return: a decorator to apply to the function you want to limit.
    """

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            nonlocal profiler
            profiler = profiler
            now = time.time()

            period = 1 / profiler.frequency
            # if we need to, we wait... (note we can also async wait...)
            if now - profiler.last_call < period:
                profiler.sleep(period - (now - profiler.last_call))

            profiler = CallProfiler(last_call=time.time(), frequency=profiler.frequency, sleep=profiler.sleep)
            return func(*args, **kwargs)

        return wrapper

    return decorator

############ from pykrakenapi

def crl_sleep(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        self = args[0]
        crl_sleep = self.crl_sleep

        # raise CallRateLimitError if crl sleep is deactivated
        if crl_sleep == 0:
            result = func(*args, **kwargs)
            return result

        # otherwise, retry after "crl_sleep" seconds
        while True:
            try:
                result = func(*args, **kwargs)
                return result
            except CallRateLimitError as err:
                print(err, '\n sleeping for {} seconds'.format(crl_sleep))
                time.sleep(crl_sleep)
                continue

    return wrapper


def callrate_limiter(query_type):
    def decorate_func(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """Call rate limit counter.

            Implementation of a call rate limiter as a decorator. If the call
            rate limit is reached, api calls will be blocked.

            See https://support.kraken.com/hc/en-us/articles/206548367

            """

            self = args[0]

            # determine increment
            if query_type == 'ledger/trade history':
                incr = 2
            elif query_type == 'other':
                incr = 1

            # decrease api counter
            self._decrease_api_counter()

            # return api call
            if self.api_counter < self.limit:
                # no retries
                if self.retry == 0:
                    self.api_counter += incr
                    result = func(*args, **kwargs)
                    return result
                # do retries
                else:
                    attempt = 0
                    while self.api_counter < self.limit:
                        try:
                            self.api_counter += incr
                            result = func(*args, **kwargs)
                            return result
                        except (HTTPError, errors.CrypyException) as err:
                            print('attempt: {} |'.format(
                                str(attempt).zfill(3)), err)
                            attempt += 1
                            time.sleep(self.retry)
                            self._decrease_api_counter()
                            continue

            # raise error if limit exceeded
            msg = ("call rate limiter exceeded (counter={}, limit={})")
            msg = msg.format(str(self.api_counter).zfill(2),
                             str(self.limit).zfill(2))
            raise CallRateLimitError(msg)

        return wrapper
    return decorate_func




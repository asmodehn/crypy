import typing
import functools
from dataclasses import dataclass, field
import time

try:  # relative imports
    from . import errors
except ImportError:
    # load from installed package instead of source
    # useful for incremental (module per module) changes
    from crypy.desk import errors

from requests import HTTPError


"""This module implements rate limiter for function call"""

# https://support.kraken.com/hc/en-us/articles/206548367-What-is-the-API-call-rate-limit-


class CallRateLimitError(Exception):
    pass


@dataclass
class Limiter:
    """
    An immutable data structure to limit calls times.
    Composable : limiter()()()() will keep the call frequency
    >>> l = Limiter(frequency=1)
    >>> start = time.time()
    >>> l()
    >>> lap = time.time() - start
    >>> print(lap)

    >>> l()()
    >>> lap = time.time() - lap
    >>> print(lap)

    """
    #: We want the current time to be able to add and remove limiter
    #: with immediate effect (prevent call bursts)

    target_frequency: float = 1.0
    now: typing.Callable = field(default=time.time, repr=False)
    sleep: typing.Callable = field(default=time.sleep, repr=False)
    epsilon: float = 0.01  # error (WARNING : this will depend on your OS/machine !)

    periods_measured: typing.List[float] = field(init=False, repr=False)
    last_call: float = field(init=False, repr=False)

    def __post_init__(self):
        self.periods_measured = []
        self.last_call = self.now()

    def __call__(self):
        #TODO : make it async proof if more is needed.
        #TODO : make it multithread proof.... if possible.
        period = 1 / self.target_frequency

        # if we need to, we wait... (note we could also async wait...)
        begin = self.now()
        since_last = begin - self.last_call
        if since_last < period:
            self.sleep(period - since_last + self.epsilon)  # in doubt, we oversleep

        last_period = self.now() - begin

        if last_period < period:  # we didn't sleep enough
            self.sleep(self.epsilon)  # sleep a bit more
            # double epsilon
            self.epsilon += self.epsilon
        elif last_period - period < self.epsilon:  # TODO : work on control theory to optimize call frequency based on measured perf
            # slept more than enough
            self.epsilon -= self.epsilon / 2

        # last_period after epsilon rectification
        last_period = self.now() - begin

        self.periods_measured.append(last_period)
        self.last_call = self.now()
        return self

    @property
    def average_period(self):
        return sum(self.periods_measured)/len(self.periods_measured)


def limiter(limiter: Limiter = Limiter()):
    """
    a limiter to use as a decorator.
    :param limiter: A limiter can be passed. useful to limit a group of functions together as one
    :return: a decorator to apply to the function you want to limit.
    """

    def decorator(func):
        """
        A decorator
        :param func:
        :param profiler:
        :return:
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            limiter()
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


if __name__ == '__main__':
    l = Limiter(target_frequency=1)
    # tick tock the clock
    start = time.time()
    for i in range(60):
        l()
        print(f"Limiter {l} period {l.average_period}")


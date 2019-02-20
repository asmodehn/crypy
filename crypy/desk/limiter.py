import inspect
import math

import profile  #: higher overhead and require calibration. BEtter for python debugging, and maybe better on average after calibration ?
#import cProfile as profile  # better for quick results, after the dev phase.
import pstats

# TODO : nice output eventually : https://stackoverflow.com/questions/4544784/how-can-you-get-the-call-tree-with-python-profilers
import sys

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


class CallLimitError(Exception):
    def __init__(self, msg, retry_after):
        self.retry_after = retry_after
        super().__init__(msg + f"Retry after: {self.retry_after}")


def slumber(secs: float = 1.0) -> None:
    """
    Make sure we actually sleep enough
    :return:
    """
    total_sleeptime = 0
    start = time.perf_counter()
    while total_sleeptime < secs:
        time.sleep(secs - total_sleeptime)
        total_sleeptime = time.perf_counter() - start


# TODO : this can be made generic by parametrizing on the type float
# TODO : optimized interval logic ?
class PeriodBounds(typing.NamedTuple):
    upper: typing.Optional[float] = None
    lower: typing.Optional[float] = None


# TODO : invertible to get FrequencyBounds...


def check_call_period_bounds(bounds: PeriodBounds, last_period: float, on_under: typing.Optional[typing.Callable] = None, on_over: typing.Optional[typing.Callable] = None):
    proceed = True  # proceed by default

    if bounds.lower and last_period < bounds.lower:
        try:
            proceed = on_under(last_period, bounds.lower)
        except TypeError:
            if on_under is None:
                return True  # no action on out of bounds -> keep usual semantics
            raise
    elif bounds.upper and last_period > bounds.upper:
        try:
            proceed = on_over(last_period, bounds.upper)
        except TypeError:
            if on_over is None:
                return True  # no action on out of bounds -> keep usual semantics
            raise
    return proceed


# TODO : numpy-based PID controller of procedure call (ie function application) period.

# TODO : relate with profiler ? we need to measure time and minimize the additional time taken by measuring time...

@dataclass
class CallBoundedFunc:

    # TODO : require a pure function (or idempotent, depending if you consider the state as an arg or not)
    func: typing.Callable = field(default=lambda: None)
    calltimer: typing.List[float] = field(init=False, default_factory=list, repr=False)  # TODO : bound in size

    limits: PeriodBounds = field(default=PeriodBounds(lower=1.0, upper=None))

    on_undercall: typing.Optional[typing.Callable] = None
    on_overcall: typing.Optional[typing.Callable] = None

    def __post_init__(self):
        # TODO : access cached value for func.
        # Design : func should be an specific class instance
        #          that allows retrieving from cache or not depending on params or context...
        self.last_res = None
        self.calltimer.append(time.perf_counter())

    def __call__(self, *args, **kwargs):
        # TODO : manage undercall properly, especially first time (initialization, etc.)
        proceed = check_call_period_bounds(
            bounds=self.limits,
            last_period=time.perf_counter() - self.calltimer[-1],
            on_under=self.on_overcall,  # Note over period is under frequency and vice versa...
            on_over=self.on_undercall)
        if proceed:
            self.calltimer.append(time.perf_counter())
            self.last_res = self.func(*args, **kwargs)
        return self.last_res

    @property
    def average_call_period(self):
        if len(self.calltimer) < 2:
            return None
        # Hardcoded precision given most computer clock -> TODO : dynamic
        return round(math.fsum((u-t for t, u in zip(self.calltimer, self.calltimer[1:]))) / (len(self.calltimer) -1), 4)

    @property
    def last_call_period(self):
        if len(self.calltimer) < 2:
            return None
        # Hardcoded precision given most computer clock -> TODO : dynamic
        return round(self.calltimer[-1] - self.calltimer[-2], 4)


def wait_limiter(max_cps=1):
    """
    A call limiter to use as a decorator.
    This limiter will wait until it is allowed to call the function again.
    Note : you can use the returned function to decorate multiple functions, if you want to limit them as a group.
    :param max_cps: Maximum number of calls per seconds to enforce
    :return: a decorator to apply to the function you want to limit.
    """

    def sleep_n_proceed(last_period, bound):
        slumber(bound - last_period)
        return True

    def decorator(func):
        # Todo : proper wrapper ?
        return CallBoundedFunc(func=func, limits=PeriodBounds(lower=max_cps, upper=None), on_overcall=sleep_n_proceed)

    return decorator


def drop_limiter(max_cps=1):
    """
    A call limiter to use as a decorator.
    This limiter will drop the call by raising an exception if it is called too quickly.
    Note : you can use the returned function to decorate multiple functions, if you want to limit them as a group.
    WARNING : to not change the semantics of your program, the function should be "as pure as possible",
              ie, skipping a call should not matter...
    :param max_cps: Maximum number of calls per seconds to enforce
    :return: a decorator to apply to the function you want to limit.
    """

    def drop(last_period, bound):
        return False  # ignore arguments and return false to drop the call (and use a cached value)

    def decorator(func):
        # Todo : proper wrapper ?
        return CallBoundedFunc(func=func, limits=PeriodBounds(lower=max_cps, upper=None), on_overcall=drop)

    return decorator


if __name__ == '__main__':

    print("Checking wait limiter:")
    # tick tock the clock
    start = time.time()

    @wait_limiter(max_cps=1)
    def printtime():
        print(f"{time.time()-start}")

    for i in range(30):
        printtime()
        print(f"Limiter last period {printtime.last_call_period} avg {printtime.average_call_period}")

    print("Checking drop limiter:")
    # tick tock the clock
    start = time.time()
    val = 0

    @drop_limiter(max_cps=1)
    def incr():
        global val
        print(f"{time.time() - start}")
        val += 1
        return val

    while time.time() - start < 30:
        time.sleep(.3)  # avoiding cpu overload, but still faster than limiter
        print(f"Limiter last period {printtime.last_call_period} avg {printtime.average_call_period}")
        print(f"{incr()}")


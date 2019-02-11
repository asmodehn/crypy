import time

import functools

from .. import limiter


def test_calllimiter_sync():
    period = 1

    def funtest(accmax):
        acc = 0
        for a in range(accmax):
            acc += a
        return acc

    start = time.time()
    funtest(1024)
    finish = time.time()
    assert finish - start < period  # making sure the call limiter will be meaningful

    # adding the limiter decorator, dynamically

    l = limiter.limiter(limiter.CallProfiler(last_call=time.time(), frequency=1.0/period))(funtest)

    start = time.time()
    l(1024)
    finish = time.time()

    assert finish - start > period  # making sure the call limiter is doing its job


def test_calllimiter_group_sync():
    period = 1

    def funtest1(accmax):
        acc = 0
        for a in range(accmax):
            acc += a
        return acc

    def funtest2(accmax):
        return funtest1(accmax)

    start = time.time()
    funtest1(1024)
    funtest2(1024)
    finish = time.time()
    assert finish - start < period  # making sure the call limiter will be meaningful

    # adding the limiter decorator, dynamically
    # we pass a last_call of 0  to force a first call immediately.
    profiler = limiter.CallProfiler(last_call=0, frequency=1.0/period)
    l1 = limiter.limiter(profiler=profiler)(funtest1)
    l2 = limiter.limiter(profiler=profiler)(funtest1)

    start = time.time()
    l1(1024)  # immediate
    lap = time.time()
    assert lap - start < period  # first assert earlier gave us confidence here.

    l2(1024)  # should wait a bit
    finish = time.time()

    assert finish - start > period  # making sure the call limiter is doing its job for two function with one profiler




def test_sleep_function():
    # simple function callable
    @limiter.sleep(sleepfun)
    def func():

        return

def test_call_limiter():

    @limiter.callrate(5, time.sleep)
    def func(arg1, arg2, arg3):
        return arg1, arg2, arg3




# partial callable
#def func( , part = None):


#partial = functools.partial(func, part="unused")


# class callable



# method callable

# TODO : async callable










import time

import functools

from .. import limiter

# TODO : mock time passing, to not depend on side effects... and mock sleep to not take too long to test


def test_calllimiter_sync():
    period = 1

    def funtest(accmax):
        acc = 0
        for a in range(accmax):
            acc += a
        return acc

    start = time.time()
    funtest(1024)
    duration = time.time() - start
    assert duration < period  # making sure the call limiter will be meaningful

    #creating the limiter
    l = limiter.Limiter(target_frequency=1.0 / period)

    # using limiter inflow
    start = time.time()
    l()
    funtest(1024)
    duration = time.time() - start
    assert duration > period  # making sure the call limiter is doing its job

    # adding the limiter decorator, dynamically

    ldec = limiter.limiter(l)(funtest)

    start = time.time()
    ldec(1024)
    duration = time.time() - start

    assert duration > period  # making sure the call limiter is doing its job


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
    duration = time.time() - start
    assert duration < period  # making sure the call limiter will be meaningful

    # creating the limiter
    l = limiter.Limiter(target_frequency=1.0 / period)

    # using limiter inflow
    start = time.time()
    l()
    funtest1(1024)
    lap = time.time() - start
    assert period < lap < 2 * period
    l()
    funtest2(1024)
    finish = time.time() - start
    assert 2 * period < finish < 3 * period  # making sure the call limiter is doing its job

    # adding the limiter decorator, dynamically, using teh same limiter instance
    lfuntest1 = limiter.limiter(l)(funtest1)
    lfuntest2 = limiter.limiter(l)(funtest1)

    start = time.time()
    lfuntest1(1024)  # immediate
    lap = time.time() - start
    assert period < lap < 2 * period
    lfuntest2(1024)  # should wait a bit
    finish = time.time() - start
    assert 2 * period < finish < 3 * period  # making sure ot s also working for two function with one profiler

    # Stacking limited calls on the same limiter instance
    @limiter.limiter(l)
    def funtest3(accmax):
        return lfuntest1(accmax)

    start = time.time()
    funtest3(1024)  # more than 2 periods
    finish = time.time() - start
    assert 2 * period < finish < 3 * period

#
# def test_sleep_function():
#     # simple function callable
#     @limiter.sleep(sleepfun)
#     def func():
#
#         return
#
# def test_call_limiter():
#
#     @limiter.callrate(5, time.sleep)
#     def func(arg1, arg2, arg3):
#         return arg1, arg2, arg3




# partial callable
#def func( , part = None):


#partial = functools.partial(func, part="unused")


# class callable



# method callable










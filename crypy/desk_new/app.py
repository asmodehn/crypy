import hypothesis
from hypothesis.strategies import builds, integers, booleans, one_of
import typing
from pydantic import BaseModel, ValidationError, validate_model
import unittest

from .commands import Answer
from .repl import input_nested

import prompt_toolkit

from prompt_toolkit.eventloop.defaults import use_asyncio_event_loop
use_asyncio_event_loop()

from prompt_toolkit.patch_stdout import patch_stdout

counter = [0]



# EVENTUALLY:
#
# from prompt_toolkit.application import Application
#
# async def repl():
#     # Define application.
#     application = Application(
#         ...
#     )
#
#     result = await application.run_async()
#     print(result)
#
# asyncio.get_event_loop().run_until_complete(main())


async def print_counter():
    """
    Coroutine that prints counters and saves it in a global variable.
    """
    import asyncio

    while True:
        print('Counter: %i' % counter[0])
        counter[0] += 1
        await asyncio.sleep(3)


def scheduler():
    import asyncio
    loop = asyncio.get_event_loop()

    import asyncio
    counter = asyncio.ensure_future(print_counter())
    result = asyncio.ensure_future(input_nested())

    def stopcount(finished_task):
        counter.cancel()

    result.add_done_callback(stopcount)

    loop.run_until_complete(asyncio.gather(counter, result))

    result.result().printme()
    loop.close()

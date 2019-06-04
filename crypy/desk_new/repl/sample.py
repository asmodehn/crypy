import typing
from pydantic import BaseModel, ValidationError, validate_model
import prompt_toolkit

from prompt_toolkit.eventloop.defaults import use_asyncio_event_loop
use_asyncio_event_loop()

from prompt_toolkit.patch_stdout import patch_stdout

from ..commands import Answer, Nested


async def input_answer() -> Answer:
    a = None
    with patch_stdout():
        data = await prompt_toolkit.prompt(message="Enter Answer: ", async_=True)
        while a is None:
            values, errors = validate_model(model=Answer, input_data={'data': data}, raise_exc=False)
            if errors:
                print(errors)
                data = await prompt_toolkit.prompt(message="Enter Answer AGAIN: ", async_=True)
            else:
                a = Answer(**values)
    return a


async def input_nested() -> Nested:
    a = None
    with patch_stdout():
        data = await prompt_toolkit.prompt(message="Enter Nested: ", async_=True)
        while a is None:

            # inspect Nested
            # parse answer using part of input_answer
            # build Nested

            values, errors = validate_model(model=Answer, input_data={'answer': data}, raise_exc=False)
            if errors:
                print(errors)
                data = await prompt_toolkit.prompt(message="Enter Nested AGAIN: ", async_=True)
            else:
                a = Nested(**values)
    return a

import hypothesis
from hypothesis.strategies import builds, integers, booleans, one_of
import typing
from pydantic import BaseModel, ValidationError, validate_model
import unittest


class Answer(BaseModel):

    # Data model of user interface (might be different than data model of Exchange interface)

    data: int

    def __init__(self, data: int):
        super().__init__(data=data)

    def printme(self):
        print(self.data)
        # Complicated code will be here
        return True


class TestAnswer(unittest.TestCase):

    # NOTE : later we can extract complex hypothesis test structures with pydantic into separate packages
    # already done for other parsers : https://hypothesis.readthedocs.io/en/latest/strategies.html#external-strategies

    @hypothesis.settings(verbosity=hypothesis.Verbosity.verbose)
    @hypothesis.given(a=hypothesis.infer)
    def test_printme(self, a: int):

        answer = Answer(a)
        assert answer.printme()

class Right(BaseModel):

    # Data model of user interface (might be different than data model of Exchange interface)

    data: bool

    def __init__(self, data: bool):
        super().__init__(data=data)

    def printme(self):
        print("RIGHT" if self.data else "WRONG")
        # Complicated code will be here
        return True


class TestRight(unittest.TestCase):

    # NOTE : later we can extract complex hypothesis test structures with pydantic into separate packages
    # already done for other parsers : https://hypothesis.readthedocs.io/en/latest/strategies.html#external-strategies

    @hypothesis.settings(verbosity=hypothesis.Verbosity.verbose)
    @hypothesis.given(a=hypothesis.infer)
    def test_printme(self, a: bool):

        right = Right(a)
        assert right.printme()


class AnswerOrRight(BaseModel):

    # Data model of user interface (might be different than data model of Exchange interface)

    data: typing.Union[Answer, Right]

    def __init__(self, data: typing.Union[Answer, Right]):
        super().__init__(data=data)

    def printme(self):
        return self.data.printme()


class TestAnswerOrRight(unittest.TestCase):

    # NOTE : later we can extract complex hypothesis test structures with pydantic into separate packages
    # already done for other parsers : https://hypothesis.readthedocs.io/en/latest/strategies.html#external-strategies

    @hypothesis.settings(verbosity=hypothesis.Verbosity.verbose)
    @hypothesis.given(a=one_of(builds(Answer, integers()), builds(Right, booleans()) ))
    def test_printme(self, a: typing.Union[Answer, Right]):

        aor = AnswerOrRight(a)
        assert aor.printme()


class AnswerAndRight(BaseModel):

    answer: Answer
    right: Right


    def __init__(self, answer: Answer, right: Right):
        super().__init__(answer=answer, right=right)

    def printme(self):
        return self.data.printme()




class TestAnswerAndRight(unittest.TestCase):

    # NOTE : later we can extract complex hypothesis test structures with pydantic into separate packages
    # already done for other parsers : https://hypothesis.readthedocs.io/en/latest/strategies.html#external-strategies

    @hypothesis.settings(verbosity=hypothesis.Verbosity.verbose)
    @hypothesis.given(a=builds(Answer, integers()), r=builds(Right, booleans()))
    def test_printme(self, a: Answer, r: Right):

        aor = AnswerAndRight(a, r)
        assert aor.printme()





import prompt_toolkit

from prompt_toolkit.eventloop.defaults import use_asyncio_event_loop
use_asyncio_event_loop()

from prompt_toolkit.patch_stdout import patch_stdout


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


async def input_right() -> Right:
    a = None
    with patch_stdout():
        data = await prompt_toolkit.prompt(message="Enter Right: ", async_=True)
        while a is None:
            values, errors = validate_model(model=Right, input_data={'data': data}, raise_exc=False)
            if errors:
                print(errors)
                data = await prompt_toolkit.prompt(message="Enter Right AGAIN: ", async_=True)
            else:
                a = Right(**values)
    return a



async def input_answerORright() -> Right:
    a = None
    with patch_stdout():
        data = await prompt_toolkit.prompt(message="Enter Answer OR Right: ", async_=True)
        while a is None:
            values, errors = validate_model(model=Right, input_data={'data': data}, raise_exc=False)
            if errors:
                print(errors)
                data = await prompt_toolkit.prompt(message="Enter Answer OR Right AGAIN: ", async_=True)
            else:
                a = Right(**values)
    return a



async def input_answerANDright() -> Right:
    a = None
    with patch_stdout():
        data = await prompt_toolkit.prompt(message="Enter Answer AND Right: ", async_=True)
        while a is None:
            values, errors = validate_model(model=Right, input_data={'data': data}, raise_exc=False)
            if errors:
                print(errors)
                data = await prompt_toolkit.prompt(message="Enter Answer AND Right AGAIN: ", async_=True)
            else:
                a = Right(**values)
    return a




counter = [0]


async def repl()-> typing.Union[Answer, Right, AnswerOrRight, AnswerAndRight]:
    a = None
    with patch_stdout():
        data = await prompt_toolkit.prompt(message="Enter Answer: ", async_=True)
        while a is None:
            if data.digit :
                values, errors = validate_model(model=Answer, input_data={'data': data}, raise_exc=False)
            elif data:
                pass #TODO
            if errors:
                print(errors)
                data = await prompt_toolkit.prompt(message="Enter Answer AGAIN: ", async_=True)
            else:
                a = Answer(**values)
    return a






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
    result = asyncio.ensure_future(input_answer())

    def stopcount(finished_task):
        counter.cancel()

    result.add_done_callback(stopcount)

    loop.run_until_complete(asyncio.gather(counter, result))

    result.result().printme()
    loop.close()


if __name__ == '__main__':

    import click

    CONTEXT_SETTINGS = dict(help_option_names=['-h', '--h', '--help', '?'])

    @click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=False)
    @click.pass_context
    def cli_group_example(ctx):
        click.echo(f"Ask stuff")

    @cli_group_example.command('ask')
    @click.option('-a', '--answer', type=int, default=42, show_default=True,
                  help='comma delimited list of assets to restrict output to')
    @click.pass_obj
    def click_cmd_exmple(obj, answer):
        a = Answer(answer)
        a.printme()

        return 0  # shell success


    @cli_group_example.command('right')
    @click.option('-r', '--right', type=int, default=42, show_default=True,
                  help='comma delimited list of assets to restrict output to')
    @click.pass_obj
    def click_cmd_exmple(obj, right):
        r = Right(right)
        r.printme()

        return 0  # shell success


    @cli_group_example.command('repl')
    @click.pass_obj
    def cli_repl(obj):
        scheduler()
        return 0  # shell success


    @cli_group_example.command('tryme')
    @click.pass_obj
    def tryme(obj):
        # initialize the test suite
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()

        # add tests to the test suite
        suite.addTests(loader.loadTestsFromTestCase(TestAnswer))

        # initialize a runner, pass it your suite and run it
        runner = unittest.TextTestRunner(verbosity=3)
        return runner.run(suite)

    cli_group_example()




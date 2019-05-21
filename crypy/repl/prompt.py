import collections
import dataclasses
import inspect
import os
import sys
from dataclasses import dataclass

from typing import Mapping, MutableMapping, Sequence, Iterable, List, Set, TypeVar
import pydantic
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from fuzzyfinder import fuzzyfinder
from pygments.lexers.sql import SqlLexer
import returns.result as result
from typing_extensions import Literal

from prompt_toolkit.history import FileHistory

# CalcKeywords = ['select', 'from', 'insert', 'update', 'delete', 'drop']

class SQLCompleter(Completer):
    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        matches = fuzzyfinder(word_before_cursor, SQLKeywords)
        for m in matches:
            yield Completion(m, start_position=-len(word_before_cursor))


lcls = {}


T = TypeVar('T')


def validate(input_value: str, t: type(T), *elem_types) -> result.Result[T, Exception]:  # TODO : refine return types
    try:
        if t in [int, float, complex, str]:
            assert " " not in input_value  # avoiding problems later...
            validated = t(input_value)# TODO : different ways to cast / validate ?
                            # TODO : interface with pydantic/hypothesis somehow ?
        else:  # assume iterable
            l = []
            for ve in parselist(input=input_value, separator=" ", *elem_types):
                l.append(ve)

            validated = t(*l)
        return validated

    except Exception as e:  # handle all kinds of validation errors
        print(e)
        return e


def parselist(input: str, separator=" ", elem_type: T) -> typing.Iterator[T]:
    for e in input.split(sep=separator):
        yield validate(e, elem_type)


H = typing.TypeVar('H')  # should be hashable

# TODO : probably something similar to python calling mechanisms ?
def parsedict(input: str, separator=" ", key_prefix="--", key_type=H, elem_type) -> typing.Dict[H, elem_type]:

    parsed = collections.OrderedDict()
    curkey = None
    for ve in parselist(input=input, separator=separator, *elem_type):
        if ve.startswith(key_prefix):
            curkey = ve[len(key_prefix):]
        else:
            parsed[curkey] = validate(input_value=ve, t=elem_type[0], *elem_type[1:])

    # todo improve for complex multiple args...

    return parsed


def dataprompt(name: str, value: T, t: type(T)) -> result.Result[T, Exception]:

    try:
        # validate value passed
        validated = None
        # base types first
        if t in [int, float, str]:
            while validated is None:
                # attempt implicit conversion
                try:
                    # TODO : skippable if value is correct?
                    user_input = prompt(
                        message=f'{name}>',
                        history=FileHistory(os.path.join(f'{name}.log')),
                        auto_suggest=AutoSuggestFromHistory(),
                        # completer=SQLCompleter(),  # add already input data

                        # lexer=SqlLexer,  # probably python lexer ?
                        # multiline=True,
                        # prompt_continuation=limited_continuation(cls),
                    )
                    # TODO : multiline on complex structure (tree ?)

                    validated = validate(name=name, input_value=user_input, t=t)  # TODO : different ways to cast / validate ?
                    # TODO : interface with pydantic somehow ?

                except TypeError as te:
                    print(te)
                    validated = None

                except Exception as e:  # TODO : make more precise
                    print(e)
                    pass  # TODO : handle ?
            # TODO : completer with existing value

        else:  # all non basic (composed / type product) cases
            #TODO : handle all possibilities in python code
            fs = inspect.getmembers(t, lambda m: not inspect.isroutine(m))
            value = {f[0]: f[1] for f in fs if "__" not in f[0]}
            for n, v in value.items():
                validdata = dataprompt(f"{name}.{n}", v, type(v))
                # TODO : store input values
                value[n] = validdata

            value = validate(**value)

            if isinstance(value, t):  # instance of the right class already there
                validated = value  # early return (end recursion). TODO : check validation with pydantic...
            else:
                validated = validate(name=name, value=value, t=t)  # TODO : different ways to cast / validate ?
            # TODO : interface with pydantic somehow ?

        return validated


    #         while data is None:  # looping on wrong entries
    #             user_input = prompt(
    #                 message=f'{name}>',
    #                 history=FileHistory(os.path.join(f'{name}.log')),
    #                 auto_suggest=AutoSuggestFromHistory(),
    #                 # completer=SQLCompleter(),  # add already input data
    #
    #                 # lexer=SqlLexer,  # probably python lexer ?
    #                 #multiline=True,
    #                 #prompt_continuation=limited_continuation(cls),
    #             )
    #             data = user_input.split()
    #
    # # TODO : think about exception that are normal errors, and those that are REAL exceptions.
    except KeyboardInterrupt as ki:
        print(ki)
        return ki
    except EOFError as eof:
        print(eof)
        return eof


# def dataprompt(cls):
#
#     def limited_continuation(field):
#
#         if dataclasses.is_dataclass(cls):
#             fields = dataclasses.fields(cls)
#         elif inspect.isclass(cls):
#             fields = inspect.getmembers(cls, inspect.isdatadescriptor)
#
#         # TODO : handle when there is no type annotation...
#         print(fields)
#
#         def prompt_continuation(width, line_number, is_soft_wrap):
#             nonlocal fields
#             try:
#                 subprompt = [('', f"{fields[line_number].name}: {fields[line_number].type.__name__}> ")]
#                 return subprompt
#             except IndexError as ie:
#                 print("DO SMTHG TO EXIT")
#                 return
#
#         return prompt_continuation
#
#     inst = None
#     while inst is None:
#
#         def do_create(cls, **data):
#
#             created = None
#             while created is None:
#                 try:
#                     created = cls(**data)
#                 except Exception as e:
#                     print(e)
#                     try:
#                         user_input = prompt(
#                             message=u'f"{cls}">create>',
#                             history=FileHistory(os.path.join('repl.log')),
#                             auto_suggest=AutoSuggestFromHistory(),
#                             # completer=SQLCompleter(),  # add already input data
#
#                             # lexer=SqlLexer,  # probably python lexer ?
#                             multiline=True,
#                             prompt_continuation=limited_continuation(cls),
#                         )
#                         data = user_input.split()
#
#                     except KeyboardInterrupt as ki:
#                         print(ki)
#                         return
#                     except EOFError as eof:
#                         print(eof)
#                         return
#
#             return created
#
#         def cmd_parse(cmd, cls, *args):
#             if cmd == 'create':
#                 do_create(cls, *args)
#             else:
#                 raise NotImplementedError()
#
#         try:
#
#             user_input = prompt(
#                 message=u'f"{cls}">',
#                 history=FileHistory(os.path.join('repl.log')),
#                 auto_suggest=AutoSuggestFromHistory(),
#                 # completer=SQLCompleter(),
#
#                 # lexer=SqlLexer,
#             )
#
#             data = user_input.split()
#
#             cmd_parse(**data)
#             try:
#                 inst = cls(*data)
#             except TypeError as te:
#                 print(te)
#
#                 # TODO : maybe we need recursive call here ?
#
#             except Exception as e:
#                 print(e)
#                 inst = None
#
#         except KeyboardInterrupt as ki:
#             print(ki)
#             return
#         except EOFError as eof:
#             print(eof)
#             return
#
#     return inst


if __name__ is "__main__":

    data: float = 42

    exfloat = dataprompt(name="data", value=data, t=float)
    print(exfloat)

    class Class:
        data: float = 42
        descr: str = "descr"

        def __init__(self, data):
            self.data = data
            self.descr = str(data)

    d = Class(31)

    exclass = dataprompt(name="d", value=d, t=Class)
    print(exclass)


    from dataclasses import dataclass

    @dataclass
    class Example:

        firstfield: int
        secondfield: float

        def __enter__(self):
            pass

        def __exit__(self, exc_type, exc_val, exc_tb):
            print(f"{exc_type}: {exc_val}\n{exc_tb}")

    dc = Example("first", "second")
    exdataclass = dataprompt(name="dc", value=dc, t=Example)

    # check iexinst is correct

    print(exdataclass)
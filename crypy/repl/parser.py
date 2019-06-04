import collections
import dataclasses
import inspect
import os
import sys
from dataclasses import dataclass

from typing import Mapping, MutableMapping, Sequence, Iterable, List, Set, TypeVar

import prompt_toolkit
import pydantic
import typing
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

# TODO : pygments lexer


lcls = {}

T = TypeVar('T')

H = TypeVar('H') # hashable

"""
This module implements a parser
that aims to be as implicit as possible for human usage
ie. we want to use the facts that:
- TODO: a str is a sequence of lines (human perspective)
- a str is a sequence of words (human perspective)
- mapping depends on a key that should be explicit for humans to read (typing by hand is not the main concern)
- implicit conversion of string to basic types, just like python does (simplicity)
"""

config_python = {
    "input_type": str,
    "sequence_separator": " ",
    "mapping_key_prefix": "",
    "mapping_key_suffix": ":",
}

config_cli = {
    "input_type": str,
    "sequence_separator": " ",
    "mapping_key_prefix": "--",
    "mapping_key_suffix": "",
}

#TODO: chnage that in higher level function
config=config_python


#line separator is explicit in one OS and managed properly by python between platforms
def parse(input: str, elem_type: T = typing.Any)-> typing.Iterator[T]:
    """
    generator  that parses a multiline input.
    :param input: input string (potentially multiline)
    :param elem_type: the type expected for each line
    :return: an iterator on the element type

    >>> [i for i in parse(" 42 \\n 56 ")]
    [42, 56]
    """
    # TODO : first line special
    # TODO : iterator to handle long input (file, etc.)
    for l in input.splitlines(keepends=False):
        yield parseline(l.strip())


def parseline(input: str, separator=" ", elem_type: T = typing.Any) -> typing.Union[typing.Mapping[H, T], typing.Iterator[T]]:
    """
    generator that parses a singleline input.
    :param input: input string (potentially multiword)
    :param separator: separator between words
    :param elem_type: the type expected for each word
    :return:
    >>>[f for f in parseline("45.5 56.2")]
    [45.5, 56.2]

    >>>[f for f in parseline("key: myvalue")]
    {key: myvalue}
    """
    #TODO : iterator to plan for long strings
    splitted = input.split(sep=separator)

    # TODO : Head/tail logic leveraging recursivity (and plug a repl in there) ?

    for e in splitted:
        key = None
        value = []
        if e.startswith(config.mapping_key_prefix) and e.startswith(config.mapping_key_suffix):
            if key is not None:
                # end previous key sequence
                yield parseword(value, elem_type)

            # new key
            key = e[len(config.mapping_key_prefix):len(config.mapping_key_suffix)]

        if key is not None:
            value.append(e)

        yield parseword(e, elem_type)


# TODO : handle prompt session ?

def parseword(input: str,  t: T) -> T:


    try:
        if t in [int, float, complex, str]:
            assert " " not in input  # avoiding problems later...
            parsed = t(input)  # TODO : different ways to cast / validate ?
            # TODO : interface with pydantic/hypothesis somehow ?
        else:
            print(f"Cannot cast {input} to {t}")
            print(f"{input} must represent one of these : {[int]}")
        return parsed

    except Exception as e:  # handle all kinds of validation errors
        print(e)
        return e

def promptword(prompter: str, suggested=None) -> input:
    def suggest(self):
        # TODO : handle possible list here
        return prompt_toolkit.auto_suggest.Suggestion(suggested)

    user_input = prompt_toolkit.prompt(
        message=u'f"{prompt}">create>',
        auto_suggest=suggest,
        # completer=SQLCompleter(),  # add already input data

        # lexer=SqlLexer,  # probably python lexer ?
        # multiline=True,
        # prompt_continuation=limited_continuation(cls),
    )
    data = parseword(user_input, t=t)


def expect(t: T) -> T:



    return functools.partial(parse())






H = typing.TypeVar('H')  # should be hashable


# TODO : probably something similar to python calling mechanisms ?
def parsedict(input: str, separator=" ", key_prefix="--", key_type: H = str, elem_type: T = object) -> typing.Dict[
    H, T]:
    parsed = collections.OrderedDict()
    curkey = None
    for ve in parselist(input=input, separator=separator, *elem_type):
        if ve.startswith(key_prefix):
            curkey = ve[len(key_prefix):]
            parsed[curkey] = None
        else:
            parsed[curkey] = validate(input_value=ve, t=elem_type[0], *elem_type[1:])

    # todo improve for complex multiple args...

    return parsed


def validate(input_value: str, t: type(T), *elem_types) -> result.Result[T, Exception]:  # TODO : refine return types
    """
    :param input_value:
    :param t:
    :param elem_types:
    :return:

    >>> validate("1", int)

    >>> validate("1 2", typing.List[int])

    >>> validate("answer 42")
    """
    try:
        if t in [int, float, complex, str]:
            assert " " not in input_value  # avoiding problems later...
            validated = t(input_value)  # TODO : different ways to cast / validate ?
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


if __name__ == "__main__":
    # import doctest
    # doctest.testmod()

    promptword("test", "suggestion")
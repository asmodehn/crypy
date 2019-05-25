"""
Prompter on failing to parse a type
Limiting ourselves to python typesfor now.
"""
from __future__ import annotations
import typing

import enum
import prompt_toolkit

from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import CompleteStyle


completer = {
    bool: WordCompleter(['True', 'False'], ignore_case=True),
    int: WordCompleter(['42', '53']),
}


class POPType:

    type: typing.Type  # python type implementation
    session: prompt_toolkit.PromptSession

    def __repr__(self):
        """
        The exact inverse of parse. Unambiguous.
        Any user-niceties should be handled somewhere else (str).
        :return:
        """
        return repr(self.type)

    def __str__(self):
        """ Human niceity version for repr."""
        return str(self.type)

    def __init__(self, type: typing.Type):
        """
        Parsing data, one at a time
        :param value:
        :param type:
        """
        self.type = type
        self.session = prompt_toolkit.PromptSession(
            message=str(type) + '? ',
            history=InMemoryHistory(),
            auto_suggest=AutoSuggestFromHistory(),
            completer=completer[type], complete_style=CompleteStyle.COLUMN,
        )
        # TODO : better wordcompleter (define more precisely possible values)


    # Note: Different strategies ARE different types.
    # Prompt is a user strategy. assumed random ?
    # This should probably just be a replay to whatever the strategy was in the first place (creation/construction of the type)

    #  note : behavior semantics is union (coproduct / sum).
    # In this case environment makes the choice, so it s a union (determinism upon measurement)
    def prompt(self):
        data = None
        while data is None:
            try:
                data = self.type(self.session.prompt())
            except ValueError as ve:
                print (ve)
                data = None
        return data

    def __call__(self, data: str) -> self.type:  # note a type hint in python is not enforced.
        """
        Parser, expecting CTType...
        :param data:
        :return:
        """
        try:
            # parse
            data = self.type(data)
            # tODO : mix in default value...
        except ValueError as ve:
            print(ve)
            #  recurse (or suicide) if user can't get it right
            data = self.prompt()
            # TODO : infinite recurse ?

        return data












    # def __add__(self, other):
    #     """
    #     CoProduct
    #     :param other:
    #     :return:
    #     """
    #
    #     if not isinstance(other, CTType):
    #         if isinstance(other, (int, float, complex)):
    #             other = self.Literal(other)
    #         elif isinstance(other, type):
    #             other = CTType(other)
    #
    #     self.type = typing.Union[self.impl, other.impl]
    #     self.impl = 'what ?'
    #     return self
    #
    # def __mul__(self, other):
    #     """
    #     Cartesian Product
    #     :param other:
    #     :return:
    #     """
    #     self.type = typing.Tuple[self.impl, other.impl]
    #     self.impl = tuple
    #     return self


if __name__ == '__main__':

    pi = POPType(type=int)

    # succeeds
    val = pi('42')

    # fails and prompt, forever
    pval = pi('fortytwo')




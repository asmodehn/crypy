"""
Representing a type as a function.
Type represent interaction with environment.
"""
from __future__ import annotations
import typing

import enum
import prompt_toolkit

from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import CompleteStyle

# TODO : improve typing.Union


class _CTypeValue:
    value: typing.Any
    members: typing.Set

    def __init__(self, value):
        self.value = value
        self.members = {value}

    def __eq__(self, other):
        # TODO : check type !
        if other in self:
            # TODO evaluates to equals values

    def __iter__(self):
        """ implementing the notion of membership """
        return self.members

    def __call__(self, index):
        """ indexed type -> ignore/drop index"""
        # TODO : what about 'types are programs' ? shouldnt it be a generator of all elements of the type ?
        return self


class _CTypeFamily:
    """
    Tentative basic implementation of some sort of CTT
    """

    value: typing.Any
    members: typing.Set

    def __init__(self, value):
        self.impl = value

    def __eq__(self, other):
        s = self.impl

    def __call__(self):
        """Index the type family"""


    def repr(self):
        return











class CTType:
    # TODO : improve...
    impl: typing.Any  # values holder
    type: typing.Type  # python type implementation

    @classmethod
    def unit(cls):
        return cls('0')

    @staticmethod
    def Literal(value):
        """
        Build a literal value (type-value, in the value-dependent type sense)
        :param value:
        :return:
        """
        return CTType(value)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.impl)

    def __init__(self, name: str, literal = None):
        # TODO : find best implementation with python typing...
        self.type = typing.TypeVar(name)  # refine current type
        self.impl = literal  # None represents never-ending computation, empty set, bottom, etc. 

    def __aenter__(self):
        """
        Entering type context.
        Now able to apply some game semantics, unrolling strategies...
        see Mellies...
        :return:
        """

    def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Exitng type context.
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """

    def __add__(self, other):
        """
        CoProduct
        :param other:
        :return:
        """

        if not isinstance(other, CTType):
            if isinstance(other, (int, float, complex)):
                other = self.Literal(other)
            elif isinstance(other, type):
                other = CTType(other)

        self.type = typing.Union[self.impl, other.impl]
        self.impl = 'what ?'
        return self

    def __mul__(self, other):
        """
        Cartesian Product
        :param other:
        :return:
        """
        self.type = typing.Tuple[self.impl, other.impl]
        self.impl = tuple
        return self

    def __aiter__(self):
        return self  # TODO : OR something else ??

    def __anext__(self):
        """generator of type elements.
        Note: Different strategies ARE different types.
        Prompt is a user strategy. assumed random ?
        This should probably just be a replay to whatever the strategy was in the first place (creation/construction of the type)
        """
        #  note : behavior semantics is union (coproduct / sum).
        # In this case environment makes the choice, so it s a union (determinism upon measurement)

        choice_completer = WordCompleter([
            'alligator', 'ant', 'ape', 'bat', 'bear', 'beaver', 'bee', 'bison',
            'butterfly', 'cat', 'chicken', 'crocodile', 'dinosaur', 'dog', 'dolphin',
            'dove', 'duck', 'eagle', 'elephant', 'fish', 'goat', 'gorilla', 'kangaroo',
            'leopard', 'lion', 'mouse', 'rabbit', 'rat', 'snake', 'spider', 'turkey',
            'turtle',
        ], ignore_case=True)

        #  TODO : move that into a prompt session
        # Create some history first. (Easy for testing.)
        history = InMemoryHistory()
        history.append_string('snake')

        return prompt_toolkit.prompt(message=f'{prptxt}>', history=history,
                                     completer=choice_completer, complete_style=CompleteStyle.READLINE_LIKE,
                                     auto_suggest=AutoSuggestFromHistory(),
                                     )

    def __call__(self, data: CTType) -> typing.Union[CTType, typing.Callable[[typing.Any], CTType]]:  # note a type hint in python is not enforced.
        """
        Parser, expecting CTType...
        :param data:
        :return:
        """
        try:
            data = self.impl(data)  # Python Type casting MUST be idempotent. TO CHECK...
        except ValueError as ve:
            print(ve)
            #  recurse (or suicide) if user can't get it right
            iter(self)
            data = next(self)

        return data



if __name__ == '__main__':

    ctt = CTType('CTT', 'B')


    ctt('not B so prompt')

    #ctt = ctt + 'B' + int



    #BorC = typing.NewType('BorC', CTType() )

    #CandD = CTType('C') * CTType('D')


    #td = BorC('WrongSoPrompt')
    #assert td == BorC.C




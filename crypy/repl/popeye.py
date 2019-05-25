"""
Prompter on failing to parse a type
Limiting ourselves to python typesfor now.
"""
from __future__ import annotations

import itertools
import typing

import enum
import prompt_toolkit

from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import CompleteStyle


# TODO : integrate with hypothesis ?
sample_elem = {
            bool: ['True', 'False'],
            # using the poptype will fill this up on success...
        }


class POPType:
    """
    'Parse or Prompt' Type
    Implementation of structure of type system.
    Inspired by Mellies Game Semantics and Harper's Computational Type Theory.
    Could also be used for interface to some kind of environment (game semantics?)
    """
    members: set

    def __init__(self, members: typing.Iterator[typing.Any]):  # TODO : improve typing here
        # TODO : clever way to discover all members (but not too many...)
        self.members = members

    def __mul__(self, other):
        """
        Mul another completer. Categorical Semantics: possible combinations
        :param other:
        :return:
        """
        result = POPCompoundType(fst=self, snd=other)
        # TODO : how to keep elems as they are ?
        return result

    def __add__(self, other):
        """
        Add another completer. Categorical Semantics: possible choice
        :param other:
        :return:
        """
        result = POPUnionType(self, other)
        # TODO : how to keep elems as they are ?
        return result

    def __call__(self, ): # draws members interactively / async ?
        # TODO / link with hypothesis strategies ?
        return WordCompleter(self.members)

    # TODO : __call__ is used for parsing... use another API ?


class POPUnionType(POPType):

    types: typing.Dict[typing.Any, POPType]  # python type (with unions) implementation
    session: prompt_toolkit.PromptSession

    def __init__(self, *types: typing.Type):
        """
        Parsing data, one at a time
        :param types: list of types to consider as union (sum)
        """

        # Magic on types to integrate with python
        self.types = {t: POPType(sample_elem.get(t, [])) for t in types}

        # TODO : introspect the type to generate members (hypothesis?)
        # when not possible or too many, fall back on sample_elem

        # Union means any of these...
        completer = WordCompleter(itertools.chain(self.types.values()))

        self.session = prompt_toolkit.PromptSession(
            message=str("+".join(self.types.keys())) + '? ',
            history=InMemoryHistory(),
            auto_suggest=AutoSuggestFromHistory(),
            completer=completer, complete_style=CompleteStyle.COLUMN,
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
            indata = self.session.prompt()
            for t in self.types.keys():
                try:
                    data = t(indata)
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
        parsed = None
        for t in self.types.keys():
            try:
                # parse
                parsed = t(data)
                # tODO : mix in default value...
            except ValueError as ve:
                print(ve)
                parsed = None

        if parsed is None:
            #  recurse (or suicide) if user can't get it right
            parsed = self.prompt()
            # TODO : infinite recurse ?

        # modifies for next session (next type)
        sample_elem.setdefault(type(parsed), list())
        sample_elem[type(parsed)].append(data)

        return parsed


class POPCompoundType:

    types: typing.Dict[str, POPType]  # python type (with unions) implementation
    session: prompt_toolkit.PromptSession

    def __init__(self, **types: typing.Type):
        """
        Parsing data, one at a time
        :param types: list of types to consider as union (sum)
        """

        # Magic on types to integrate with python
        self.types = {k: {t: POPType(sample_elem.get(t, []))} for k, t in types.items()}

        # TODO : introspect the type to generate members (hypothesis?)
        # when not possible or too many, fall back on sample_elem

        # Product means means any of these...
        completer = WordCompleter(itertools.product(self.types.values()))

        # TODO : multiline ? or just multiprompt ??
        self.session = prompt_toolkit.PromptSession(
            message=str("+".join(self.types.keys())) + '? ',
            history=InMemoryHistory(),
            auto_suggest=AutoSuggestFromHistory(),
            completer=completer, complete_style=CompleteStyle.COLUMN,
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
            # TODO : multi prompt / line
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
        # TODO : multi prompt / line
        try:
            # parse
            parsed = self.type(data)
            # tODO : mix in default value...
        except ValueError as ve:
            print(ve)
            #  recurse (or suicide) if user can't get it right
            parsed = self.prompt()
            # TODO : infinite recurse ?

        # modifies for next session (next type)
        sample_elem.setdefault(self.type, list())
        sample_elem[self.type].append(data)

        return parsed


if __name__ == '__main__':

    pi = POPUnionType(int)

    # succeeds
    ival = pi('42')

    # fails and prompt, forever
    pival = pi('fortytwo')


    pfi = POPType(type=float)

    pfi *= POPType(type=int)


    # succeeds
    fival = pfi(('3.14', '42'))

    # fails and prompt, forever
    pfival = pfi('fortytwo')



    psi = POPType(type=str)

    psi = POPType(type=int)


    # succeeds
    sival = psi(('charlie', '42'))

    # fails and prompt, forever
    psival = psi('fortytwo')






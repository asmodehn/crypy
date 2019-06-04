"""
Prompter on failing to parse a type
Limiting ourselves to python typesfor now.
"""
from __future__ import annotations

import copy
import functools
import inspect
import itertools
import typing
import collections.abc

import enum
import prompt_toolkit
import pydantic

from pydantic import BaseModel, ValidationError

from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import CompleteStyle

# TODO : integrate with hypothesis ?
sample_elem = {
    bool: ['True', 'False'],
    # using the poptype will fill this up on success...
}


Value = typing.TypeVar('Value')


class POPType:
    """
    Encapsulate a type to provide prompt session for it.
    We need to also contain the name (if any) under which it is known/stored to interface easily with prompt
    """
    name: typing.Optional[str]  # if none, no name yet.
    model: typing.Union[typing.Type, pydantic.BaseModel]  # TODO describe this union...
    session: prompt_toolkit.PromptSession  # session for this type

    @staticmethod
    def _display_error_loc(error: typing.Dict[str, typing.Any]) -> str:
        return ' -> '.join(str(l) for l in error['loc'])

    @staticmethod
    def _display_error_type_and_ctx(error: typing.Dict[str, typing.Any]) -> str:
        t = 'type=' + error['type']
        ctx = error.get('ctx')
        if ctx:
            return t + ''.join(f'; {k}={v}' for k, v in ctx.items())
        else:
            return t

    def __init__(self, model: typing.Union[typing.Any], name: typing.Optional[str] = None):
        self.name = name
        self.model = model

        # TODO : dynamic wordcompleter
        completer = WordCompleter(['alice', 'bob', 'charlie'])

        self.session = prompt_toolkit.PromptSession(
            completer=completer, complete_style=CompleteStyle.COLUMN,
        )

        # dynamically implement methods based on model, to be able to use dynamic duck typing ! Scary...

        def getitem(self, item):
            """emulate a hierarchy of encapsulated types"""
            if hasattr(self.model, item):
                if BaseModel in inspect.getmro(self.model):
                    ft = model.__annotations__.get(item)
                    return POPType(ft, item)
                elif model == typing.List:
                    return

        def setitem(self, item, value):
            pass

        def delitem(self, item):
            pass

        def iter(self):
            pass

        def len(self):
            pass

        if self.model in [int, float, complex]:
            pass

        elif self.model in BaseModel:
            self.__getitem__ = getitem
            self.__setitem__ = setitem
            self.__delitem__ = delitem
            self.__iter__ = iter
            self.__len__ = len

    def __call__(self, **data) -> POPInstance:
        inst = None
        while inst is None:
            try:
                inst = self.model(**data)
            except ValidationError as ve:
                for e in ve.errors():
                    # print error as pydantic would
                    print(f'{self._display_error_loc(e)}\n  {e["msg"]} ({self._display_error_type_and_ctx(e)})')

                    # diving into model to find proper location and its annotation
                    p = POPType(self.model, e['loc'])}

                    # TODO : debug that with nested structures !!

                    data.update(s)

                    eprompt = PydanticErrorPrompter(self.model, data, ve, self.session)
                    data = eprompt()
                    inst = None
        return inst


class POPInstance(Value):
    """
    Intent : Yoneda embedding of values (to be able to extend what a value can be)...
    Ref :John Hughes paper (cited in meyers talk about probabilistic differentiable programming)
    """
    type: POPType  # the instance name
    parser: typing.Optional[
        typing.Callable]  # callable to parse input and return data. Note pydantic doesnt propose this interface yet...
    prompt: typing.Callable  # prompt for this instance

    # TODO : we might want to store more things her that depends on the instance, rather than the type...

    def __init__(self, type: POPType, parser: typing.Optional[typing.Callable] = None) -> None:
        self.type = type
        self.parser = parser  # TODO : plug pydantic here as well...
        self.prompt = functools.partial(session.prompt,
                                        history=InMemoryHistory(),
                                        auto_suggest=AutoSuggestFromHistory(),
                                        )

    def __call__(self, **data: typing.Any) -> Value:
        """
        Prompts if needed and returns a value
        :param args:
        :param kwargs:
        :return:
        """

        inst = None
        while inst is None:
            try:
                inst = self.model(**data)
            except ValidationError as ve:
                for e in self.pydantic_error.errors():
                    # print error as pydantic would
                    print(f'{self._display_error_loc(e)}\n  {e["msg"]} ({self._display_error_type_and_ctx(e)})')

                    # diving into model to find proper location and its annotation
                    s = {e['loc']: POPType(self.model)}

                    # TODO : debug that with nested structures !!

                data.update(s)
                # return data

                # data = self.prompt(message = f'{self.name}: {self.type_hint} ?', *args, **kwargs)

                # PydanticErrorPrompter(self.model, data, ve, self.session)
                inst = None
        return inst


class POPSession:
    """
    A stackable prompt session
    """
    name: str  # the name under which this session needs to be stored (instance)
    model: typing.Union[typing.Type]  # TODO describe this union...
    value: typing.Union[None, typing.Any]  # TODO describe this union...
    session: prompt_toolkit.PromptSession

    def __init__(self, name: str, model: typing.Union[typing.Any], session: prompt_toolkit.PromptSession = None):
        self.name = name
        self.model = model

        # TODO : dynamic wordcompleter
        completer = WordCompleter(['alice', 'bob', 'charlie'])

        self.session = session if session is not None else prompt_toolkit.PromptSession(
            history=InMemoryHistory(),
            auto_suggest=AutoSuggestFromHistory(),
            completer=completer, complete_style=CompleteStyle.COLUMN,
        )

    def prompt_and_complete(self, *args, **kwargs):
        inpt = self.session.prompt(*args, **kwargs)
        # TODO : update wordcompleter

    def __call__(self, message_prefix=None, **kwargs):

        if self.model in [int, float]:
            return self.prompt_and_complete(message=f'{self.name}: {self.model} ?', **kwargs)
        elif BaseModel in inspect.getmro(self.model):
            for f, t in self.model.__annotations__.items():
                return {f: s for s in
                        POPSession(name=f, model=t)}  # Note session doesnt simply follow into nested field
        else:
            raise NotImplementedError

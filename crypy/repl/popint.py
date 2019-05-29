"""
Prompter on failing to parse a type
Limiting ourselves to python typesfor now.
"""
from __future__ import annotations

import itertools
import typing

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


#from pydantic.types import CallableGenerator
#from pydantic.main import Model, DictStrAny, DictError, change_exception

# hooking POPModel in the pydantic validator hierarchy
# class POPModel(pydantic.BaseModel):
#
#     @classmethod
#     def __get_validators__(cls) -> CallableGenerator:
#         yield cls.validate
#
#     @classmethod
#     def validate(cls: typing.Type[Model], value: typing.Union[DictStrAny, Model]) -> Model:
#         if isinstance(value, dict):
#             return cls(**value)
#         elif isinstance(value, cls):
#             return value.copy()
#         else:
#             with change_exception(DictError, TypeError, ValueError):
#                 return cls(**dict(value))  # type: ignore
#
#     def __call__(self, *args, **kwargs):
#         pass
#



class POP:

    session: prompt_toolkit.PromptSession
    model: typing.Type[BaseModel]

    def __init__(self,  model: typing.Type[BaseModel]) -> None:

        self.model = model

        # Product means means any of these...
        completer = WordCompleter(['alice', 'bob', 'charlie'])
        # TODO : better wordcompleter (define more precisely possible values, maybe dynamically)

        self.session = prompt_toolkit.PromptSession(
            message=str(model) + '? ',
            history=InMemoryHistory(),
            auto_suggest=AutoSuggestFromHistory(),
            completer=completer, complete_style=CompleteStyle.COLUMN,
        )

    def __call__(self, **data: typing.Any):

        inst = None
        while inst is None:
            try:
                inst = self.model(**data)
            except ValidationError as ve:
                print(ve)
                data = self.session.prompt()
                inst = None
        return inst




# class POPType:
#     # each instance has its own session
#     session: prompt_toolkit.PromptSession
#     model: POPBaseModel
#
#     def __init__(self, prompt_typename: str, model_type: typing.Type[BaseModel]) -> None:
#
#         self.model = model_type
#
#         # Product means means any of these...
#         completer = WordCompleter([])
#         # TODO : better wordcompleter (define more precisely possible values, maybe dynamically)
#
#         self.session = prompt_toolkit.PromptSession(
#             message=prompt_typename + '? ',
#             history=InMemoryHistory(),
#             auto_suggest=AutoSuggestFromHistory(),
#             completer=completer, complete_style=CompleteStyle.COLUMN,
#         )
#
#
#     def __call__(self, arg: typing.Optional[typing.Union[str, int]] = None):
#         """
#         calling a POPType instance attempts to parse, or prompt
#         :param arg:
#         :return:
#         """
#         if arg is None:
#             return self.val
#         else:
#             #  Parse or Prompt logic
#             try:
#                 self.val = arg
#             except Exception as e:
#                 while self.val is None:
#                     inpt = self.session.prompt(default=arg, accept_default=True)
#                     try:
#                         self.val = inpt  #  TODO : validate
#                     except Exception as e:
#                         print(e)




if __name__ == '__main__':

    from datetime import datetime
    from typing import List

    class User(BaseModel):
        id: int
        name = 'John Doe'
        signup_ts: datetime = None
        friends: List[int] = []

    POPUser = POP(User)

    # pydantic works as documented
    external_data = {'id': '123', 'signup_ts': '2017-06-01 12:22', 'friends': [1, '2', b'3']}
    user = POPUser(**external_data)

    # on errors, prompts:
    user = POPUser(signup_ts='broken', friends=[1, 2, 'not number'])










#
# class POPInt(POPType):
#     """
#     Integer as POPType
#     """
#
#     completer: WordCompleter
#     val: int
#
#     def __init__(self, prompt: str = 'int', default=0):
#
#         # TODO : introspect the type to generate members (hypothesis?)
#         # when not possible or too many, fall back on sample_elem
#
#         # Product means means any of these...
#         completer = WordCompleter()
#         # TODO : better wordcompleter (define more precisely possible values)
#
#         super(POPInt, self).__init__(prompt=prompt, default=default)
#
#     # Note: Different strategies ARE different types.
#     #  Prompt is a user strategy. assumed random ?
#     #  This should probably just be a replay to whatever the strategy was in the first place (creation/construction of the type)
#
#     #  note : behavior semantics is union (coproduct / sum).
#     # In this case environment makes the choice, so it s a union (determinism upon measurement)
#     def prompt(self):
#         data = None
#         while data is None:
#             # TODO : multi prompt / line
#             try:
#                 data = self.type(self.session.prompt())
#             except ValueError as ve:
#                 print(ve)
#                 data = None
#         return data
#
#     def __call__(self, data: str) -> self.type:  # note a type hint in python is not enforced.
#         """
#         Parser, expecting CTType...
#         :param data:
#         :return:
#         """
#         # TODO : multi prompt / line
#         try:
#             # parse
#             parsed = self.type(data)
#             # tODO : mix in default value...
#         except ValueError as ve:
#             print(ve)
#             #  recurse (or suicide) if user can't get it right
#             parsed = self.prompt()
#             # TODO : infinite recurse ?
#
#         # modifies for next session (next type)
#         sample_elem.setdefault(self.type, list())
#         sample_elem[self.type].append(data)
#
#         return parsed


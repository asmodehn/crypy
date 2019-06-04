from __future__ import annotations

import functools
import types

import hypothesis
from hypothesis.strategies import builds, integers, booleans, one_of
import typing
from pydantic import BaseModel, ValidationError, validate_model
import unittest

import prompt_toolkit
from prompt_toolkit.patch_stdout import patch_stdout


def prompt_patch(instance: BaseModel):
    """
    Patching pydantic because extending BaseModel seems to break the debugger currently (0.27)
    :param model:
    :return:
    """

    def process_values(self, input_data: typing.Any) -> typing.Dict[str, typing.Any]:
        # (casting here is slow so use ignore)
        values, errors = validate_model(self, input_data, raise_exc=False)  # type: ignore

        # CAREFUL : breakpoints here will break the debugger !!! (pydantic 0.27)

        if errors:
            if self.prompts:
                for e in errors.raw_errors:
                    print(e.msg)
                    f = getattr(self, e['loc'][0])
                    if self.prompts:
                        try:
                            f.type_.prompt(data=input_data.get('data'))
                        except Exception as e:
                            print(e)
                            raise e
                            # TODO : handle properly?
            else:
                raise errors
        else:
            return values

    def prompt(cls, data= None, again=False):  # data can be the previous prompt or default value...
        a = None
        with patch_stdout():
            data = prompt_toolkit.prompt(
                message=f"{cls.__name__}: ",
                async_=True,
                # TODO : prefill with default ? auto complete with previous ?
            )
            while a is None:
                if again:  # avoiding too deep
                    try:
                        a = cls.create(data_dict=data)
                    except ValidationError as ve:
                        # creation failed, loop instead of recursing in fixer_cb
                        a = None  # guarantee that we will loop
                else:
                    a = cls(prompts=False, **data)

        return a

    # Patching
    instance._process_values = types.MethodType(process_values, instance)  # instance method
    instance.prompts = prompt  # class method

    return instance

#
# class PromptBaseModel(BaseModel):
#
#     """
#     Extending Pydantic Base Model with a prompt function.
#     """
#     prompts: bool  # TODO : enrich with a prompt function / schema/ structure/ strategy, whatever you wanna call it
#
#     def __init__(self, prompts: bool = False, **data: typing.Any) -> None:
#         # CAREFUL : breakpoints here will break the debugger !!! (pydantic 0.27)
#         self.prompts = prompts
#         super().__init__(**data)
#
#
#     def _process_values(self, input_data: typing.Any) -> typing.Dict[str, typing.Any]:
#         # (casting here is slow so use ignore)
#         values, errors = validate_model(self, input_data, raise_exc=False)  # type: ignore
#
#         # CAREFUL : breakpoints here will break the debugger !!! (pydantic 0.27)
#
#         if errors:
#             if self.prompts:
#                 for e in errors.raw_errors:
#                     print(e.msg)
#                     f = self.get(e['loc'][0])
#                     if self.prompts:
#                         try:
#                             f.type_.prompt(data=input_data.get('data'))
#                         except Exception as e:
#                             print(e)
#                             raise e
#                             # TODO : handle properly?
#             else:
#                 raise errors
#         else:
#             return values
#
#     @classmethod
#     def prompt(cls, data= None, again=False):  # data can be the previous prompt or default value...
#         a = None
#         with patch_stdout():
#             data = prompt_toolkit.prompt(
#                 message=f"{cls.__name__}: ",
#                 async_=True,
#                 # TODO : prefill with default ? auto complete with previous ?
#             )
#             while a is None:
#                 if again:  # avoiding too deep
#                     try:
#                         a = cls.create(data_dict=data)
#                     except ValidationError as ve:
#                         # creation failed, loop instead of recursing in fixer_cb
#                         a = None  # guarantee that we will loop
#                 else:
#                     a = cls(prompts=False, **data)
#
#         return a


class Answer(BaseModel):

    data: int

    # Careful when playing with __init__, BaseModel.__getattr__ will break and so will the debugger

    def printme(self):
        print(self.data)
        # Complicated code will be here
        return True


Answer = prompt_patch(Answer)


class Nested(BaseModel):

    answer: Answer

    # Careful when playing with __init__, BaseModel.__getattr__ will break and so will the debugger

    def printme(self):
        print({
            'data': self.data
        })
        # Complicated code will be here
        return True

Nested = prompt_patch(Nested)


if __name__ == '__main__':


    # should work
    a1 = Answer(**{"data": "42"})

    assert a1.data == 42

    # that too
    a2 = Answer(data="42")
    assert a2.data == 42

    # or even that
    a3 = Answer(data=42)

    assert a3.data == 42

    # other ways will NOT
    # Answer(42)
    # Answer("42")
    # Answer({"data": "42"})
    # etc.

    # should prompt and loop until user gets it right
    Answer(data="bob")

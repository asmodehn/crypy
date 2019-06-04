import hypothesis
from hypothesis.strategies import builds, integers, booleans, one_of
import typing
from pydantic import BaseModel, ValidationError, validate_model
import unittest


class Answer(BaseModel):

    data: int

    def __init__(self, data: int):
        # keeping it around for syntaxchecker
        super().__init__(data=data)

    def printme(self):
        print(self.data)
        # Complicated code will be here
        return True


class Nested(BaseModel):

    answer: Answer

    def __init__(self, answer: Answer):
        # keeping it around for syntaxchecker
        super().__init__(answer=answer)

    def printme(self):
        print({
            'data': self.data
        })
        # Complicated code will be here
        return True


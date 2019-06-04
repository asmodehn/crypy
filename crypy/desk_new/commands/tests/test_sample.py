import hypothesis
from hypothesis.strategies import builds, integers, booleans, one_of
import typing
from pydantic import BaseModel, ValidationError, validate_model
import unittest

from ..sample import Answer


class TestAnswer(unittest.TestCase):

    # NOTE : later we can extract complex hypothesis test structures with pydantic into separate packages
    # already done for other parsers : https://hypothesis.readthedocs.io/en/latest/strategies.html#external-strategies

    @hypothesis.settings(verbosity=hypothesis.Verbosity.verbose)
    @hypothesis.given(a=hypothesis.infer)
    def test_printme(self, a: int):

        answer = Answer(a)
        assert answer.printme()


#TODO : test Nested
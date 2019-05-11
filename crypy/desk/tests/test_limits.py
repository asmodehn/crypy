import random

import pydantic
import pytest
from hypothesis import given, settings, Verbosity
from hypothesis.strategies import integers, floats, builds
from .. import bounds


# TODO : use bounds fixture


# TODO : test limits



if __name__ == "__main__":
    pytest.main(["-s", __file__])

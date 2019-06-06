from __future__ import annotations

import datetime
import functools
import types

import hypothesis
from hypothesis.strategies import builds, integers, booleans, one_of
import typing
from pydantic import BaseModel, ValidationError, validate_model
import unittest

import prompt_toolkit
from prompt_toolkit.patch_stdout import patch_stdout

import datetime as dt
from dataclasses import dataclass

from marshmallow import Schema, fields, pprint

# MODELS

@dataclass
class Email:
    user: str  # HOW TO enforce string content via types
    hostname: str  # HOWTO enforce string content via types ?


@dataclass(init=False)
class User:
    name: str
    email: Email
    created_at: datetime.datetime

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = dt.datetime.now()

    def __repr__(self):
        return '<User(name={self.name!r})>'.format(self=self)


# SCHEMAS ( how to convert to / from strings )
# Not a type check but a parsing validation ( not as strict, but probably more practical in python)


class UserSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()


user = User(name="Monty", email="monty@python.org")
schema = UserSchema()
result = schema.dump(user)
pprint(result)
# {"name": "Monty",
#  "email": "monty@python.org",
#  "created_at": "2014-08-17T14:54:16.049594+00:00"}


user_data = {
    'created_at': '2014-08-11T05:26:03.869245',
    'email': u'ken@yahoo.com',
    'name': u'Ken'
}
schema = UserSchema()
result = schema.load(user_data)
pprint(result)
# {'name': 'Ken',
#  'email': 'ken@yahoo.com',
#  'created_at': datetime.datetime(2014, 8, 11, 5, 26, 3, 869245)},

# TODO : plug tests (hypothesis) on that
# TODO : plug click on that
# TODO : plug repl prompt on that
# Note plugging json load/dump for neetwork already managed by marshmallow

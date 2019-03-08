#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

from pydantic import validator
from pydantic.dataclasses import dataclass
from dataclasses import field
import typing


try:
    from ..euc import mpmath
    from .errors import CrypyException
except (ImportError, ValueError):
    from crypy.euc import mpmath
    from crypy.desk.errors import CrypyException


"""
Module providing an interface to mpmath, allowing it to work with pydantic for runtime type enforcement
"""


class Exact(mpmath.mp.mpf):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return mpmath.mp.mpf(v)


class Interval(mpmath.iv.mpf):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return mpmath.iv.mpf(v)

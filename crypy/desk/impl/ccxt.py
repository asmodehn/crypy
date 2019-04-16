#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass

import numpy
import pandas
import pydantic
import typing

try:
    from ...euc import ccxt
    from ... import config
except (ImportError, ValueError):
    from crypy.euc import ccxt
    from crypy import config



"""
Module providing an interface to ccxt, allowing it to work with pydantic for runtime type enforcement.
Note the dataclasses here are pure python dataclasses.
pydantic is not involved in the type enforcement at this level.
"""


# Very simple wrapping for now...
# to limit the interaction points with ccxt.
# TODO : check data types (pydantic)
kraken = ccxt.kraken

bitmex = ccxt.bitmex

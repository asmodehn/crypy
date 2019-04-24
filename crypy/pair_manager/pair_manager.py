#!/usr/bin/env python
# coding: utf-8
import typing

import json



from ..desk.utils import formatTS

from .position_manager import Position_Manager
import strategy

try:
    from ..euc import ccxt
    from .. import config
except (ImportError, ValueError, ModuleNotFoundError):
    from crypy.euc import ccxt
    from crypy import config


class Manager:


    def __init__(self, conf: config.ExchangeSection = None):
        self.exchangeName = conf.name

        # Using the impl_hook from settings.ini
        self.exchange = conf.exec_hook(ccxt=ccxt)

    def info(self):
        return f"Trade Manager for {self.exchangeName} WIP"
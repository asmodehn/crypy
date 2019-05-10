#!/usr/bin/env python
# coding: utf-8
import typing

#import json
#from ..desk.utils import formatTS

import crypy.desk.global_vars as gv
from crypy.desk.errors import CrypyException

from .position_manager import Position_Manager
import strategy

try:
    from ..euc import ccxt
    from .. import config
except (ImportError, ValueError, ModuleNotFoundError):
    from crypy.euc import ccxt
    from crypy import config


class Manager:


    def __init__(self, conf: config.ExchangeSection = None, ticker = gv.defPAIR):
        
        #TODO use Desk instead of exchange directly

        self.exchangeName = conf.name

        # Using the impl_hook from settings.ini
        self.exchange = conf.exec_hook(ccxt=ccxt)

        self.symbol = gv.ticker2symbol[ticker]

        self.alarms = []

    def info(self):
        return f"Trade Manager for {self.symbol} on {self.exchangeName} WIP"

    def alarmsList(self):
        if len(self.alarms) > 0:
            list = ''

            "TODO better format"
            for alarm in self.alarms:
                list += f"{alarm.id} -> {alarm.definition} "

            return list

        else:
            return 'no alarm set atm'

    def alarmShow(self, id):
        try: 
            return self.alarms[id].definition
        except:
            raise CrypyException(msg = f"No alarm at id {id}")

    def alarmsCancel(self, id):
        "TODO multiple at same time"
        try: 
            del self.alarms[id]
        except:
            raise CrypyException(msg = f"No alarm at id {id}")

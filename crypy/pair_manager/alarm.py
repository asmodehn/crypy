#!/usr/bin/env python
# coding: utf-8

import typing
import datetime

operands = [
    "Crossing",
    "Crossing Up",
    "Crossing Down",
    "Greater Than",
    "Lesser Than",
    "Entering Range",
    "Exiting Range",
    "Inside Range",
    "Moving Up",
    "Moving Up %",
    "Moving Down",
    "Moving Down %"
]

timeframes = [
    "Only once",
    "Once per bar", 
    "Once per bar close",
    "Once per minute"
]

class Alarm:
    
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def definition(self) -> int:
        return self._definition

    @property
    def expiracy(self) -> datetime.datetime:
        return self._expiracy

    @property
    def timeframe(self) -> str:
        return self._tf

    def __init__(self, manager):
        self.manager = manager
        self.manager.alarms = []
        self.manager.alarms.append(self)
        self._id = 1

    def info(self):
        return f"Alarm management for {self.manager.exchangeName} WIP: {self.id}"

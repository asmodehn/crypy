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
    @id.setter
    def id(self, value):
        self._id = value
    
    @property
    def definition(self) -> str:
        return self._definition
    @definition.setter
    def definition(self, value):
        self._definition = value

    @property
    def expiracy(self) -> datetime.datetime:
        return self.expiracy

    @property
    def timeframe(self) -> str:
        return self.tf

    def __init__(self, manager):
        self.manager = manager

        self.data = {}
        self.definition =  "defintion text TODO"

    def execute(self):
        try:
            
            self.manager.alarms.append(self)
            self.id = len(self.manager.alarms) - 1

            return f"Alarm created, id: {self.id}"

        except Exception as error:
            return "Error: " + str(type(error)) + " " + str(error)

    def cancel(alarm):
        "TODO"
        pass

    

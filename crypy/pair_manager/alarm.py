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

triggers = [
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

    def __init__(self, alarmsList, timeframe, trigger, expiracy, indicator, indicator_value, operand, check, check_value):
        self.alarmsList = alarmsList

        self.data = {
            'timeframe':timeframe,
            'trigger': trigger,
            'expiracy': expiracy,
            'indicator': indicator,
            'indicator_value': indicator_value,
            'operand': operand,
            'check': check,
            'check_value': check_value
        }
        self.definition =  f"Alert {self.data['trigger']} when {self.data['indicator']}({self.data['indicator_value']}) {self.data['operand']} {self.data['check']}({self.data['check_value']}) for the {self.data['timeframe']} timeframe" + ( f" before {self.data['expiracy']}" if self.data['expiracy'] is not None else "")


    def execute(self):
        try:
            
            self.alarmsList.append(self)
            self.id = len(self.alarmsList) - 1

            return f"Alarm created, id: {self.id}"

        except Exception as error:
            return "Error: " + str(type(error)) + " " + str(error)

    def cancel(alarm):
        "TODO"
        pass

    

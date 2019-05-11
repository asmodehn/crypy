#!/usr/bin/env python
# coding: utf-8


class Alarm:


    def __init__(self, manager):
        self.manager = manager

    def info(self):
        return f"Alarm management for {self.manager.exchangeName} WIP"

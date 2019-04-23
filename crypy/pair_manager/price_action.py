#!/usr/bin/env python
# coding: utf-8


class Price_Action:


    def __init__(self, manager):
        self.manager = manager

    def info(self):
        return f"Price Action management for {self.manager.exchangeName} WIP"

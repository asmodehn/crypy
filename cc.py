#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 15:51:55 2019

@author: alexv
"""

import cryptocompare
print(cryptocompare.get_coin_list(format=False))
print(cryptocompare.get_price('BTC'))

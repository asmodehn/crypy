#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 15:51:55 2019

@author: alexv
"""

import cryptocompare
cryptocompare.get_coin_list(format=False)
cryptocompare.get_price('BTC')

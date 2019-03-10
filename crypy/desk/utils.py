#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import datetime

class Utils:
    def formatTS(msts):
        """Format a UNIX timestamp in millesecond to truncated ISO8601 format"""
        #TODO look into import arrow https://github.com/crsmithdev/arrow
        return datetime.datetime.utcfromtimestamp(msts/1000).strftime("%Y-%m-%d %H:%M:%S")


    def ppJSON(res):
        """Pretty-print a JSON result"""
        if res is not None:
            print(json.dumps(res, indent=2))
    
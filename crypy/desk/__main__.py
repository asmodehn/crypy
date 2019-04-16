#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cli import cli
from capital_cli import capital
from order_cli import order_group

"""Entrypoint for the desk subpackage
Manages one (currently) exchange, via CLI
"""

if __name__ == '__main__':
    #try:
        cli()
    #except:
    #     pass

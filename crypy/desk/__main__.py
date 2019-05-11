#!/usr/bin/env python
# -*- coding: utf-8 -*-

from crypy.desk.desk_cli import cli_root_group as cli
from crypy.desk.capital_cli import capital_group
from crypy.desk.order_cli import order_group

"""Entrypoint for the desk subpackage
Manages one (currently) exchange, via CLI
"""

if __name__ == '__main__':
    #try:
        cli()
    #except:
    #     pass

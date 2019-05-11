#!/usr/bin/env python
# -*- coding: utf-8 -*-

from crypy.pair_manager.pair_manager_cli import cli_root_group as cli
from crypy.pair_manager.price_action_cli import price_action_group
from crypy.pair_manager.alarm_cli import alarm_group

"""Entrypoint for the pair_manager subpackage
Manages one pair
One instance for one managed pair
"""

if __name__ == '__main__':
    #try:
        cli()
    #except:
    #     pass

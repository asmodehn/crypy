#!/usr/bin/env python
from __future__ import unicode_literals

import os

from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.widgets import Dialog
from ptterm import Terminal

import click
from click_repl import repl as crepl
import sys
#import sqlite3
import prompt_toolkit
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
#from pygments.lexers.sql import SqlLexer


# TODO : https://python-prompt-toolkit.readthedocs.io/en/stable/pages/tutorials/repl.html

def start_repl(ctx, exchange):

    prompt_toolkit.shortcuts.clear()
    click.echo(f"-== PAIR MANAGER CLI ==-")
    click.echo(f"EXCHANGE: {exchange}")
    # ctx.invoke(help) #TODO invoke help cmd on startup

    # Setup the prompt
    # https://python-prompt-toolkit.readthedocs.io/en/stable/pages/reference.html?prompt_toolkit.shortcuts.Prompt#prompt_toolkit.shortcuts.PromptSession
    prompt_kwargs = {
        'message': f"{exchange}> ",
        'history': prompt_toolkit.history.FileHistory(os.path.join(sys.path[0], 'crypy.hist')),
        # TODO don't use os.path
        'auto_suggest': prompt_toolkit.auto_suggest.AutoSuggestFromHistory(),
        'wrap_lines': True,
        'bottom_toolbar': [
            # ('class:bottom-toolbar-logo', ' Ϟ ') #TODO setup
        ]
    }

    # launching repl
    return crepl(ctx, prompt_kwargs=prompt_kwargs, allow_system_commands=False)

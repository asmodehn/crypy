import click
import prompt_toolkit

import crypy.desk.global_vars as gv

from .alarm import Alarm
from .pair_manager_cli import cli_root_group


manager = None

### CLI Alarm Sub Commands
@cli_root_group.group('alarm')
@click.pass_context
def alarm_group(ctx):
    """
    Managing Alarms for the pair
    """
    click.echo(f"Alarms")
    global manager
    if manager is None:
        manager = ctx.obj['manager']

@alarm_group.command()
@click.pass_context
def info(ctx):
    """
    """
    alarm = Alarm(manager)
    print(alarm.info())

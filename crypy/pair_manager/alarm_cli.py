import click
import prompt_toolkit

import crypy.desk.global_vars as gv
from crypy.desk.errors import CrypyException

from .alarm import Alarm
from .pair_manager_cli import cli_root_group


manager = None

### CLI Alarm Sub Commands
@cli_root_group.group('alarm', invoke_without_command=True)
@click.pass_context
def alarm_group(ctx, id = None):
    """
    Managing Alarms for the pair
    """
    global manager
    if manager is None:
        manager = ctx.obj['manager']

    #NO subcommand, we want to create/update an alarm
    if ctx.invoked_subcommand is None:
        alarm = Alarm(manager)

        if id is None:
            click.echo(f'Do you want to create the following alarm on {manager.symbol} ?')
        else:
            click.echo(f'Do you want to update the following alarm on {manager.symbol} ?')

        print(alarm.definition)

        if click.confirm('Please confirm'): #abort (but don't die!) here if No is selected (default) otherwise continue code below
            print(alarm.execute())
        else:
            print("alarm creation aborted")

    else: #there is a subcommand -> run it
        pass


@alarm_group.command()
@click.pass_context
def list(ctx):
    """
    list alarms
    """
    print(manager.alarmsList());

@alarm_group.command()
@click.pass_context
def cancel(ctx):
    """
    cancel alarm
    """
    id = 0 #TODO get id from cli
    try: 
        print(f"Cancel the following alarm: {manager.alarmShow(id)} ?")

        if click.confirm('Please confirm'): #abort (but don't die!) here if No is selected (default) otherwise continue code below
            manager.alarmsCancel(id)
            print("done")
        else:
            print("alarm cancelation aborted")

    except CrypyException as error:
        print(error.args[0])
    

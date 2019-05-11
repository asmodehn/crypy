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
            print("Alarm creation aborted")

    else: #there is a subcommand -> run it
        pass


@alarm_group.command()
@click.pass_context
def list(ctx):
    """
    list alarms
    """
    try: 
        print(manager.alarmsList())

    except CrypyException as error:
        print(error.args[0])

@alarm_group.command()
@click.argument('id', nargs=1, type=int, required=True)
@click.pass_context
def cancel(ctx, id):
    """
    Cancel alarm at Id
    """
    try: 
        print(f"Cancel the following alarm: {manager.alarmShow(id)} ?")

        if click.confirm('Please confirm'): #abort (but don't die!) here if No is selected (default) otherwise continue code below
            manager.alarmsCancel(id)
            print("Done")
        else:
            print("Alarm cancelation aborted")

    except CrypyException as error:
        print(error.args[0])
    

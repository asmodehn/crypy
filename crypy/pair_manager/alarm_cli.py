import click
from click_datetime import Datetime
import prompt_toolkit

import crypy.desk.global_vars as gv
from crypy.desk.errors import CrypyException

from . import alarm
from .pair_manager_cli import cli_root_group


manager = None

### CLI Alarm Sub Commands
@cli_root_group.group('alarm')
@click.pass_context
def alarm_group(ctx):
    """
    Manage pair's alarm
    """
    global manager
    if manager is None:
        manager = ctx.obj['manager']


@alarm_group.command()
#@click.option('-id', '--id', type=int, help="id of alarm to edit", required = False)
@click.option('-tf', '--timeframe', default='1h', type=click.Choice(['1m', '5m', '1h', '1d']), show_default=True, help="valid timeframe for exchange") #TODO choices must depend on desk.exchange.timeframes
@click.option('-tr', '--trigger', type=click.Choice(alarm.triggers), help="trigger for the alarm", required = True, default = alarm.triggers[0], show_default = True)
@click.option('-exp', '--expiracy', type=Datetime(format='%Y-%m-%d'), help="expiracy for the alarm", default=None, required=False)
#@click.option('-a', '--action', help="action for the alarm", default=None, required=False) #TODO a list of action for the alarm

@click.argument('indicator', nargs=1, type=str, required=True)
@click.argument('indicator_value', nargs=1, type=str, required=True)
@click.argument('operand', nargs=1, type=click.Choice(alarm.operands), required=True)
@click.argument('check', nargs=1, type=str, required=True)
@click.argument('check_value', nargs=1, type=str, required=True)

@click.pass_context
def new(ctx, timeframe, trigger, expiracy, indicator, indicator_value, operand, check, check_value):
    """
    Create a new alarm
    """
    try: 
        myAlarm = alarm.Alarm(alarmsList = manager.alarms, timeframe = timeframe, trigger = trigger, expiracy = expiracy, indicator = indicator, indicator_value = indicator_value, operand = operand, check = check, check_value = check_value)

        #if id is None:
        click.echo(f'Do you want to create the following alarm on {manager.symbol} ?')
        #else:
        #    click.echo(f'Do you want to update the following alarm on {manager.symbol} ?')

        print(myAlarm.definition)

        if click.confirm('Please confirm'): #abort (but don't die!) here if No is selected (default) otherwise continue code below
            print(myAlarm.execute())
        else:
            print("Alarm creation aborted")

    except CrypyException as error:
        print(error.args[0])


@alarm_group.command()
@click.pass_context
def list(ctx):
    """
    List alarms
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

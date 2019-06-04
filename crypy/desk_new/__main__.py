from crypy.desk_new.commands import Answer


import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--h', '--help', '?'])


@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=False)
@click.pass_context
def cli_group_example(ctx):
    click.echo(f"Ask stuff")


@cli_group_example.command('ask')
@click.option('-a', '--answer', type=int, default=42, show_default=True,
              help='comma delimited list of assets to restrict output to')
@click.pass_obj
def click_cmd_exmple(obj, answer):
    a = Answer(answer)
    a.printme()

    return 0  # shell success


@cli_group_example.command('repl')
@click.pass_obj
def cli_repl(obj):
    from crypy.desk_new.app import scheduler
    scheduler()
    return 0  # shell success


@cli_group_example.command('tryme')
@click.pass_obj
def tryme(obj):
    import unittest
    from .commands.tests import TestAnswer
    # initialize the test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # add tests to the test suite
    suite.addTests(loader.loadTestsFromTestCase(TestAnswer))

    # initialize a runner, pass it your suite and run it
    runner = unittest.TextTestRunner(verbosity=3)
    return runner.run(suite)


cli_group_example()



import click
import prompt_toolkit

from desk_cli import cli_root_group

### CLI CAPITAL manager Sub Commands
@cli_root_group.group('capital')
@click.pass_context
def capital_group(ctx):
    """
    Managing capital for the exchange (all pairs)
    """
    click.echo(f"Capital")

@capital_group.command()
@click.pass_context
def balance(ctx):
    """Capital: user balance"""
    print("wip")


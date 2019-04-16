import click
import prompt_toolkit

from cli import cli

### CLI CAPITAL manager Sub Commands
@cli.group()
@click.pass_context
def capital(ctx):
    """
    Managing capital for the exchange (all pairs)
    """
    click.echo(f"Capital")

@capital.command()
@click.pass_context
def balance(ctx):
    """Capital: user balance"""
    print("wip")


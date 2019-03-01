#!/usr/bin/env python
from __future__ import unicode_literals

import dataclasses

import click

from crypy.config import Config, resolve, default_filename
from crypy.desk.repl import repl
from crypy.desk.exchange import exchange

"""Entrypoint for the desk subpackage
Manages one (currently) exchange, via CLI
"""


@click.group()
@click.option('-c', '--config', help=f'config filepath. Will default to {resolve(default_filename)}')
@click.pass_context
def cli(ctx, config):
    conf = Config(config) if config is not None else Config()
    ctx.obj = conf


@click.command()
@click.option('-p', '--public', is_flag=True, default=False, help='public only')
@click.pass_obj
def bitmex(obj, public):

    assert 'bitmex.com' in obj.sections.keys()  # preventing errors early

    if public:
        exconf = obj.sections.get('bitmex.com').public()
    else:
        exconf = obj.sections.get('bitmex.com')

    # we never display the key and secret
    click.echo(exconf)

    x = exchange(hostname='bitmex.com', **dataclasses.asdict(exconf))

    print(x.markets)


@click.command()
@click.option('-p', '--public', is_flag=True, default=False, help='public only')
@click.pass_obj
def kraken(obj, public):

    assert 'kraken.com' in obj.sections.keys()  # preventing errors early

    if public:
        exconf = obj.sections.get('kraken.com').public()
    else:
        exconf = obj.sections.get('kraken.com')

    click.echo(exconf)

    x = exchange(hostname='kraken.com', **dataclasses.asdict(exconf))

    print(x.markets)


cli.add_command(kraken)
cli.add_command(bitmex)


if __name__ == '__main__':
    cli()

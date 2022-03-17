#!/usr/bin/env python

import os
import click
from configparser import ConfigParser
from pathlib import Path

from logsight.user import LogsightUser

from src.application import application
from src.log import log
from src.compare import compare
from src.incident import incident
from src.transformation import transformation


CONFIG_FILE = os.path.join(str(Path.home()), '.logsight')
cp = ConfigParser()
cp.read(CONFIG_FILE)

CONFIG = {i: None for i in ['EMAIL', 'PASSWORD', 'APP_ID']}
CONFIG.update({i: cp['DEFAULT'][i] for i in CONFIG.keys()
               if cp.has_option('DEFAULT', i)})
CONFIG.update({i: os.environ[f'LOGSIGHT_{i}'] for i in CONFIG.keys()
               if f'LOGSIGHT_{i}' in os.environ})

VERSION = '2022.03.14'


@click.group(help="CLI tool to manage logsight.ai artifacts")
@click.version_option(VERSION)
@click.pass_context
@click.option('--debug/--no-debug', default=False)
@click.option('--email', default=CONFIG['EMAIL'], help='email of logsight user.')
@click.option('--password', default=CONFIG['PASSWORD'], help='password of logsight user.')
@click.option('--json', default=False, is_flag=True, help='output returned as a json structure.')
@click.option('--app_id', default=CONFIG['APP_ID'], help='app_id to use as default.')
def cli(ctx, debug, json, email, password, app_id):
    if not email or not password:
        click.echo(f"Authentication incomplete: EMAIL {'found' if email else 'not found'}, "
                   f"PASSWORD {'found' if email else 'not found'}.")
        exit(1)

    ctx.obj['USER'] = LogsightUser(email=email, password=password)
    ctx.obj['APP_ID'] = app_id
    ctx.obj['DEBUG'] = debug
    ctx.obj['JSON'] = json

    if debug:
        click.echo(f"Config file found? {'yes' if Path(CONFIG_FILE).is_file() else 'no'}")
        click.echo(f"EMAIL: {email}, PASSWORD: {password}")


@cli.command()
@click.pass_context
def config(ctx):
    """
    Show configuration
    """
    u = ctx.obj['USER']
    a = ctx.obj['APP_ID']
    click.echo(f"EMAIL: {u.email}, PASSWORD: {u.password}, APP_ID: {a}")


cli.add_command(application.apps)
cli.add_command(log.log)
cli.add_command(compare.compare)
cli.add_command(incident.incident)
cli.add_command(transformation.transform)


if __name__ == "__main__":
    cli(obj={})

#!/usr/bin/env python

import os
import click
from configparser import ConfigParser
from pathlib import Path
from prettytable import PrettyTable

from logsight.user import LogsightUser

from src.application import application
from src.log import log
from src.compare import compare
from src.incident import incident
from src.transformation import transformation

LOGSIGHT_OPTIONS = ['EMAIL', 'PASSWORD', 'APP_ID', 'DEBUG', 'JSON']

CONFIG_FILE = os.path.join(str(Path.home()), '.logsight')
cp = ConfigParser()
cp.read(CONFIG_FILE)

CONFIG = {i: None for i in LOGSIGHT_OPTIONS}
CONFIG.update({i: cp['DEFAULT'][i] for i in CONFIG.keys()
               if cp.has_option('DEFAULT', i)})
CONFIG.update({i: os.environ[f'LOGSIGHT_{i}'] for i in CONFIG.keys()
               if f'LOGSIGHT_{i}' in os.environ})

VERSION = '0.0.7'


@click.group(help="CLI tool to manage logsight.ai artifacts")
@click.version_option(VERSION, prog_name='Logsight CLI')
@click.pass_context
@click.option('--debug/--no-debug', default=CONFIG['DEBUG'])
@click.option('--email', default=CONFIG['EMAIL'], help='Email of logsight user.')
@click.option('--password', default=CONFIG['PASSWORD'], help='Password of logsight user.')
@click.option('--json', default=False, is_flag=True, help='Output returned as a json structure.')
@click.option('--app_id', default=CONFIG['APP_ID'], help='Application ID to use as default.')
def cli(ctx, debug, json, email, password, app_id):
    if not email or not password:
        click.echo(f"Authentication incomplete: EMAIL {'found' if email else 'not found'}, "
                   f"PASSWORD {'found' if email else 'not found'}.")
        exit(1)

    ctx.obj['EMAIL'] = email
    ctx.obj['PASSWORD'] = password
    ctx.obj['APP_ID'] = app_id
    ctx.obj['DEBUG'] = debug
    ctx.obj['JSON'] = json

    ctx.obj['USER'] = LogsightUser(email=email, password=password)


@cli.command()
@click.pass_context
def config(ctx):
    """
    Show configuration
    """
    click.echo(f"Config file found? {f'yes ({Path(CONFIG_FILE)})' if Path(CONFIG_FILE).is_file() else 'no'}")
    table = PrettyTable(['OPTION', 'VALUE'])
    table.align = 'l'
    for i in LOGSIGHT_OPTIONS:
        table.add_row([i, ctx.obj[i]])
    click.echo(table)


cli.add_command(application.apps)
cli.add_command(log.log)
cli.add_command(compare.compare)
cli.add_command(incident.incident)
cli.add_command(transformation.transform)


if __name__ == "__main__":
    cli(obj={})

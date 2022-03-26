#!/usr/bin/env python

import sys
import os
from configparser import ConfigParser
from pathlib import Path

import json as js
import click
from prettytable import PrettyTable

from logsight.user import LogsightUser

from logsight_cli.application import application
from logsight_cli.log import log
from logsight_cli.compare import compare
from logsight_cli.incident import incident
from logsight_cli.utils import utils


LOGSIGHT_OPTIONS = ["EMAIL", "PASSWORD", "APP_ID", "DEBUG", "JSON"]
CONFIG = dict.fromkeys(LOGSIGHT_OPTIONS, (None, None))

CONFIG_FILE = os.path.join(str(Path.home()), ".logsight")
cp = ConfigParser()
cp.read(CONFIG_FILE)

CONFIG.update(
    {
        i: (cp["DEFAULT"][i], CONFIG_FILE)
        for i in LOGSIGHT_OPTIONS
        if cp.has_option("DEFAULT", i)
    }
)
CONFIG.update(
    {
        i: (os.environ[f"LOGSIGHT_{i}"], 'Environment')
        for i in LOGSIGHT_OPTIONS
        if f"LOGSIGHT_{i}" in os.environ
    }
)

VERSION = '0.0.41'


@click.group(help="CLI tool to manage logsight.ai artifacts")
@click.version_option(VERSION, prog_name="Logsight CLI")
@click.pass_context
@click.option("--debug/--no-debug")
@click.option("--email", help="User e-mail.")
@click.option("--password", help="User password.")
@click.option("--json", help="Output as JSON.", is_flag=True)
@click.option("--app_id", help="Default app ID.")
def cli(ctx, debug, json, email, password, app_id):

    for k in LOGSIGHT_OPTIONS:
        if locals().get(k.lower()):
            CONFIG[k] = (locals().get(k.lower()), 'Option')

    for k in LOGSIGHT_OPTIONS:
        ctx.obj[k] = CONFIG[k][0]
        if k in ['DEBUG', 'JSON'] and ctx.obj[k] is not None:
            ctx.obj[k] = js.loads(ctx.obj[k].lower())

    ctx.obj["USER"] = LogsightUser(email=ctx.obj["EMAIL"],
                                   password=ctx.obj["PASSWORD"])

    if not ctx.obj["EMAIL"] or not ctx.obj["PASSWORD"]:
        click.echo('Authentication incomplete')
        echo_config()
        sys.exit(1)


@cli.command()
def config():
    """
    Show configuration
    """
    echo_config()
    sys.exit(0)


def echo_config():
    table = PrettyTable(["OPTION", "VALUE", "SOURCE"])
    table.align = "l"
    for i in LOGSIGHT_OPTIONS:
        table.add_row([i, CONFIG[i][0], CONFIG[i][1]])
    click.echo(table)


cli.add_command(application.apps)
cli.add_command(log.log)
cli.add_command(compare.compare)
cli.add_command(incident.incident)
cli.add_command(utils.utils)


def main():
    cli(obj={})


if __name__ == "__main__":
    cli(obj={})

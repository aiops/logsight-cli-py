#!/usr/bin/env python

import sys
import os
import json
from configparser import ConfigParser
from pathlib import Path
import pkg_resources
from packaging import version
import importlib.metadata

import json as js
import click
from prettytable import PrettyTable

import logsight.config
from logsight.authentication import LogsightAuthentication

from logsight_cli.log import log
from logsight_cli.compare import compare
from logsight_cli.incident import incident
from logsight_cli.utils import utils


LOGSIGHT_VERSION_MIN = '0.2.6'
if version.parse(importlib.metadata.version('logsight-sdk-py')) < \
        version.parse(LOGSIGHT_VERSION_MIN):
    raise EnvironmentError(
        f'logsight-sdk-py version too low, required >= {LOGSIGHT_VERSION_MIN}')


PYTHON_VERSION_MIN = (3, 8, 0)
if not sys.version_info >= PYTHON_VERSION_MIN:
    raise EnvironmentError(
        f'Python version too low, required >= {".".join(str(n) for n in PYTHON_VERSION_MIN)}')


LOGSIGHT_OPTIONS = ['HOST_API', 'EMAIL', 'PASSWORD', 'DEBUG', 'JSON']
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


VERSION = pkg_resources.require('logsight-cli-py')[0].version


@click.group(help="CLI tool to manage logsight.ai artifacts")
@click.version_option(VERSION, prog_name="Logsight.ai CLI")
@click.pass_context
@click.option("--debug/--no-debug")
@click.option("--json", help="Output as JSON.", is_flag=True)
@click.option("--host_api", help="Logsight host API.")
@click.option("--email", help="User e-mail.")
@click.option("--password", help="User password.")
def cli(ctx, debug, json, host_api, email, password):

    for k in LOGSIGHT_OPTIONS:
        if locals().get(k.lower()):
            CONFIG[k] = (locals().get(k.lower()), 'Option')

    for k in LOGSIGHT_OPTIONS:
        ctx.obj[k] = CONFIG[k][0]
        if k in ['DEBUG', 'JSON'] and ctx.obj[k] is not None:
            ctx.obj[k] = js.loads(str(ctx.obj[k]).lower())

    if ctx.obj['HOST_API']:
        logsight.config.set_host(ctx.obj['HOST_API'])

    ctx.obj['AUTHENTICATION'] = LogsightAuthentication(email=ctx.obj['EMAIL'],
                                                       password=ctx.obj['PASSWORD'])

    if not ctx.obj['EMAIL'] or not ctx.obj['PASSWORD']:
        click.echo('Authentication incomplete')
        echo_config()
        sys.exit(1)


@cli.command()
@click.pass_context
def config(ctx):
    """
    Show configuration
    """
    echo_config(ctx)
    sys.exit(0)


def echo_config(ctx):
    keys = ['option', 'value', 'source']
    config = [{keys[0]: i, keys[1]: CONFIG[i][0], keys[2]: CONFIG[i][1]} for i in LOGSIGHT_OPTIONS]
    if ctx.obj['JSON']:
        s = json.dumps(config, sort_keys=True, indent=4)
        click.echo(s)
    else:
        table = PrettyTable(keys)
        table.align = "l"
        for opt in config:
            table.add_row([opt.get(k, '') for k in keys])
        click.echo(table)


cli.add_command(log.log)
cli.add_command(compare.compare)
cli.add_command(incident.incident)
cli.add_command(utils.utils)


def main():
    cli(obj={})


if __name__ == "__main__":
    cli(obj={})

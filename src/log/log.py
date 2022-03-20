import sys
import json

import click
from prettytable import PrettyTable

from logsight.logs import LogsightLogs
from logsight.exceptions import APIException
from logsight.compare import LogsightCompare


@click.group()
@click.pass_context
def log(ctx):
    """Manages log files"""


@log.command("upload")
@click.pass_context
@click.argument("file", type=click.Path(exists=True))
@click.option("--tag", help="tag to index the log file.")
@click.option("--app_id", help="application id.")
def upload(ctx, file, tag, app_id):
    """
    Upload a log file to an application

    FILE is the name of the log file

    python -m cli.ls-cli log upload <file> --tag v1 --app_id <applicationId>
    """
    u = ctx.obj["USER"]
    a = app_id or ctx.obj["APP_ID"]

    try:
        logs = LogsightLogs(u.token)
        r = logs.upload(a, file, tag=tag)
        flush_id = logs.flush(r["receiptId"])

        if ctx.obj["JSON"]:
            click.echo(json.dumps(flush_id, sort_keys=True, indent=4))
        else:
            click.echo(f'flush_id: {flush_id["flushId"]}')

    except APIException as e:
        click.echo(f"Unable to upload log file to application ({e})")
        sys.exit(1)

    sys.exit(0)


@log.group('tag')
@click.pass_context
def tag_(ctx):
    """Management of tags"""


@tag_.command()
@click.pass_context
@click.option("--app_id", help="application id.")
def ls(ctx, app_id):
    """
    List the tags of logs

    python -m cli.ls-cli log tag ls --app_id <applicationId>
    """
    u = ctx.obj["USER"]
    a = app_id or ctx.obj["APP_ID"]

    try:

        cmp_mng = LogsightCompare(u.user_id, u.token)

        if ctx.obj["JSON"]:
            click.echo(json.dumps(cmp_mng.tags(a), sort_keys=True, indent=4))
        else:
            table = PrettyTable(["TAG", "VIEW"])
            table.align = "l"
            for i in cmp_mng.tags(a):
                table.add_row([i["tag"], i["tagView"]])
            click.echo(table)

    except APIException as e:
        click.echo(f"Unable to retrieve tags ({e})")
        sys.exit(1)

    sys.exit(0)

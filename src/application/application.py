import sys
import json

import click
from prettytable import PrettyTable

from logsight.application import LogsightApplication
from logsight.exceptions import APIException


@click.group("application")
@click.pass_context
def apps(ctx):
    """Manages applications"""


@apps.command()
@click.pass_context
def ls(ctx):
    """
    lists applications registered

    python -m src.logsight_cli application ls
    """
    u = ctx.obj["USER"]

    try:

        app_mng = LogsightApplication(u.user_id, u.token)

        if ctx.obj["JSON"]:
            click.echo(json.dumps(app_mng.lst(), sort_keys=True, indent=4))
        else:
            table = PrettyTable(["APPLICATION ID", "NAME"])
            table.align = "l"
            for a in app_mng.lst()["applications"]:
                table.add_row([a["applicationId"], a["name"]])
            click.echo(table)

    except APIException as e:
        click.echo(f"Unable to retrieve application list ({e})")
        sys.exit(1)

    sys.exit(0)


@apps.command()
@click.pass_context
@click.option("--name", help="name of the application.")
def create(ctx, name):
    """Creates an application

    python -m src.logsight_cli application create --name app_name
    """
    u = ctx.obj["USER"]

    try:

        app_mng = LogsightApplication(u.user_id, u.token)
        r = app_mng.create(name)

        if ctx.obj["JSON"]:
            click.echo(json.dumps(r, sort_keys=True, indent=4))
        else:
            click.echo(f"app_id: {r['applicationId']}")

    except APIException as e:
        click.echo(f"Unable to create application name: {name} ({e})")
        sys.exit(1)

    sys.exit(0)


@apps.command()
@click.pass_context
@click.option("--app_id", help="name of the application.")
def delete(ctx, app_id):
    """Deletes an application

    python -m src.logsight_cli application delete --app_id app_id
    """
    u = ctx.obj["USER"]
    a = app_id or ctx.obj["APP_ID"]

    try:

        app_mng = LogsightApplication(u.user_id, u.token)
        app_mng.delete(a)

    except APIException as e:
        click.echo(f"Unable to delete application name ({e})")
        sys.exit(1)

    sys.exit(0)

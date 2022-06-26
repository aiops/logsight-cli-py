import sys
import json
import time
import click
from tqdm import tqdm
from prettytable import PrettyTable

from logsight.compare import LogsightCompare
from logsight.exceptions import Conflict, BadRequest, NotFound


N_CALL_RETRIES = 10

# TODO: to implement
# PATH_GET_COMPARE = "logs/compare"
# PATH_POST_COMPARE = "logs/compare"
# PATH_GET_COMPARE_ID = "logs/compare/{compareId}"
# PATH_DELETE_COMPARE = "logs/compare/{compareId}"
# PATH_POST_COMPARE_STATUS = "logs/compare/status"


@click.group()
@click.pass_context
def compare(_):
    """Compares log files"""


@compare.command()
@click.pass_context
@click.option("--app_id", help="id of the application")
@click.option("--tags", required=True, type=click.Tuple([str, str]),
              help="tags to use during comparison")
@click.option("--flush_id", help="flush id")
def log(ctx, app_id, tags, flush_id):
    """
    compare indexed logs

    python -m src.logsight_cli compare log \
    --app_id <applicationId> --tags <tag_v1> <tag_v2> --flush_id <flushId>
    """
    u = ctx.obj['AUTHENTICATION']
    a = app_id or ctx.obj["APP_ID"]

    comp = LogsightCompare(u.user_id, u.token)
    for _ in (
        td := tqdm(
            range(1, N_CALL_RETRIES + 1),
            desc="Call retries",
            colour="white",
            file=sys.stdout,
            disable=not ctx.obj["DEBUG"],
        )
    ):
        td.refresh()
        try:
            r = comp.compare(
                app_id=a,
                baseline_tag=tags[0],
                candidate_tag=tags[1],
                flush_id=flush_id,
                verbose=ctx.obj["DEBUG"],
            )

            if ctx.obj["JSON"]:
                s = json.dumps(r, sort_keys=True, indent=4)
                click.echo(s)
            else:
                table = PrettyTable(["KEY", "VALUE"])
                table.align = "l"
                link = None
                for key, value in r.items():
                    if key != 'link':
                        table.add_row([key, value])
                    else:
                        link = value
                click.echo(table)
                click.echo('Link: ' + link)

            sys.exit(0)
            break
        except Conflict:
            time.sleep(10)
        except BadRequest as e:
            click.echo(e)
            break

    click.echo("Unable to compare log files")
    sys.exit(1)


@compare.command()
@click.pass_context
def ls(ctx):
    """
    compare indexed logs

    python -m src.logsight_cli compare ls --tags <tag_v1> <tag_v2>
    """
    u = ctx.obj['AUTHENTICATION']

    try:
        comp = LogsightCompare(u.token)
    except Exception as e:
        print(e)
        click.echo(f'Unable to authenticate user: {ctx.obj["AUTHENTICATION"]}')
        sys.exit(1)

    for _ in (
        td := tqdm(
            range(1, N_CALL_RETRIES + 1),
            desc="Call retries",
            colour="white",
            file=sys.stdout,
            disable=not ctx.obj["DEBUG"],
        )
    ):
        td.refresh()
        try:
            r = comp.ls_comparisons()

            if ctx.obj["JSON"]:
                s = json.dumps(r, sort_keys=True, indent=4)
                click.echo(s)
            else:
                table = PrettyTable(["KEY", "VALUE"])
                table.align = "l"
                link = None
                for key, value in r.items():
                    if key != 'link':
                        table.add_row([key, value])
                    else:
                        link = value
                click.echo(table)
                click.echo('Link: ' + link)

            sys.exit(0)
            break
        except Conflict:
            time.sleep(10)
        except BadRequest as e:
            click.echo(e)
            break

    click.echo("Unable to retrieve list of comparisons")
    sys.exit(1)

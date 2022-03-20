import sys
import json
import time
import datetime
import click
from tqdm import tqdm
from prettytable import PrettyTable

from logsight.incidents import LogsightIncident
from logsight.exceptions import Conflict

N_CALL_RETRIES = 10


@click.group()
@click.pass_context
def incident(ctx):
    """Analyzes log files for incidents"""


@incident.command()
@click.pass_context
@click.option("--app_id", help="id of the application")
@click.option(
    "--tag", required=True, type=str, help="tag used to select section of log"
)
@click.option("--flush_id", help="flush id")
def log(ctx, app_id, tag, flush_id):
    """
    Show the incidents that occurred in a log file

    python -m cli.ls-cli incident log --app_id <applicationId> --tag <tag_v1>
    """

    # todo(jcardoso): Tag is not being used. Currently using now() - 1 day
    #   it should be possible to use tags which are resolved to timestamps
    click.echo(
        f"Tag ({tag}) option is not being used."
        f"A default 365d window in being applied"
    )

    u = ctx.obj["USER"]
    a = app_id or ctx.obj["APP_ID"]

    i = LogsightIncident(u.user_id, u.token)
    now = datetime.datetime.utcnow()
    stop_time = now.isoformat()
    start_time = (now - datetime.timedelta(days=365)).isoformat()

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
            r = i.incidents(
                app_id=a,
                start_time=start_time,
                stop_time=stop_time,
                flush_id=flush_id,
                verbose=ctx.obj["DEBUG"],
            )

            if ctx.obj["JSON"]:
                s = json.dumps(r, sort_keys=True, indent=4)
                click.echo(s)
            else:
                table = PrettyTable(["KEY", "VALUE"])
                table.align = "l"
                for key, value in r.items():
                    table.add_row([key, value])
                click.echo(table)

            sys.exit(0)
        except Conflict:
            time.sleep(10)

    click.echo("Unable to retrieve incidents")
    sys.exit(1)

import click

from logsight_cli.utils.log_parser import parse_line


@click.group()
def utils():
    """Utilities for log transformation"""


@utils.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--output", required=True, default=" ", type=str,
              help="output file name")
@click.option("--date", required=True, type=click.Tuple([int, int]),
              help="indices of array with the date/time")
@click.option("--level", required=True, type=click.Tuple([int, int]),
              help="indices of array with log level")
@click.option("--message", required=True, type=int,
              help="index of array where message starts")
def transform(file, output, date, level, message):
    """
    transforms the structure of a log file

    FILE, the name of the log file to transform

    e.g.,
    python -m src.logsight_cli utils transform log_file.log \
    --output log_file_out.log --date 0 3 --level 3 3 --message 3
    """
    with open(file, "r", encoding="utf8") as read,\
            open(output, "w", encoding="utf8") as write:
        for line in read:
            data = parse_line(
                line,
                timestamp=lambda x: x[date[0]: date[1]],
                level=lambda x: x[level[0]: level[1]],
                message=lambda x: x[message:],
            )
            if data:
                write.write(
                    " ".join([data[i]
                              for i in ["timestamp", "level", "message"]])
                    + read.newlines
                )

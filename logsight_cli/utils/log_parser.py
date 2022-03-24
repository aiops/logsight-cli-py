import datetime
from dateutil import parser
from dateutil.tz import tzlocal


def create_log_record(level, message, timestamp=None, metadata=None):
    timestamp = timestamp or datetime.datetime.now(tz=tzlocal()).isoformat()
    return {
        "timestamp": timestamp,
        "level": level,
        "message": message,
        "metadata": metadata or "",
    }


def read_lines(file_name):
    with open(file_name, encoding="utf8") as f:
        lines = f.readlines()
        return lines


def autodetect_datetime(date):
    try:
        return parser.parse(date).replace(tzinfo=tzlocal()).isoformat()
    except parser.ParserError:
        return None


def parse_lines(lines, **kwargs):
    return [parse_line(line, **kwargs) for line in lines]


def parse_line(line, timestamp, level, message):
    sep = " "
    line_lst = line.split()

    d = {
        "timestamp": autodetect_datetime(sep.join(timestamp(line_lst))),
        "level": sep.join(level(line_lst)) or "INFO",
        "message": sep.join(message(line_lst)),
        "metadata": "",
    }

    if not d["timestamp"]:
        return None

    return create_log_record(**d)


def parse_file(file_name, **kwargs):
    lines = read_lines(file_name)
    return [i for i in parse_lines(lines, **kwargs) if i is not None]
    # return lines_to_struct(lines, **kwargs)


if __name__ == "__main__":

    # r = parse_file(file, sep=' ',
    #                timestamp=lambda x: x[1:3],
    #                level=lambda x: x[4:5],
    #                message=lambda x: x[6:])

    FILE = "hadoop_name_node_v2"
    r = parse_file(
        FILE,
        sep=" ",
        timestamp=lambda x: x[0:2],
        level=lambda x: x[2:3],
        message=lambda x: x[3:],
    )
    for i in r:
        print(i)
    print(len(r))

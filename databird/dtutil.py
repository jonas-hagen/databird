import datetime as dt


def parse_timedelta(s):

    valid_units = [
        "weeks",
        "days",
        "hours",
        "seconds",
        "minutes",
        "miliseconds",
        "microseconds",
    ]

    try:
        if s == "0":
            return dt.timedelta()
        value, unit = s.split(" ")
        if unit[-1] != "s":
            unit += "s"
        value = float(value)
        delta = dt.timedelta(**{unit: value})
        return delta
    except:
        raise ValueError(
            "Could not parse '{}'. Timedelta format is '<number> <unit> | 0', where `unit` is one of {} (tailing 's' is optional).".format(
                s, ", ".join(valid_units)
            )
        )


def parse_datetime(s):
    try:
        date = dt.datetime.strptime(s, "%Y-%m-%d")
    except:
        try:
            date = dt.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
        except:
            raise ValueError(
                "Could not parse '{}'. Time format is '%Y-%m-%d' or '%Y-%m-%d %H:%M:%S'.".format(
                    s
                )
            )
    return date

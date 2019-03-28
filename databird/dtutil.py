import datetime as dt
import calendar
import time


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


def iter_dates(start, end, period):
    """Yield dates from `start` to `end` with step equalt to `period`."""
    current = start
    while current <= end:
        yield current
        current += period


def month_last_day(date):
    """Return the last date of the month for the month containing date."""
    _, last_day = calendar.monthrange(date.year, date.month)
    return dt.datetime(date.year, date.month, last_day)


def month_first_day(date):
    """Return the first date of the month (always 01) for the month containing date."""
    return dt.datetime(date.year, date.month, 1)


def iso_date(date):
    return date.strftime("%Y-%m-%d")


def normalize_datetime(date):
    return dt.datetime.fromtimestamp(time.mktime(date.timetuple()))

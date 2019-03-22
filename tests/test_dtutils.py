from databird import dtutil
import datetime as dt
import pytest


@pytest.mark.parametrize(
    "text,expected",
    [
        ("0", dt.timedelta()),
        ("1 days", dt.timedelta(days=1)),
        ("1 day", dt.timedelta(days=1)),
        ("8 weeks", dt.timedelta(weeks=8)),
        ("6.5 hours", dt.timedelta(hours=6, minutes=30)),
    ],
)
def test_parse_timedelta(text, expected):
    value = dtutil.parse_timedelta(text)
    assert value == expected


@pytest.mark.parametrize(
    "text,expected",
    [
        ("2019-01-01", dt.datetime(2019, 1, 1)),
        ("2019-01-01 06:00:00", dt.datetime(2019, 1, 1, 6)),
    ],
)
def test_parse_datetime(text, expected):
    value = dtutil.parse_datetime(text)
    assert value == expected


def test_iter_dates():
    start = dt.datetime(2019, 1, 1)
    end = dt.datetime(2019, 1, 10)
    period = dt.timedelta(days=1)
    dates = list(dtutil.iter_dates(start, end, period))

    assert len(dates) == 10

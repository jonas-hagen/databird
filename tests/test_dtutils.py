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


@pytest.mark.parametrize(
    "date,last",
    [
        (dt.datetime(2019, 1, 20), dt.datetime(2019, 1, 31)),
        (dt.datetime(2019, 2, 20, 6), dt.datetime(2019, 2, 28)),
    ],
)
def test_last_day(date, last):
    assert last == dtutil.month_last_day(date)


def test_first_day():
    assert dt.datetime(2019, 1, 1) == dtutil.month_first_day(dt.datetime(2019, 1, 20))


def test_iso_date():
    assert "2019-01-20" == dtutil.iso_date(dt.datetime(2019, 1, 20))


@pytest.mark.parametrize(
    "value,expected",
    [
        (dt.datetime(2019, 1, 1, 12), dt.datetime(2019, 1, 1, 12)),
        (dt.date(2019, 1, 1), dt.datetime(2019, 1, 1)),
    ],
)
def test_normalize_datetime(value, expected):
    assert dtutil.normalize_datetime(value) == expected

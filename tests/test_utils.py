from databird import utils
import datetime as dt


def test_render_one():
    d = dict(foo="bar{x}")
    d2 = utils.render_dict(d, dict(x=5))
    assert "bar5" == d2["foo"]

def test_render_date():
    d = dict(foo="foo_{time:%Y-%m-%d}",bar="bar_{time:%Y%m%d}")
    c = dict(time=dt.datetime(2019, 1, 2))
    d2 = utils.render_dict(d, c)
    assert "foo_2019-01-02" == d2["foo"]
    assert "bar_20190102" == d2["bar"]

def test_render_nested():
    d = dict(foo="bar{x}", laber=dict(blubb="xyz{y}"))
    d2 = utils.render_dict(d, dict(x=5, y=100))
    assert "bar5" == d2["foo"]
    assert "xyz100" == d2["laber"]["blubb"]

from databird import utils


def test_render_one():
    d = dict(foo="bar{x}")
    d2 = utils.render_dict(d, dict(x=5))
    assert "bar5" == d2["foo"]


def test_render_nested():
    d = dict(foo="bar{x}", laber=dict(blubb="xyz{y}"))
    d2 = utils.render_dict(d, dict(x=5, y=100))
    assert "bar5" == d2["foo"]
    assert "xyz100" == d2["laber"]["blubb"]

from databird import Profile, Repository
from databird.drivers import FilesystemDriver
import datetime as dt


def test_profile():
    p = Profile("foo", FilesystemDriver, dict(root="/data/"))


def test_repository():
    p = Profile("foo", FilesystemDriver, dict(root="/data/"))
    r = Repository(
        "foo",
        period="1 days",
        start=dt.datetime.now() - dt.timedelta(days=10),
        profile=p,
        targets=["blubber_{time:%Y-%d-%m}.dat"],
        configuration=dict(pattern="simple_{date}.txt"),
    )

    missing = list(r.iter_missing("/something"))

    assert len(missing) == 10

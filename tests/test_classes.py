from databird import Profile, Repository
from databird.drivers import FilesystemDriver


def test_profile():
    p = Profile("foo", FilesystemDriver, dict(root="/data/"))


def test_repository():
    p = Profile("foo", FilesystemDriver, dict(root="/data/"))
    r = Repository(
        "foo",
        period="1 days",
        start="2019-01-01",
        profile=p,
        targets=[],
        configuration=dict(pattern="simple_{date}.txt"),
    )

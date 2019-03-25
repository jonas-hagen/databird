from databird import Profile, Repository
from databird import runner
from databird.drivers import FilesystemDriver
import datetime as dt
import glob
import pytest


def test_retrieve_missing(tmpdir):
    source_root = tmpdir.mkdir("source")
    repo_root = tmpdir.mkdir("repo")

    # Create new source files
    (source_root.join("simple_2019-03-01.txt")).open("w").close()
    (source_root.join("simple_2019-03-02.txt")).open("w").close()
    (source_root.join("simple_2019-03-03.txt")).open("w").close()
    (source_root.join("simple_2019-03-04.txt")).open("w").close()

    p = Profile("foo", FilesystemDriver, dict(root=str(source_root)))
    r = Repository(
        "foo",
        period="1 days",
        start=dt.datetime(2019, 2, 1),
        profile=p,
        targets=["empty_{time:%Y-%m-%d}.dat"],
        configuration=dict(pattern="simple_{time:%Y-%m-%d}.txt"),
    )

    unreached = runner.retrieve_missing(repo_root, [r], num_workers=0)
    assert len(list(glob.glob(str(repo_root.join("foo/*.dat"))))) == 4


def _test_repository():
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


def _test_filesystem(tmpdir):
    source_root = tmpdir.mkdir("source")
    repo_root = tmpdir.mkdir("repo")

    # Create new source file
    (source_root.join("simple_2019-03-01.txt")).open("w").close()

    profile_config = dict(root=source_root)
    repo_config = dict(pattern="simple_{date:%Y-%m-%d}.txt")
    fsd = filesystem.FilesystemDriver(profile_config, repo_config)

    context = dict(date=dt.date(2019, 3, 1))
    assert fsd.is_available(context)

    assert len(list(glob.glob(str(repo_root.join("*.txt"))))) == 0
    fsd.retrieve(context, repo_root.join("new_file.txt"))
    assert len(list(glob.glob(str(repo_root.join("*.txt"))))) == 1

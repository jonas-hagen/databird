from databird.drivers import filesystem
import datetime as dt


def test_filesystem_render():
    profile_config = dict(root="/data")
    repo_config = dict(pattern="simple_{date:%Y-%m-%d}.txt")
    fsd = filesystem.FilesystemDriver(profile_config, repo_config)

    context = dict(date=dt.date(2019, 3, 1))
    assert fsd.render_filename(context) == "simple_2019-03-01.txt"


def test_filesystem(tmp_path):
    source_root = tmp_path / "source"
    source_root.mkdir()
    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    # Create new source file
    (source_root / "simple_2019-03-01.txt").open("w").close()

    profile_config = dict(root=source_root)
    repo_config = dict(pattern="simple_{date:%Y-%m-%d}.txt")
    fsd = filesystem.FilesystemDriver(profile_config, repo_config)

    context = dict(date=dt.date(2019, 3, 1))
    assert fsd.is_available(context)

    assert len(list(repo_root.glob("*.txt"))) == 0
    fsd.retrieve(context, repo_root / "new_file.txt")
    assert len(list(repo_root.glob("*.txt"))) == 1

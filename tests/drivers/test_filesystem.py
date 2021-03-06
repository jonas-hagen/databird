from databird_drivers.standard import FilesystemDriver
import datetime as dt
import glob


def test_filesystem_render():
    config = dict(root="/data", patterns=dict(default="simple_{date:%Y-%m-%d}.txt"))
    fsd = FilesystemDriver(config)

    context = dict(date=dt.date(2019, 3, 1))
    assert fsd.render_filename(context, "default") == "simple_2019-03-01.txt"


def test_filesystem(tmpdir):
    source_root = tmpdir.mkdir("source")
    repo_root = tmpdir.mkdir("repo")

    # Create new source file
    (source_root.join("simple_2019-03-01.txt")).open("w").close()

    config = dict(root=source_root, patterns=dict(default="simple_{date:%Y-%m-%d}.txt"))
    fsd = FilesystemDriver(config)

    context = dict(date=dt.date(2019, 3, 1))
    assert fsd.is_available(context)

    assert len(list(glob.glob(str(repo_root.join("*.txt"))))) == 0
    fsd.retrieve(context, dict(default=repo_root.join("new_file.txt")))
    assert len(list(glob.glob(str(repo_root.join("*.txt"))))) == 1

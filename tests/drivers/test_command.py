from databird_drivers.standard import CommandDriver
import datetime as dt
import glob


def test_args_render():
    config = dict(
        command="cp",
        patterns=dict(default=["-v", "simple_{date:%Y-%m-%d}.txt", "{target_file}"]),
    )
    cd = CommandDriver(config)

    context = dict(date=dt.date(2019, 3, 1))
    assert cd._render_arguments(
        context, "file.x", "default"
    ) == "-v simple_2019-03-01.txt file.x".split(" ")


def test_command(tmpdir):
    source_root = tmpdir.mkdir("source")
    repo_root = tmpdir.mkdir("repo")

    # Create new source file
    (source_root.join("simple_2019-03-01.txt")).open("w").close()

    config = dict(
        command="cp",
        patterns=dict(
            default=[
                "-f",
                str(source_root.join("simple_{date:%Y-%m-%d}.txt")),
                "{target_file}",
            ]
        ),
    )
    dri = CommandDriver(config)

    context = dict(date=dt.date(2019, 3, 1))
    assert dri.is_available(context)

    assert len(list(glob.glob(str(repo_root.join("*.txt"))))) == 0
    dri.retrieve(context, dict(default=repo_root.join("new_file.txt")))
    assert len(list(glob.glob(str(repo_root.join("*.txt"))))) == 1

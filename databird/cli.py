import click
import functools
from databird.configuration import Settings


def with_settings():
    def inner_decorator(func):
        @click.option(
            "-c",
            "--config",
            type=click.Path(exists=True),
            default="/etc/databird/databird.conf",
            help="The configuration file.",
        )
        @click.option(
            "-n",
            "--num-workers",
            type=int,
            help="Number of concurrent workers, set to 0 for debugging",
        )
        @functools.wraps(func)
        def wrapper(config, num_workers, *args, **kwargs):
            settings = Settings(config)
            if num_workers is not None:
                settings["general"]["num_workers"] = num_workers
            return func(settings, *args, **kwargs)

        return wrapper

    return inner_decorator


@click.group()
def cli():
    """Keeps a local data repository up to date with different data sources."""
    pass


@cli.command()
@with_settings()
def retrieve(settings):
    """Retrieve missing files."""
    from databird import runner

    runner.retrieve_missing(
        settings["general"]["root"],
        settings["repositories"].values(),
        settings["general"].get("num_workers", 4),
    )

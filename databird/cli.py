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
        @functools.wraps(func)
        def wrapper(config, *args, **kwargs):
            settings = Settings(config)
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
        settings["general"]["root"], settings["repositories"].values()
    )

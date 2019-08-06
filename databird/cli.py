from databird.configuration import Settings
import click
import functools
import logging


def with_settings():
    def inner_decorator(func):
        @click.option(
            "-c",
            "--config",
            type=click.Path(exists=True),
            default="/etc/databird/databird.conf",
            help="The configuration file.",
        )
        @click.option("-v", "--verbose", count=True)
        @functools.wraps(func)
        def wrapper(config, verbose, *args, **kwargs):
            settings = Settings(config)
            settings["general"]["verbosity"] = verbose
            if verbose == 0:
                logging.basicConfig(level=logging.WARNING)
            elif verbose == 1:
                logging.basicConfig(level=logging.INFO)
            elif verbose >= 2:
                logging.basicConfig(level=logging.DEBUG)
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


@cli.command()
@click.argument("port", default=9180, required=False)
@click.argument("host", default="localhost", required=False)
def webmonitor(port, host):
    from databird import webmonitor

    webmonitor.run_server(host, port)

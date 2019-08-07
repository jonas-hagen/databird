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
    """Start the web monitor server."""
    from databird import webmonitor

    webmonitor.run_server(host, port)


@cli.command()
@click.option("--clean", is_flag=True, help="Remove failed jobs.")
def jobs(clean):
    """List all jobs in queues."""
    from redis import Redis
    from operator import itemgetter

    redis_conn = Redis(decode_responses=True)
    jobs = []
    attrs = ["status", "origin", "enqueued_at", "description"]
    for key in redis_conn.scan_iter("rq:job:db_*"):
        values = redis_conn.hmget(key, attrs)
        j = dict(zip(attrs, values))
        j["id"] = key.split(":")[-1]
        j["short_id"] = key.split(":")[-1][3:9]
        if j["status"] == "failed" and clean:
            redis_conn.delete(key)
        else:
            jobs.append(j)

    jobs = sorted(jobs, key=itemgetter("enqueued_at"))
    for j in jobs:
        print("{short_id} {origin:<10s} {status:<10s} {description}".format(**j))

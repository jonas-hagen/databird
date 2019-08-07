from collections import defaultdict
from databird import Repository
from databird import utils
from typing import List
import datetime as dt
import logging
from databird.queue import MultiQueue
from redis import Redis

logger = logging.getLogger("databird.runner")


def retrieve_missing(
    root_dir, repos: List[Repository], redis_conn=None, is_async=True, ref_time=None
):
    """Retrieve all targets that are missing from the repositories."""
    if redis_conn is None:
        redis_conn = Redis()
    queue = MultiQueue(redis_conn, is_async=is_async)

    if ref_time is None:
        ref_time = dt.datetime.now()
    logger.debug("ref time is " + str(ref_time))

    submitted_jobs = []
    for repo in repos:
        logger.debug("checking repo " + repo.name)
        for context, targets in repo.iter_missing(root_dir, ref_time):
            logger.debug(
                "missing {} targets for {}".format(len(targets), str(context["time"]))
            )
            driver_name = str(type(repo.driver).__name__)
            info = "Repo {} with {} for targets {} at {}".format(
                repo.name, driver_name, ", ".join(targets), str(context["time"])
            )

            job_id = "db_" + utils.hash_dict(targets)
            job = queue.submit_job(
                repo.queue,
                job_id,
                repo.driver.retrieve_safe,
                context,
                targets,
                description=info,
            )
            if job is not None:
                logger.info("Sumitted job " + job_id)
                submitted_jobs.append(job)
            else:
                status = queue.job_status(job_id)
                logger.info("Job {} already in queue: {}".format(job_id, str(status)))

    return submitted_jobs

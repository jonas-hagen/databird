from collections import defaultdict
from databird import Repository
from databird import utils
from redis import Redis
from rq import Queue
from typing import List
import datetime as dt
import logging

logger = logging.getLogger("databird.runner")

ONE_HOUR = 3600
ONE_DAY = 24 * ONE_HOUR

RESULT_TTL = 600
QUEUE_TTL = 24 * ONE_HOUR
JOB_TIMEOUT = 7 * ONE_DAY
FAILURE_TTL = 360 * ONE_DAY


def retrieve_missing(root_dir, repos: List[Repository], queue=None, ref_time=None):
    """Retrieve all targets that are missing from the repositories."""
    if queue is None:
        queue = Queue("databird", connection=Redis())
    redis_conn = queue.connection
    logger.info("Using queue " + str(queue.name))

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

            # To check if a job is already running, we pre-create the
            # redis hash entry that is created by rq by setting the
            # 'databird->1' hash table entry under 'rq:job:<id>'
            # The whole hash map is dropped after the TTL defined by rq.
            job_id = "db_" + utils.hash_dict(targets)
            rq_job = "rq:job:" + job_id
            if redis_conn.hsetnx(rq_job, "databird", 1):
                # we are the first ones
                job = queue.enqueue(
                    repo.driver.retrieve_safe,
                    context,
                    targets,
                    job_id=job_id,
                    description=info,
                    result_ttl=RESULT_TTL,
                    job_timeout=JOB_TIMEOUT,
                    ttl=QUEUE_TTL,
                    failure_ttl=FAILURE_TTL,
                )
                logger.info("Sumitted job " + job_id)
                submitted_jobs.append(job)
            else:
                try:
                    job = queue.fetch_job(job_id)
                    status = job.get_status()
                except:
                    status = "unknown"
                logger.info("Job {} already in queue: {}".format(job_id, str(status)))

    return submitted_jobs

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
        queue = Queue(connection=Redis())
    redis_conn = queue.connection

    if ref_time is None:
        ref_time = dt.datetime.now()

    submitted_jobs = []
    for repo in repos:
        for context, targets in repo.iter_missing(root_dir, ref_time):
            driver_name = str(type(repo.driver).__name__)
            info = driver_name + " for targets " + str(targets)

            # To check if a job is already running, we pre-create the
            # redis hash entry that is created by rq by setting the
            # 'databird->1' hash table entry under 'rq:job:<id>'
            # The whole hash map is dropped after the TTL defined by rq.
            job_id = "db_" + utils.hash_dict(targets)
            rq_job = "rq:job:" + job_id
            if redis_conn.hsetnx(rq_job, "databird", 1):
                # we are the first ones
                job = queue.enqueue(
                    repo.driver.retrieve,
                    context,
                    targets,
                    description=info,
                    result_ttl=RESULT_TTL,
                    job_timeout=JOB_TIMEOUT,
                    ttl=QUEUE_TTL,
                    failure_ttl=FAILURE_TTL,
                )
                logger.info("Sumitted job " + job_id)
                submitted_jobs.append(job)
            else:
                logger.debug(
                    "Job {} already in queue for targets: {}".format(
                        job_id, str(targets)
                    )
                )

    return submitted_jobs

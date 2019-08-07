from redis import Redis
from rq import Queue

RESERVE_KEY = "databird"

ONE_HOUR = 3600
ONE_DAY = 24 * ONE_HOUR

RESULT_TTL = 600
QUEUE_TTL = 24 * ONE_HOUR
JOB_TIMEOUT = 7 * ONE_DAY
FAILURE_TTL = ONE_DAY


class MultiQueue:
    def __init__(self, redis_conn=None, is_async=True):
        self._redis_conn = redis_conn or Redis()
        self._is_async = is_async
        self._ttl_defaults = dict(
            result_ttl=RESULT_TTL,
            job_timeout=JOB_TIMEOUT,
            ttl=QUEUE_TTL,
            failure_ttl=FAILURE_TTL,
        )

    def submit_job(self, queue_name, job_id, *args, **kwargs):
        """Add a task to the queue and  return False if job already exists."""
        q = Queue(queue_name, connection=self._redis_conn, is_async=self._is_async)
        if self._reserve_job_id(job_id):
            # we are the first ones
            rq_args = args
            rq_kwargs = self._ttl_defaults.copy()
            rq_kwargs.update(kwargs)
            rq_kwargs["job_id"] = job_id
            job = q.enqueue(*rq_args, **rq_kwargs)
            return job

    @staticmethod
    def _rq_key(job_id):
        return "rq:job:" + job_id

    def _reserve_job_id(self, job_id):
        # To check if a job is already running, we pre-create the
        # redis hash entry that is created by rq by setting the
        # 'databird->1' hash table entry under 'rq:job:<id>'
        # The whole hash map is dropped after the TTL defined by rq.
        return self._redis_conn.hsetnx(self._rq_key(job_id), RESERVE_KEY, 1)

    def job_status(self, job_id):
        try:
            status = self._redis_conn.hget(self._rq_key(job_id), "status").decode()
        except:
            status = "unknown"
        return status

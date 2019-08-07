from databird.queue import MultiQueue
import pytest


@pytest.fixture
def queue():
    from fakeredis import FakeStrictRedis

    redis_conn = FakeStrictRedis()
    return MultiQueue(redis_conn)


def test_reservation(queue):
    j1 = queue.submit_job("default", "abc123", print, "Hallo")
    assert j1 is not None
    j2 = queue.submit_job("default", "abc123", print, "Hallo")
    assert j2 is None
    assert queue.job_status("abc123") == "queued"


def test_status(queue):
    j1 = queue.submit_job("default", "abc123", print, "Hallo")
    assert queue.job_status("abc123") == "queued"

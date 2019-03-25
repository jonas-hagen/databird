from databird.queue import TaskQueue
from databird import Repository
from typing import List
import datetime as dt
from collections import defaultdict


def wrap(func):
    def inner(*args, **kwargs):
        try:
            r = func(*args, **kwargs)
        except Exception as e:
            return False
        return r

    return inner


def retrieve_missing(root_dir, repos: List[Repository], num_workers=4):
    """Retrieve all targets that are missing from the repositories."""

    queue = TaskQueue(num_workers)
    ref_time = dt.datetime.now()

    for repo in repos:
        for context, target in repo.iter_missing(root_dir, ref_time):
            if num_workers > 0:
                queue.add_task(wrap(repo.driver.retrieve), context, target)
            else:
                # Retrieve synchronously, for debugging
                wrap(repo.driver.retrieve)(context, target)

    queue.join()
    queue.stop_workers()

    # Check if all targets have been reached
    unreached = defaultdict(list)
    for repo in repos:
        for context, target in repo.iter_missing(root_dir, ref_time):
            unreached[repo].append((context, target))

    return unreached

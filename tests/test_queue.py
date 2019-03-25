from databird.queue import TaskQueue
import time


def test_task_queue():
    def relax(*args, **kwargs):
        time.sleep(0.2)

    q = TaskQueue(num_workers=5)
    for item in range(10):
        q.add_task(relax)
    q.join()
    q.stop_workers()

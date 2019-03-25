from threading import Thread
import queue


class TaskQueue(queue.Queue):
    """ A simple task queue with multiple threaded workers."""

    def __init__(self, num_workers=1):
        super().__init__()
        if num_workers < 0:
            raise ValueError("num_workers must be positive")
        self.num_workers = num_workers
        self.workers = []
        self.start_workers()

    def add_task(self, task, *args, **kwargs):
        """Add a task to the queue."""
        if task is not None:
            self.put((task, args, kwargs))

    def start_workers(self):
        """Spin up the workers."""
        for i in range(self.num_workers - len(self.workers)):
            t = Thread(target=self.worker)
            t.daemon = True
            self.workers.append(t)
            t.start()

    def stop_workers(self):
        """Stop the workers and join the threads."""
        self.join()
        for i in range(self.num_workers):
            # submitting None quits the worker
            self.put((None, None, None))
        for t in self.workers:
            t.join()
        self.workers = []

    def worker(self):
        while True:
            item, args, kwargs = self.get()
            if item is None:
                break
            item(*args, **kwargs)
            self.task_done()

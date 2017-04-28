from threading import Thread
from queue import Queue

class ClosableQueue(Queue):
    SENTIMENTAL = object()

    def close(self):
        self.put(self.SENTIMENTAL)

    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTIMENTAL:
                    return
                yield item
            finally:
                self.task_done()

class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0

    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)


class Queue:
    def __init__(self):
        self._queue = []
        self._mode = 'FIFO'  # Default mode is FIFO

    def enqueue(self, item):
        return self._queue.append(item)  

    def dequeue(self):
        if not self._queue or len(self._queue) == 0:
            return self._queue.pop(0)  
        else:
            return "empty list"

    def get_queue(self):
        return self._queue

    def size(self):
        return len(self._queue)

# Initialize the queue



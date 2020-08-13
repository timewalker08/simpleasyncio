
import random
from datetime import datetime, timedelta

from future import Future

ios = {}

class Event(object):
    def __init__(self, ioid, fut, delay):
        self.ioid = ioid
        self.fut = fut
        self.due_time = datetime.utcnow() + timedelta(seconds=delay)

def listen_io(ioid, fut):
    ios[ioid] = Event(ioid, fut, random.randint(1, 2))

def recv_io(ioid):
    return ioid + 10000

class Selector(object):
    def __init__(self):
        self.io_handle = {}

    def select(self):
        ready_ioids = []
        for ioid, event in ios.items():
            if event.due_time < datetime.utcnow():
                ready_ioids.append(ioid)

        ready = []
        for ioid in ready_ioids:
            event = ios.pop(ioid)
            handle = self.io_handle.get(ioid)
            ready.append((event, handle))

        return ready

    def register(self, ioid, handle):
        self.io_handle[ioid] = handle

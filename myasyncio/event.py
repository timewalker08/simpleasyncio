
from functools import partial

from future import Future
from selector import Selector, listen_io, recv_io
from task import Task


class Handle(object):
    def __init__(self, loop, callback):
        self.loop = loop
        self.callback = callback

    def run(self):
        self.callback()


class Eventloop(object):
    instance = None

    def __init__(self):
        self._ready = []
        self._selector = Selector()
        self._stopping = False

    @classmethod
    def get_current_loop(cls):
        if Eventloop.instance is None:
            Eventloop.instance = cls()
        return Eventloop.instance

    def call_soon(self, callback):
        self._ready.append(Handle(self, callback))

    def run_forever(self):
        while True:
            self.run_once()
            if self._stopping:
                break

    def run_once(self):
        event_list = self._selector.select()
        if event_list:
            for _, handle in event_list:
                handle.run()
        for handle in self._ready:
            handle.run()
        self._ready = []

    def run_until_complete(self, future):
        task = self.create_task(future)
        task.add_done_callback(self.stop)
        self.run_forever()

    def stop(self):
        self._stopping = True

    def create_future(self):
        return Future(loop=self)

    def create_task(self, coro):
        return Task(coro, self)

    async def listen_io(self, ioid):
        fut = self.create_future()
        self._selector.register(ioid, Handle(self, partial(self._recv_io, fut, ioid)))
        #fut.add_done_callback()
        listen_io(ioid, fut)
        return await fut

    def _recv_io(self, fut, ioid):
        res = recv_io(ioid)
        fut.set_result(res)

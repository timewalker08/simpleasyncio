

from future import Future

class Task(Future):
    def __init__(self, coro, loop):
        self._coro = coro
        super(Task, self).__init__(loop)
        loop.call_soon(self._step)

    def _step(self):
        try:
            result = self._coro.send(None)
        except StopIteration:
            pass
        else:
            result.add_done_callback(self._step)

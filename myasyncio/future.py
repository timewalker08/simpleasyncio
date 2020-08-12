
from exception import CancelledError, InvalidStateError


_PENDING = 'PENDING'
_CANCELLED = 'CANCELLED'
_FINISHED = 'FINISHED'


class Future(object):
    def __init__(self, loop):
        if loop is None:
            raise ValueError("loop should not be none.")

        self._loop = loop
        self._result = None
        self._status = _PENDING
        self._exception = None
        self._callbacks = []
        self._asyncio_future_blocking = False

    def result(self):
        if self._status == _CANCELLED:
            raise CancelledError()
        if self._status != _FINISHED:
            raise InvalidStateError('Result is not ready.')
        if self._exception is not None:
            raise self._exception
        return self._result

    def set_result(self, result):
        if self._status != _PENDING:
            raise InvalidStateError(f'{self._status}: {self!r}')
        self._result = result
        self._status = _FINISHED
        self.__schedule_callbacks()

    def add_done_callback(self, fn):
        if self._status != _PENDING:
            self._loop.call_soon(fn)
        else:
            self._callbacks.append(fn)

    def __schedule_callbacks(self):
        if self._callbacks:
            for callback in self._callbacks:
                self._loop.call_soon(callback)
        self._callbacks = []

    def done(self):
        return not self._status == _PENDING

    def __await__(self):
        if not self.done():
            self._asyncio_future_blocking = True
            print("future.__await__.1")
            yield self  # This tells Task to wait for completion.
        if not self.done():
            raise RuntimeError("await wasn't used with future")
        return self.result()  # May raise too.
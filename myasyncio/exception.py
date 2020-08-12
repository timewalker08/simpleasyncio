

class CancelledError(BaseException):
    """The Future or Task was cancelled."""

class InvalidStateError(Exception):
    """The operation is not allowed in this state."""
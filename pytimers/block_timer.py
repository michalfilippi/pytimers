from contextlib import AbstractContextManager
from timeit import default_timer


class BlockTimer(AbstractContextManager):

    def __init__(self):
        self._start_time = None
        self._end_time = None

    def __enter__(self):
        self._start_time = default_timer()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._end_time = default_timer()

    @property
    def time(self):
        return self._end_time - self._start_time

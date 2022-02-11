from timeit import default_timer
from typing import Optional

from pytimers.exceptions import UnfinishedTimer


class StartedClock:
    def __init__(self, label: Optional[str]):
        self.label = label
        self.start_time = default_timer()
        self._duration: Optional[float] = None

    def stop(self):
        self._duration = default_timer() - self.start_time

    @property
    def time(self) -> float:
        if self._duration is None:
            raise UnfinishedTimer()
        else:
            return self._duration

    @property
    def current_duration(self) -> float:
        return default_timer() - self.start_time

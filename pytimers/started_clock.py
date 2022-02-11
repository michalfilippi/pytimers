from timeit import default_timer
from typing import Optional

from pytimers.exceptions import UnfinishedTimer


class StartedClock:
    def __init__(self, label: Optional[str]):
        self.label = label
        self.start_time = default_timer()
        self._duration: Optional[float] = None

    def stop(self) -> None:
        """Stops the clock.
        """

        self._duration = default_timer() - self.start_time

    @property
    def time(self) -> float:
        """Exposes measured time of the clock.

        :return: Measured time in seconds between start and stop of the clock.
        :raise UnfinishedTimer: Clock has to be stopped before accessing elapsed time.
        """

        if self._duration is None:
            raise UnfinishedTimer("Clock has to be stopped before accessing elapsed time.")
        else:
            return self._duration

    @property
    def current_duration(self) -> float:
        """Calculates the duration elapsed since the clock started.

        :return: Duration in seconds elapsed since the clock start.
        """

        return default_timer() - self.start_time

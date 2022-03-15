from timeit import default_timer
from typing import Optional

from pytimers.exceptions import ClockStillRunning


class Clock:
    def __init__(self, label: Optional[str]):
        self.label = label
        self.start_time = default_timer()
        self._duration: Optional[float] = None

    def stop(self) -> None:
        """Stops the running clock."""

        self._duration = default_timer() - self.start_time

    def duration(self, precision: Optional[int] = None) -> float:
        """Exposes measured time of the clock. You can use this method to access the
        measured time even after the context manager is closed. This property should
        never be used directly inside a timed code block as it would raise an
        :py:exc:`pytimers.exceptions.ClockStillRunning` exception.

        :param precision: Number of decimal places of the returned time. If set to
            ``None`` the full precision is returned.
        :return: Measured time in seconds between start and stop of the clock.
        :raise pytimers.exceptions.ClockStillRunning: Clock has to be stopped before
            accessing elapsed time.
        """

        if self._duration is None:
            raise ClockStillRunning(
                "Clock has to be stopped before accessing elapsed time."
            )
        elif precision is None:
            return self._duration
        else:
            return round(self._duration, precision)

    def current_duration(self, precision: Optional[int] = None) -> float:
        """Calculates the current duration elapsed since the clock was started. This
        property can be used inside a timed code block.

        :param precision: Number of decimal places of the returned time. If set to
            ``None`` the full precision is returned.
        :return: Measured time in seconds between start of the clock and the method
            call.
        """

        if precision is None:
            return default_timer() - self.start_time
        else:
            return round(default_timer() - self.start_time, precision)

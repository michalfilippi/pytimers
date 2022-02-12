from typing import Optional

from pytimers.started_clock import StartedClock


class ClockHierarchy:
    def __init__(
        self,
        head: StartedClock,
        tail: Optional["ClockHierarchy"] = None,
    ):
        self.head = head
        self.tail: Optional["ClockHierarchy"] = tail

    def add(self, clock: StartedClock) -> "ClockHierarchy":
        return ClockHierarchy(clock, self)

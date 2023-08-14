import pytest

from pytimers.exceptions import TimerNotRunning
from pytimers.timer import Timer


def test_duration_raises_exception_before_clock_start() -> None:
    pt = Timer([], label=None)
    with pytest.raises(TimerNotRunning):
        pt.duration()


def test_exit_raises_exception_before_clock_start() -> None:
    pt = Timer([], label=None)
    with pytest.raises(TimerNotRunning):
        pt.__exit__(None, None, None)

import pytest

from pytimers.exceptions import ClockNotRunning
from pytimers.parametrized_timer import ParameterizedTimer


def test_duration_raises_exception_before_clock_start() -> None:
    pt = ParameterizedTimer([], label=None)
    with pytest.raises(ClockNotRunning):
        pt.duration()


def test_exit_raises_exception_before_clock_start() -> None:
    pt = ParameterizedTimer([], label=None)
    with pytest.raises(ClockNotRunning):
        pt.__exit__(None, None, None)

from __future__ import annotations

import inspect
from timeit import default_timer
from types import TracebackType
from typing import (
    Any,
    Awaitable,
    Callable,
    Iterable,
    Optional,
    Type,
    TypeVar,
)
from warnings import warn

from decorator import decorate  # type: ignore

from pytimers.exceptions import ClockNotRunning
from pytimers.triggers import BaseTrigger

ReturnT = TypeVar("ReturnT")


class ParameterizedTimer:
    def __init__(
        self,
        triggers: Iterable[BaseTrigger],
        label: Optional[str],
        **kwargs: Any,
    ) -> None:
        self.triggers = triggers
        self.label = label
        self.kwargs = kwargs
        self._start_time: Optional[float] = None
        self._duration: Optional[float] = None

    def __enter__(self) -> "ParameterizedTimer":
        self._start_time = default_timer()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        if self._start_time is None:
            raise ClockNotRunning
        else:
            self._duration = self.duration()
            self._finish_timing(
                self._duration,
                self.label,
                False,
            )

    def __call__(
        self,
        wrapped: Callable[..., ReturnT],
    ) -> Callable[..., ReturnT]:
        if inspect.iscoroutinefunction(wrapped):
            return decorate(wrapped, self._async_wrapper)  # type: ignore
        else:
            return decorate(wrapped, self._wrapper)  # type: ignore

    def _wrapper(
        self,
        wrapped: Callable[..., ReturnT],
        *args: Any,
        **kwargs: Any,
    ) -> ReturnT:
        start_time = default_timer()
        output = wrapped(*args, **kwargs)
        end_time = default_timer()
        self._finish_timing(
            end_time - start_time,
            self.label if self.label is None else wrapped.__qualname__,
            True,
        )
        return output

    async def _async_wrapper(
        self,
        wrapped: Callable[..., Awaitable[ReturnT]],
        *args: Any,
        **kwargs: Any,
    ) -> ReturnT:
        start_time = default_timer()
        output = await wrapped(*args, **kwargs)
        end_time = default_timer()
        self._finish_timing(
            end_time - start_time,
            self.label if self.label is None else wrapped.__qualname__,
            True,
        )
        return output

    def _finish_timing(
        self,
        duration: float,
        name: Optional[str],
        decorator: bool,
    ) -> None:
        for trigger in self.triggers:
            trigger(
                duration,
                decorator,
                name,
                **self.kwargs,
            )

    def duration(self, precision: Optional[int] = None) -> float:
        """Exposes measured time of the clock. You can use this method to access the
        measured time even after the context manager is closed. This property should
        never be used directly inside a timed code block as it would raise an
        :py:exc:`pytimers.exceptions.ClockNotRunning` exception.

        :param precision: Number of decimal places of the returned time. If set to
            ``None`` the full precision is returned.
        :return: Measured time in seconds between start and stop of the clock.
        :raise pytimers.exceptions.ClockNotRunning: Clock has to be stopped before
            accessing elapsed time.
        """

        if self._start_time is None:
            raise ClockNotRunning
        duration = (
            default_timer() - self._start_time
            if self._duration is None
            else self._duration
        )
        if precision is None:
            return duration
        else:
            return round(duration, precision)

    def current_duration(self, precision: Optional[int] = None) -> float:
        """Calculates the current duration elapsed since the clock was started. This
        property can be used inside a timed code block.

        :param precision: Number of decimal places of the returned time. If set to
            ``None`` the full precision is returned.
        :return: Measured time in seconds between start of the clock and the method
            call.

        .. deprecated:: 4.0
        """

        warn(
            message=(
                "The `current_duration` method will no longer be supported in future "
                "versions. Please use `duration` method instead."
            ),
            category=DeprecationWarning,
        )

        return self.duration(precision)

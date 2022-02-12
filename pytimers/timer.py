from __future__ import annotations

import inspect
from contextvars import ContextVar
from timeit import default_timer
from types import TracebackType
from typing import Any, Awaitable, Callable, Iterable, Optional, Type

from decorator import decorate  # type: ignore

from pytimers.clock_hierarchy import ClockHierarchy
from pytimers.started_clock import StartedClock
from pytimers.triggers import BaseTrigger


STARTED_CLOCK_VAR: ContextVar[Optional[ClockHierarchy]] = ContextVar(
    "started_clock",
    default=None,
)


class Timer:
    def __init__(
        self,
        triggers: Optional[
            Iterable[BaseTrigger | Callable[[float, bool, Optional[str]], Any]]
        ] = None,
    ):
        """Initializes Timer object with a set of triggers to be applied after the
        timer finishes.

        :param triggers: An iterable of callables to be called after the timer finishes.
            All triggers should accept keywords arguments duration_s: float,
            decorator: bool, label: str. PyTimers also provide an abstract class
            BaseTrigger to help with trigger interface implementation. See the
            BaseTrigger for more details. Any instance of BaseTrigger subclass is a
            valid trigger and can be passed to the triggers argument.
        """

        self._name: Optional[str] = None
        self.triggers = list(triggers) if triggers else []
        self._latest_time: Optional[float] = None

    def label(self, name: str) -> "Timer":
        """Sets label for the next timed code block. This label propagates to all
        triggers once the context managers is closed.

        :param name: Code block label name.
        :return: Returns self. This is comes makes possible to call the method directly
            inside context manager with statement.
        """

        self._name = name
        return self

    def __enter__(self) -> StartedClock:
        started_timer = StartedClock(label=self._name)
        clock_hierarchy = STARTED_CLOCK_VAR.get()
        if clock_hierarchy is None:
            STARTED_CLOCK_VAR.set(ClockHierarchy(started_timer))
        else:
            STARTED_CLOCK_VAR.set(clock_hierarchy.add(started_timer))

        if self._name:
            self._name = None

        return started_timer

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        clock_hierarchy = STARTED_CLOCK_VAR.get()
        if clock_hierarchy is not None:
            STARTED_CLOCK_VAR.set(clock_hierarchy.tail)
            clock_hierarchy.head.stop()
            self._finish_timing(
                clock_hierarchy.head.time,
                clock_hierarchy.head.label,
                False,
            )

    def _wrapper(
        self,
        wrapped: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        start_time = default_timer()
        output = wrapped(*args, **kwargs)
        end_time = default_timer()
        self._finish_timing(end_time - start_time, wrapped.__qualname__, True)
        return output

    async def _async_wrapper(
        self,
        wrapped: Callable[..., Awaitable[Any]],
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        start_time = default_timer()
        output = await wrapped(*args, **kwargs)
        end_time = default_timer()
        self._finish_timing(end_time - start_time, wrapped.__qualname__, True)
        return output

    def __call__(self, wrapped: Callable[..., Any]) -> Any:
        if inspect.iscoroutinefunction(wrapped):
            return decorate(wrapped, self._async_wrapper)
        else:
            return decorate(wrapped, self._wrapper)

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
            )

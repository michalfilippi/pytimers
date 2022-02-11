from __future__ import annotations

import inspect
from contextvars import ContextVar
from timeit import default_timer
from types import TracebackType
from typing import Any, Callable, Iterable, Optional, Type

from decorator import decorate  # type: ignore

from pytimers.started_clock import StartedClock
from pytimers.triggers import BaseTrigger


STARTED_CLOCK_VAR: ContextVar[Optional[list[StartedClock]]] = ContextVar(
    "started_clock", default=None
)


class Timer:
    def __init__(
        self,
        triggers: Iterable[
            BaseTrigger | Callable[[float, bool, Optional[str]], Any]
        ] = None,
    ):
        """Initializes Timer object with custom configuration parameters.

        :param triggers: A list of callables to be called after the timing finishes.
            All triggers should accept keywords arguments duration: float, name: str,
            code_block: bool.
        """

        self._name: Optional[str] = None
        self.triggers = triggers if triggers else []
        self._latest_time: Optional[float] = None

    def label(self, name: str) -> "Timer":
        """Sets name for the next timed code block. If there's no name set for code
        blocks the log message will use general "code block" as a name for timed block.

        :param name: Code block name.
        :return: Returns self.
        """

        self._name = name
        return self

    def __enter__(self) -> StartedClock:
        started_timer = StartedClock(label=self._name)
        started_clocks = STARTED_CLOCK_VAR.get()
        if started_clocks is None:
            STARTED_CLOCK_VAR.set([started_timer])
        else:
            started_clocks.append(started_timer)

        if self._name:
            self._name = None

        return started_timer

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        started_clocks = STARTED_CLOCK_VAR.get()
        if started_clocks is not None:
            started_timer = started_clocks.pop()
            started_timer.stop()
            self._finish_timing(started_timer.time, started_timer.label, False)

    def _wrapper(self, wrapped, *args, **kwargs):
        start_time = default_timer()
        output = wrapped(*args, **kwargs)
        end_time = default_timer()
        self._finish_timing(end_time - start_time, wrapped.__qualname__, True)
        return output

    async def _async_wrapper(self, wrapped, *args, **kwargs):
        start_time = default_timer()
        output = await wrapped(*args, **kwargs)
        end_time = default_timer()
        self._finish_timing(end_time - start_time, wrapped.__qualname__, True)
        return output

    def __call__(self, wrapped):
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

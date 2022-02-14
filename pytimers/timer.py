from __future__ import annotations

import inspect
from contextvars import ContextVar
from timeit import default_timer
from types import TracebackType
from typing import Any, Awaitable, Callable, Iterable, Optional, Type

from decorator import decorate  # type: ignore

from pytimers.immutable_stack import ImmutableStack
from pytimers.started_clock import StartedClock
from pytimers.triggers import BaseTrigger


STARTED_CLOCK_VAR: ContextVar[ImmutableStack[StartedClock]] = ContextVar(
    "started_clock",
    default=ImmutableStack.create_empty(),
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

    def label(self, name: str) -> Timer:
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
        clock_stack = STARTED_CLOCK_VAR.get()
        STARTED_CLOCK_VAR.set(clock_stack.push(started_timer))

        if self._name:
            self._name = None

        return started_timer

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        clock_stack = STARTED_CLOCK_VAR.get()
        started_clock, new_clock_stack = clock_stack.pop()
        STARTED_CLOCK_VAR.set(new_clock_stack)
        started_clock.stop()
        self._finish_timing(
            started_clock.time,
            started_clock.label,
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

from __future__ import annotations

import inspect
from contextvars import ContextVar
from timeit import default_timer
from types import TracebackType
from typing import Any, Awaitable, Callable, Iterable, Optional, Type
from warnings import warn

from decorator import decorate  # type: ignore

from pytimers.clock import Clock
from pytimers.immutable_stack import ImmutableStack
from pytimers.triggers import BaseTrigger


STARTED_CLOCK_VAR: ContextVar[ImmutableStack[Clock]] = ContextVar(
    "clock",
    default=ImmutableStack.create_empty(),
)


class Timer:
    """Initializes Timer object with a set of triggers to be applied after the
    timer finishes.

    :param triggers: An iterable of callables to be called after the timer finishes.
        All triggers should accept keywords arguments ``duration_s: float,
        decorator: bool, label: str``. PyTimers also provide an abstract class
        :py:class:`BaseTrigger` to help with trigger interface implementation. See the
        :py:class:`BaseTrigger` for more details. Any instance of
        :py:class:`BaseTrigger` subclass is a valid trigger and can be passed to the
        argument ``triggers``.
    """

    def __init__(
        self,
        triggers: Optional[
            Iterable[BaseTrigger | Callable[[float, bool, Optional[str]], Any]]
        ] = None,
    ):
        self._label_text: Optional[str] = None
        self.triggers = list(triggers) if triggers else []
        self._latest_time: Optional[float] = None

    def label(self, text: str) -> Timer:
        """Sets label for the next timed code block. This label propagates to all
        triggers once the context managers is closed.

        :param text: Code block label text.
        :return: Returns ``self``. This makes possible to call the method directly
            inside context manager with statement.
        """

        self._label_text = text
        return self

    def named(self, name: str) -> Timer:
        """This method only ensures backwards compatibility. Use
        :py:meth:`pytimers.Timer.label` instead.

        .. deprecated:: 3.0
        """

        warn(
            message=(
                "The `named` method will no longer be supported in future versions. "
                "Please use `label` method instead."
            ),
            category=DeprecationWarning,
        )
        return self.label(name)

    def __enter__(self) -> Clock:
        started_timer = Clock(label=self._label_text)
        clock_stack = STARTED_CLOCK_VAR.get()
        STARTED_CLOCK_VAR.set(clock_stack.push(started_timer))

        if self._label_text:
            self._label_text = None

        return started_timer

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        clock_stack = STARTED_CLOCK_VAR.get()
        clock, new_clock_stack = clock_stack.pop()
        STARTED_CLOCK_VAR.set(new_clock_stack)
        clock.stop()
        self._finish_timing(
            clock.duration(),
            clock.label,
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

from __future__ import annotations

import inspect
from timeit import default_timer
from types import TracebackType
from typing import (
    Any,
    Awaitable,
    Callable,
    Collection,
    Optional,
    Type,
    TypeVar,
)
from warnings import warn

from decorator import decorate  # type: ignore

from pytimers.exceptions import TimerNotRunning
from pytimers.triggers import BaseTrigger

ReturnT = TypeVar("ReturnT")


class Timer:
    """Class represents

    It is not recommended to use this class directly. TimerFactory should be used instead to allow reuse

    The Timer instance can be used in two different ways, as a decorator and a context manager.


    .. highlight:: python
    .. code-block:: python

        from time import sleep

        from pytimers import Timer
        from pytimers import PrinterTrigger

        with Timer([PrinterTrigger()]):
            sleep(1)


    .. code-block:: none

        Finished code block in 1s 1.147ms [1.001s].

    Decorator usage

    .. highlight:: python
    .. code-block:: python

        from time import sleep

        from pytimers import Timer
        from pytimers import PrinterTrigger

        @Timer([PrinterTrigger()])
        def func() -> None:
            sleep(1)

        func()


    .. code-block:: none

        Finished func in 1s 1.103ms [1.001s].

    """

    def __init__(
        self,
        triggers: Collection[BaseTrigger],
        label: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Inits Timer object with a collection of triggers to be executed at the end of the time measurement.

        :param triggers: A collection of :py:class:`BaseTrigger` to be executed at the end of the time measurement.
        :param label: String label to override callable name in the decorator usage or a label
        :param kwargs: Additional arguments, these will all be passed to each trigger execution and can serve as more fine grained trigger configuration.
        """

        self._triggers = triggers
        self.label = label
        self.kwargs = kwargs
        self._start_time: Optional[float] = None
        self._duration: Optional[float] = None

    def __enter__(self) -> "Timer":
        self._start_time = default_timer()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        if self._start_time is None:
            raise TimerNotRunning
        else:
            self._duration = self.duration()
            self._execute_triggers(
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
        self._execute_triggers(
            end_time - start_time,
            self.label if self.label is not None else wrapped.__qualname__,
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
        self._execute_triggers(
            end_time - start_time,
            self.label if self.label is not None else wrapped.__qualname__,
            True,
        )
        return output

    def _execute_triggers(
        self,
        duration: float,
        name: Optional[str],
        decorator: bool,
    ) -> None:
        for trigger in self._triggers:
            trigger(
                duration,
                decorator,
                name,
                **self.kwargs,
            )

    def duration(self, precision: Optional[int] = None) -> float:
        """Exposes measured time of the timer. You can use this method to access the
        measured time both inside the context manager and also after the context
        manager is closed. Calling this method before the context manager is entered
        will raise a :py:exc:`pytimers.exceptions.TimerNotRunning` exception.

        .. highlight:: python
        .. code-block:: python

            from time import sleep

            from pytimers import Timer
            from pytimers import PrinterTrigger

            with Timer([PrinterTrigger()]) as t:
                sleep(0.5)
                print(f"We are half way there. Elapsed time is {t.duration(4)}s.")
                sleep(0.5)
            print(f"Timer still exists, so we can access the measured time. It was {t.duration(4)}s.")

        .. code-block:: none

            We are half way there. Elapsed time is 0.5006s.
            Finished code block in 1s 1.425ms [1.001s].
            Timer still exists, so we can access the measured time. It was 1.0014s.

        :param precision: Number of decimal places of the returned time. If set to
            ``None`` the full precision is returned.
        :return: Measured time in seconds since the timer start and present time or
            timer end, depending on which of these happened first.
        :raise pytimers.exceptions.TimerNotRunning: Timer has to be started before
            accessing elapsed time. This can happen when calling this method before
            entering the context manager.
        """

        if self._start_time is None:
            raise TimerNotRunning
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
        """Alias to :py:meth:`pytimers.Timer.duration`. Take a look there for more
        details. This method exists only for a backward compatibility and will be
        removed in future versions.

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

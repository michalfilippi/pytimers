from __future__ import annotations

import inspect
from timeit import default_timer
from typing import Iterable, Optional

from decorator import decorate  # type: ignore

from pytimers.triggers import BaseTrigger


class Timer:
    def __init__(
        self,
        triggers: Iterable[BaseTrigger] = None,
    ):
        """Initializes Timer object with custom configuration parameters.

        :param triggers: A list of callables to be called after the timing finishes.
            All triggers should accept keywords arguments duration: float, name: str,
            code_block: bool.
        """

        self._start_times: list[float] = []
        self._name: Optional[str] = None
        self._names: list[str] = []
        self.triggers = triggers if triggers else []
        self.time: Optional[float] = None

    def label(self, name: str) -> "Timer":
        """Sets name for the next timed code block. If there's no name set for code
        blocks the log message will use general "code block" as a name for timed block.

        :param name: Code block name.
        :return: Returns self.
        """

        self._name = name
        return self

    def __enter__(self):
        self._start_times.append(default_timer())
        self._names.append(self._name)
        if self._name:
            self._name = None
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = default_timer()
        start_time = self._start_times.pop()
        label = self._names.pop()
        self._finish_timing(end_time - start_time, label, False)

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
        name: str,
        decorator: bool,
    ) -> None:
        self.time = duration
        for trigger in self.triggers:
            trigger(
                duration_s=duration,
                label=name,
                decorator=decorator,
            )


timer = Timer()

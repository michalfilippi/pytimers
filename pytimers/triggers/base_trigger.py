from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional


class BaseTrigger(ABC):
    """This class provides timer trigger abstraction. Custom triggers can be
    implemented using simple functions but subclassing this abstract class is the
    preferred way. Any custom implementation has to override
    :py:meth:`pytimers.BaseTrigger.__call__` method where the trigger logic
    should be provided.
    """

    @abstractmethod
    def __call__(
        self,
        duration_s: float,
        decorator: bool,
        label: Optional[str] = None,
    ) -> None:
        """This is a trigger action entrypoint. This method is called in
        :py:class:`pytimers.Timer` once the timer stops.

        :param duration_s: The measured duration in seconds.
        :param decorator: True if the timer was used as a decorator for callable.
            False if used as a context manager for timing code blocks.
        :param label: The label of the measured code block provided by client before
            entering the context manager. For decorator usage this value is set to the
            callable name.
        """
        pass

    @staticmethod
    def humanized_duration(duration_s: float, precision: int = 0) -> str:
        """This method provides formatter for human-readable duration with hours being
        the highest level of the format.

        :param duration_s: The duration in seconds to be formatted.
        :param precision: Number of decimal places for milliseconds.
        :return: Human-readable duration as a string.
        """

        hours, remainder = divmod(duration_s, 60 * 60)
        minutes, remainder = divmod(remainder, 60)
        seconds, remainder = divmod(remainder, 1)
        ms = remainder * 1000

        if hours > 0:
            return f"{hours:.0f}h {minutes:.0f}m {seconds:.0f}s {ms:.{precision}f}ms"
        elif minutes > 0:
            return f"{minutes:.0f}m {seconds:.0f}s {ms:.{precision}f}ms"
        elif seconds > 0:
            return f"{seconds:.0f}s {ms:.{precision}f}ms"
        else:
            return f"{ms:.{precision}f}ms"

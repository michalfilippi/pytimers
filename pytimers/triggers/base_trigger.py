from __future__ import annotations

from abc import ABC, abstractmethod


class BaseTrigger(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def __call__(
        self,
        duration_s: float,
        decorator: bool,
        label: str = None,
    ) -> None:
        pass

    @staticmethod
    def humanized_duration(duration_s: float, precision: int = 0) -> str:
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

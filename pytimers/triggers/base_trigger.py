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

from __future__ import annotations

from typing import Optional

from pytimers.triggers.base_trigger import BaseTrigger


class DummyTrigger(BaseTrigger):
    def __init__(self) -> None:
        super().__init__()
        self.calls: list[tuple[float, bool, Optional[str]]] = []

    def __call__(
        self,
        duration_s: float,
        decorator: bool,
        label: Optional[str] = None,
    ) -> None:
        self.calls.append((duration_s, decorator, label))

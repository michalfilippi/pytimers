from __future__ import annotations

from pytimers.triggers.base_trigger import BaseTrigger


class DummyTrigger(BaseTrigger):
    def __init__(self):
        super().__init__()
        self.calls: list[tuple] = []

    def __call__(
            self,
            duration_s: float,
            decorator: bool,
            label: str = None,
    ) -> None:
        self.calls.append((duration_s, decorator, label))

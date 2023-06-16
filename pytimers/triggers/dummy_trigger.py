from __future__ import annotations

from typing import Any, Dict, Optional

from pytimers.triggers.base_trigger import BaseTrigger


class DummyTrigger(BaseTrigger):
    """This is a trigger implementation used for debugging and unit testing.
    There's no real usage for this.
    """

    def __init__(self) -> None:
        super().__init__()
        self.calls: list[Dict[str, Any]] = []

    def __call__(
        self,
        duration_s: float,
        decorator: bool,
        label: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.calls.append(
            (
                {
                    "duration_s": duration_s,
                    "decorator": decorator,
                    "label": label,
                    "kwargs": kwargs,
                }
            )
        )

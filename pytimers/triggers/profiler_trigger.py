from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterator, Optional

from pytimers.triggers.base_trigger import BaseTrigger


@dataclass
class ProfilerItem:
    total: float = 0
    counter: int = 0
    nested: Dict[str, "ProfilerItem"] = field(default_factory=dict)

    def add(self, keys: Iterator[str], value: float) -> None:
        self.total += value
        self.counter += 1
        try:
            key = next(keys)
        except StopIteration:
            return

        if key not in self.nested:
            self.nested[key] = ProfilerItem()
        return self.nested[key].add(keys, value)

    def to_json(self) -> dict:  # type: ignore
        return self._to_json([])

    def _to_json(self, prefixes: list[str]) -> dict:  # type: ignore
        return {
            "full_name": ".".join(prefixes),
            "total": self.total,
            "calls": self.counter,
            "children": [
                profiler_item._to_json(prefixes + [key])
                for key, profiler_item in self.nested.items()
            ],
        }


class ProfilerTrigger(BaseTrigger):
    def __init__(self, require: bool = True) -> None:
        super().__init__()
        self._require = require
        self.data = ProfilerItem()

    def __call__(
        self,
        duration_s: float,
        decorator: bool,
        label: Optional[str] = None,
        profiler_part: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        if profiler_part is not None:
            self.data.add(iter(profiler_part.split(".")), duration_s)

    def reset(self) -> None:
        self.data = ProfilerItem()

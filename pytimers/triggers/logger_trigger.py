from __future__ import annotations
import logging
from string import Template

from pytimers.triggers.base_trigger import BaseTrigger


class LoggerTrigger(BaseTrigger):
    def __init__(
        self,
        level: int = logging.INFO,
        template: str = "Finished ${label} in ${duration}s.",
    ):
        super().__init__()
        self.level = level
        self.logger = logging.getLogger(__name__)
        self.template = Template(template)

    def __call__(
        self,
        duration_s: float,
        decorator: bool,
        label: str = None,
    ) -> None:
        self.logger.log(
            level=self.level,
            msg=self.template.substitute(
                duration=duration_s,
                label=label,
            ),
        )

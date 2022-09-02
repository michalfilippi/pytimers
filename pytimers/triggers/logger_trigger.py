from __future__ import annotations

import logging
from string import Template
from typing import Optional

from pytimers.triggers.base_trigger import BaseTrigger


class LoggerTrigger(BaseTrigger):
    """Provided trigger class for logging the measured duration using std logging
    library.

    :param level: Log level (as understood by the standard logging library
        :py:mod:`logging`) used for the message.
    :param template: Message `template string
        <https://docs.python.org/3/library/string.html#template-strings>`_
        containing placeholders for label, duration and/or humanized_duration.
    :param precision: Number of decimal places for the message duration in seconds.
    :param humanized_precision: Number of decimal places for milliseconds in
        human-readable duration in the message.
    :param default_code_block_label: Label used for code blocks with missing label.
    """

    def __init__(
        self,
        level: int = logging.INFO,
        template: str = "Finished ${label} in ${humanized_duration} [${duration}s].",
        precision: int = 3,
        humanized_precision: int = 3,
        default_code_block_label: str = "code block",
    ):
        super().__init__()
        self.level = level
        self.logger = logging.getLogger(__name__)
        self.template = Template(template)
        self.precision = precision
        self.humanized_precision = humanized_precision
        self.default_code_block_label = default_code_block_label

    def __call__(
        self,
        duration_s: float,
        decorator: bool,
        label: Optional[str] = None,
    ) -> None:
        if label is None and decorator is False:
            label = self.default_code_block_label
        self.logger.log(
            level=self.level,
            msg=self.template.substitute(
                duration=round(duration_s, self.precision),
                humanized_duration=self.humanized_duration(
                    duration_s=duration_s,
                    precision=self.humanized_precision,
                ),
                label=label,
            ),
        )

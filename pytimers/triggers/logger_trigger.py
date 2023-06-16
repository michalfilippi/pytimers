from __future__ import annotations

import logging
from string import Template
from typing import Any, Optional, Union

from pytimers.triggers.base_trigger import BaseTrigger


class LoggerTrigger(BaseTrigger):
    """Provided trigger class for logging the measured duration using std logging
    library.

    :param default_log_level: Log level (as understood by the standard logging library
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
        default_log_level: int = logging.INFO,
        logger: logging.Logger = logging.getLogger(__name__),
        template: str = "Finished ${label} in ${humanized_duration} [${duration}s].",
        precision: int = 3,
        humanized_precision: int = 3,
        default_code_block_label: str = "code block",
    ):
        super().__init__()
        self.default_log_level = default_log_level
        self.logger = logger
        self.template = Template(template)
        self.precision = precision
        self.humanized_precision = humanized_precision
        self.default_code_block_label = default_code_block_label

    def __call__(
        self,
        duration_s: float,
        decorator: bool,
        label: Optional[str] = None,
        log_level: Optional[Union[int, str]] = None,
        **kwargs: Any,
    ) -> None:
        if log_level is None:
            level = self.default_log_level
        elif isinstance(log_level, str):
            level = logging.getLevelName(log_level)
        else:
            level = log_level
        if label is None and decorator is False:
            label = self.default_code_block_label

        self.logger.log(
            level,
            msg=self.template.substitute(
                duration=round(duration_s, self.precision),
                humanized_duration=self.humanized_duration(
                    duration_s=duration_s,
                    precision=self.humanized_precision,
                ),
                label=label,
            ),
        )

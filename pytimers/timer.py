from timeit import default_timer
import inspect
from typing import Optional, List
from string import Template
import logging


import wrapt  # type: ignore


class Timer:
    def __init__(
        self,
        log_template: Optional[str] = None,
        log_level: int = logging.INFO,
    ):
        """Initializes Timer object with custom configuration parameters.

        :param log_template: String template to be used to format log message. The
            template is used in String.Template object. There are two placeholders
            allowed ${name} and ${duration}. These will be replaced during actual
            logging for timed instance name and time duration respectively.
        :param log_level: Logging level as understood by standard logging library.
        """

        self._start_times: List[float] = []
        self._name: Optional[str] = None
        self._names: List[str] = []
        self.message_template = Template(
            log_template if log_template else "Finished ${name} in ${duration}s."
        )
        self.logger = logging.getLogger(__name__)
        self.log_level = log_level

    def named(self, name: str) -> "Timer":
        """Sets name for the current timer. This method should be used to name code
        block for timing. The name of the block is later used for logging.

        :param name: Timer name.
        :return: Returns self.
        """

        self._name = name
        return self

    def __enter__(self):
        self._start_times.append(default_timer())
        self._names.append(self._name)
        if self._name:
            self._name = None
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = default_timer()
        start_time = self._start_times.pop()
        label = self._names.pop()
        if label is None:
            label = "code block"
        self._log_message(end_time - start_time, label)

    @wrapt.decorator
    def __call__(self, wrapped, instance, args, kwargs):
        if instance is None:
            if inspect.isclass(wrapped):
                # Decorator was applied to a class.
                callable_type = "class "
            else:
                # Decorator was applied to a function or static method.
                callable_type = "function "
        else:
            if inspect.isclass(instance):
                # Decorator was applied to a class method.
                callable_type = f"class method {type(instance).__name__}."
            else:
                # Decorator was applied to an instance method.
                callable_type = f"method {type(instance).__name__}."
        start_time = default_timer()
        output = wrapped(*args, **kwargs)
        end_time = default_timer()
        self._log_message(end_time - start_time, f"{callable_type}{wrapped.__name__}")
        return output

    def _log_message(self, duration: float, name: str):
        self.logger.log(
            self.log_level,
            self.message_template.substitute(
                duration=duration,
                name=name,
            ),
        )

    def __repr__(self) -> str:
        return f"Timer({self.message_template.template}, {self.log_level})"


timer = Timer()

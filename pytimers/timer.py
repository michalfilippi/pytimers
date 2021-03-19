from timeit import default_timer
import inspect
from typing import Optional, List, Callable
from string import Template
import logging


from decorator import decorate  # type: ignore


class Timer:
    def __init__(
        self,
        log_template: Optional[str] = None,
        log_level: int = logging.INFO,
        triggers: List[Callable] = None,
    ):
        """Initializes Timer object with custom configuration parameters.

        :param log_template: String template to be used to format log message. The
            template is used in String.Template object. There are two placeholders
            allowed ${name} and ${duration}. These will be replaced during actual
            logging for timed instance name and time duration respectively.
        :param log_level: Logging level as understood by standard logging library.
        :param triggers: A list of callables to be called after the timing finishes.
            The timer passes keywords arguments duration: float, name: str, code_block:
            bool.
        """

        self._start_times: List[float] = []
        self._name: Optional[str] = None
        self._names: List[str] = []
        self.message_template = Template(
            log_template if log_template else "Finished ${name} in ${duration}s."
        )
        self.logger = logging.getLogger(__name__)
        self.log_level = log_level
        self.triggers = triggers if triggers else []

        self.triggers.append(
            lambda name, duration: self.logger.log(
                self.log_level,
                self.message_template.substitute(
                    duration=duration,
                    name=name,
                ),
            )
        )

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
        self._finish_timing(end_time - start_time, label, True)

    def _wrapper(self, wrapped, *args, **kwargs):
        start_time = default_timer()
        output = wrapped(*args, **kwargs)
        end_time = default_timer()
        self._finish_timing(end_time - start_time, wrapped.__qualname__, False)
        return output

    async def _async_wrapper(self, wrapped, *args, **kwargs):
        start_time = default_timer()
        output = await wrapped(*args, **kwargs)
        end_time = default_timer()
        self._finish_timing(end_time - start_time, wrapped.__qualname__, False)
        return output

    def __call__(self, wrapped):
        if inspect.iscoroutinefunction(wrapped):
            return decorate(wrapped, self._async_wrapper)
        else:
            return decorate(wrapped, self._wrapper)

    def _finish_timing(self, duration: float, name: str, code_block: bool):
        for trigger in self.triggers:
            trigger(
                duration=duration,
                name=name,
                code_block=code_block,
            )

    def __repr__(self) -> str:
        return f"Timer({self.message_template.template}, {self.log_level})"


timer = Timer()

from timeit import default_timer
import inspect
from typing import Optional
from string import Template
import logging


import wrapt


class Timer:
    def __init__(
        self,
        log_template: Optional[str] = None,
        log_level: Optional[int] = logging.INFO,
    ):
        self._start_times = []
        self._name = None
        self._names = []
        self.message_template = Template(
            log_template if log_template else "Finished ${name} in ${duration}s."
        )
        self.logger = logging.getLogger(__name__)
        self.log_level = log_level

    def name(self, name: str):
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
        self.log_message(end_time - start_time, label)

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
        self.log_message(end_time - start_time, f"{callable_type}{wrapped.__name__}")
        return output

    def log_message(self, duration: float, name: str):
        self.logger.log(
            self.log_level,
            self.message_template.substitute(
                duration=duration,
                name=name,
            ),
        )


# @wrapt.decorator
# def timer(wrapped, instance, args, kwargs):
#     return wrapped(*args, **kwargs)

timer = Timer()

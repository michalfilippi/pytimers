from .timer import Timer
from .triggers.base_trigger import BaseTrigger
from .triggers.logger_trigger import LoggerTrigger

# provide default instance for the simplicity containing logger Trigger
timer = Timer(
    triggers=[
        LoggerTrigger(),
    ]
)


__all__ = [
    "Timer",
    "timer",
    "BaseTrigger",
    "LoggerTrigger",
]

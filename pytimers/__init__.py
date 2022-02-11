from .timer import Timer
from .triggers.base_trigger import BaseTrigger
from .triggers.logger_trigger import LoggerTrigger

__all__ = [
    "Timer",
    "BaseTrigger",
    "LoggerTrigger",
]

# provide default instance for the simplicity
timer = Timer(
    triggers=[
        LoggerTrigger(),
    ]
)

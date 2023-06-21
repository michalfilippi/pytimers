from .timer_factory import TimerFactory
from .triggers.base_trigger import BaseTrigger
from .triggers.logger_trigger import LoggerTrigger

# provide default Timer instance containing logger Trigger
timer = TimerFactory(
    triggers=[
        LoggerTrigger(),
    ]
)


__all__ = [
    "TimerFactory",
    "timer",
    "BaseTrigger",
    "LoggerTrigger",
]

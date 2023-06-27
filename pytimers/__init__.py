from pytimers.timer import Timer
from pytimers.timer_factory import TimerFactory
from pytimers.triggers.base_trigger import BaseTrigger
from pytimers.triggers.logger_trigger import LoggerTrigger
from pytimers.triggers.printer_trigger import PrinterTrigger
from pytimers.triggers.profiler_trigger import ProfilerTrigger
from pytimers.exceptions import TimerNotRunning

# provide default Timer instance containing logger Trigger
timer = TimerFactory(
    triggers=[
        LoggerTrigger(),
    ]
)


__all__ = [
    "Timer",
    "TimerFactory",
    "timer",
    "BaseTrigger",
    "LoggerTrigger",
    "ProfilerTrigger",
    "PrinterTrigger",
    "TimerNotRunning",
]

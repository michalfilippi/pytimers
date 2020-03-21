from typing import Callable, Any, Optional, List, Union
from timeit import default_timer
import logging


class DecoratorConfig:

    def __init__(
            self,
            normalization: Optional[Callable[[float], float]] = None,
            triggers: Optional[List[Callable[[float], Any]]] = None,
            log_level: Union[str, int] = logging.INFO,
    ):
        self.normalization = normalization
        self.triggers = [] if triggers is None else triggers
        logging._checkLevel(log_level)
        self.log_level = log_level

    def copy_config(self):
        return DecoratorConfig(
            normalization=self.normalization,
            triggers=self.triggers,
            log_level=self.log_level,
        )


class DecoratedCallable:

    def __init__(
            self,
            callable_object: Callable[..., Any],
            config: DecoratorConfig,
    ):
        self.callable_object = callable_object
        self.config = config
        self.logger = logging.getLogger(__name__)

    def __call__(self, *args, **kwargs):
        time_start = default_timer()
        val = self.callable_object(*args, **kwargs)
        time_delta = default_timer() - time_start
        if self.config.normalization is not None:
            time_delta = self.config.normalization(time_delta)
            
        for trigger in self.config.triggers:
            trigger(time_delta)
        
        self.logger.log(self.config.log_level, self._logger_message(time_delta))
        
        return val

    def _logger_message(self, time_delta: float):
        return (
            f'Finished timing for callable "{self.callable_object.__name__}" '
            f'in {time_delta}s.'
        )


class DecoratorTimer(DecoratorConfig):

    decorated_callable_class: DecoratedCallable = None

    def __call__(
            self,
            callable_object: Callable[..., Any]
    ) -> DecoratedCallable:
        return self.decorated_callable_class(
            callable_object=callable_object,
            config=self.copy_config()
        )

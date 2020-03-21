from .decorator_timer import DecoratedCallable, DecoratorTimer


class DecoratedFunction(DecoratedCallable):

    def _logger_message(self, time_delta: float):
        return (
            f'Finished timing for function "{self.callable_object.__name__}" '
            f'in {time_delta}s.'
        )


class FunctionTimer(DecoratorTimer):
    decorated_callable_class = DecoratedFunction


function_timer = FunctionTimer()

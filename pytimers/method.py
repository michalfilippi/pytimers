from .decorator_timer import DecoratedCallable, DecoratorTimer


class DecoratedMethod(DecoratedCallable):

    def _logger_message(self, time_delta: float):
        return (
            f'Finished timing for method "{self.callable_object.__name__}" '
            f'in {time_delta}s.'
        )


class MethodTimer(DecoratorTimer):
    decorated_callable_class = DecoratedMethod


method_timer = MethodTimer()

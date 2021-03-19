import inspect
import logging

from pytimers import timer, Timer


def test_function_decorator_preserves_output():
    @timer
    def func(a):
        return a

    assert func(2) == 2


def test_function_decorator_preserves_name():
    @timer
    def func(a):
        return a

    assert func.__name__ == "func"


def test_function_decorator_preserves_doc():
    @timer
    def func(a):
        """Function func docstring."""
        return a

    assert func.__doc__ == "Function func docstring."


def test_function_decorator_preserves_inspection():
    @timer
    def func(a, b: int = 1, *args: int, c: int = 1, **kwargs: int):
        return a + b + sum(args) + c + sum(kwargs.values())

    inspection = inspect.getfullargspec(func)

    assert inspection.args == ["a", "b"]
    assert inspection.varargs == "args"
    assert inspection.varkw == "kwargs"
    assert inspection.defaults == (1,)
    assert inspection.kwonlyargs == ["c"]
    assert inspection.kwonlydefaults == {"c": 1}
    assert inspection.annotations == {
        "b": int,
        "args": int,
        "c": int,
        "kwargs": int,
    }


def test_method_decorator_preserves_output():
    class Foo:
        @timer
        def bar(self, a):
            return a

    assert Foo().bar(2) == 2


def test_method_decorator_preserves_name():
    class Foo:
        @timer
        def bar(self, a):
            return a

    assert Foo().bar.__name__ == "bar"


def test_method_decorator_preserves_doc():
    class Foo:
        @timer
        def bar(self, a):
            """Method bar docstring."""
            return a

    assert Foo().bar.__doc__ == "Method bar docstring."


def test_method_decorator_preserves_inspection():
    class Foo:
        @timer
        def bar(self, a, b: int = 1, *args: int, c: int = 1, **kwargs: int):
            return a + b + sum(args) + c + sum(kwargs.values())

    inspection = inspect.getfullargspec(Foo().bar)

    assert inspection.args == ["self", "a", "b"]
    assert inspection.varargs == "args"
    assert inspection.varkw == "kwargs"
    assert inspection.defaults == (1,)
    assert inspection.kwonlyargs == ["c"]
    assert inspection.kwonlydefaults == {"c": 1}
    assert inspection.annotations == {
        "b": int,
        "args": int,
        "c": int,
        "kwargs": int,
    }


def test_static_method_decorator_preserves_output():
    class Foo:
        @staticmethod
        @timer
        def bar(a):
            return a

    assert Foo.bar(2) == 2


def test_static_method_decorator_preserves_name():
    class Foo:
        @staticmethod
        @timer
        def bar(a):
            return a

    assert Foo.bar.__name__ == "bar"


def test_static_method_decorator_preserves_doc():
    class Foo:
        @staticmethod
        @timer
        def bar(a):
            """Method bar docstring."""
            return a

    assert Foo.bar.__doc__ == "Method bar docstring."


def test_static_method_decorator_preserves_inspection():
    class Foo:
        @staticmethod
        @timer
        def bar(a, b: int = 1, *args: int, c: int = 1, **kwargs: int):
            return a + b + sum(args) + c + sum(kwargs.values())

    inspection = inspect.getfullargspec(Foo().bar)

    assert inspection.args == ["a", "b"]
    assert inspection.varargs == "args"
    assert inspection.varkw == "kwargs"
    assert inspection.defaults == (1,)
    assert inspection.kwonlyargs == ["c"]
    assert inspection.kwonlydefaults == {"c": 1}
    assert inspection.annotations == {
        "b": int,
        "args": int,
        "c": int,
        "kwargs": int,
    }


def test_class_method_decorator_preserves_output():
    class Foo:
        @classmethod
        @timer
        def bar(cls, a):
            return a

    assert Foo.bar(2) == 2


def test_class_method_decorator_preserves_name():
    class Foo:
        @classmethod
        @timer
        def bar(cls, a):
            return a

    assert Foo.bar.__name__ == "bar"


def test_class_method_decorator_preserves_doc():
    class Foo:
        @classmethod
        @timer
        def bar(cls, a):
            """Method bar docstring."""
            return a

    assert Foo.bar.__doc__ == "Method bar docstring."


def test_class_method_decorator_preserves_inspection():
    class Foo:
        @classmethod
        @timer
        def bar(cls, a, b: int = 1, *args: int, c: int = 1, **kwargs: int):
            return a + b + sum(args) + c + sum(kwargs.values())

    inspection = inspect.getfullargspec(Foo().bar)

    assert inspection.args == ["cls", "a", "b"]
    assert inspection.varargs == "args"
    assert inspection.varkw == "kwargs"
    assert inspection.defaults == (1,)
    assert inspection.kwonlyargs == ["c"]
    assert inspection.kwonlydefaults == {"c": 1}
    assert inspection.annotations == {
        "b": int,
        "args": int,
        "c": int,
        "kwargs": int,
    }


def test_function_decorator_creates_info_log(caplog):
    @timer
    def func():
        pass

    with caplog.at_level(logging.INFO):
        func()

    assert len(caplog.records) == 1
    assert caplog.records[0].levelno == logging.INFO


def test_function_decorator_creates_correct_log_level(caplog):
    custom_timer = Timer(log_level=logging.WARNING)

    @custom_timer
    def func():
        pass

    with caplog.at_level(logging.INFO):
        func()

    assert len(caplog.records) == 1
    assert caplog.records[0].levelno == logging.WARNING


def test_function_decorator_creates_correct_message(caplog):
    message = "No placeholder."
    custom_timer = Timer(log_template=message)

    @custom_timer
    def func():
        pass

    with caplog.at_level(logging.INFO):
        func()

    assert len(caplog.records) == 1
    assert caplog.records[0].message == message


def test_function_decorator_creates_correct_message_with_placeholders(caplog):
    custom_timer = Timer(log_template="Message ${name}.")

    @custom_timer
    def func():
        pass

    with caplog.at_level(logging.INFO):
        func()

    assert len(caplog.records) == 1
    assert caplog.records[0].message == "Message func."

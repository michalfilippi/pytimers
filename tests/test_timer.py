import inspect

import pytest

from timer import Timer, timer


@pytest.fixture
def complex_function():
    def f(a, b: int = 0, *args: int, **kwargs: int):
        """Docstring for the fucntion f."""
        return a + b + sum(args) + sum(kwargs.values())

    return f


@pytest.fixture
def decorated_function(complex_function):
    return timer(complex_function)


def test_timer_singleton_function_identical_output(
    complex_function, decorated_function
):
    @timer
    def func(a):
        return a

    assert func(2) == 2


def test_timer_singleton_function_preserves_name(complex_function, decorated_function):
    @timer
    def func(a):
        return a

    assert func.__name__ == "func"


def test_timer_singleton_function_preserves_doc(complex_function, decorated_function):
    @timer
    def func(a):
        """Function func docstring."""
        return a

    assert func.__doc__ == "Function func docstring."


def test_timer_singleton_function_preserves_inspection(
    complex_function, decorated_function
):
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


def test_timer_singleton_method_preserves_output():
    class Foo:
        @timer
        def bar(self, a):
            return a

    assert Foo().bar(2) == 2


def test_timer_singleton_method_preserves_name():
    class Foo:
        @timer
        def bar(self, a):
            return a

    assert Foo().bar.__name__ == "bar"


def test_timer_singleton_method_preserves_doc():
    class Foo:
        @timer
        def bar(self, a):
            """Method bar docstring."""
            return a

    assert Foo().bar.__doc__ == "Method bar docstring."


def test_timer_singleton_method_preserves_inspection():
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


def test_timer_singleton_static_method_preserves_output():
    class Foo:
        @timer
        @staticmethod
        def bar(a):
            return a

    assert Foo.bar(2) == 2


def test_timer_singleton_static_method_preserves_name():
    class Foo:
        @timer
        @staticmethod
        def bar(a):
            return a

    assert Foo.bar.__name__ == "bar"


def test_timer_singleton_static_method_preserves_doc():
    class Foo:
        @timer
        @staticmethod
        def bar(a):
            """Method bar docstring."""
            return a

    assert Foo.bar.__doc__ == "Method bar docstring."


def test_timer_singleton_static_method_preserves_inspection():
    class Foo:
        @timer
        @staticmethod
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

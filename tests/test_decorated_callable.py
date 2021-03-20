import inspect
import logging
from typing import Callable, List

import pytest

from pytimers import timer


def create_callables(extra_param: bool = False):
    @timer
    def callable_name(a, b: int = 1, *args: int, c: int = 1, **kwargs: int):
        """Callable docstring."""
        return a + b + sum(args) + c + sum(kwargs.values())

    class ClassWithMethod:
        @timer
        def callable_name(self, a, b: int = 1, *args: int, c: int = 1, **kwargs: int):
            """Callable docstring."""
            return a + b + sum(args) + c + sum(kwargs.values())

    class ClassWithStaticMethod:
        @staticmethod
        @timer
        def callable_name(a, b: int = 1, *args: int, c: int = 1, **kwargs: int):
            """Callable docstring."""
            return a + b + sum(args) + c + sum(kwargs.values())

    class ClassWithClassMethod:
        @classmethod
        @timer
        def callable_name(cls, a, b: int = 1, *args: int, c: int = 1, **kwargs: int):
            """Callable docstring."""
            return a + b + sum(args) + c + sum(kwargs.values())

    callables = [
        callable_name,
        ClassWithMethod().callable_name,
        ClassWithStaticMethod.callable_name,
        ClassWithStaticMethod().callable_name,
        ClassWithClassMethod.callable_name,
        ClassWithClassMethod().callable_name,
    ]

    if extra_param:
        return list(
            zip(
                callables,
                [
                    [],
                    ["self"],
                    [],
                    [],
                    ["cls"],
                    ["cls"],
                ],
            )
        )
    else:
        return callables


@pytest.mark.parametrize(
    "decorated_callable",
    create_callables(),
)
def test_decorator_preserves_output(decorated_callable: Callable):
    assert decorated_callable(2) == 4


@pytest.mark.parametrize(
    "decorated_callable",
    create_callables(),
)
def test_decorator_preserves_name(decorated_callable: Callable):
    assert decorated_callable.__name__ == "callable_name"


@pytest.mark.parametrize(
    "decorated_callable",
    create_callables(),
)
def test_decorator_preserves_doc(decorated_callable: Callable):
    assert decorated_callable.__doc__ == "Callable docstring."


@pytest.mark.parametrize(
    "decorated_callable,extra_params",
    create_callables(True),
)
def test_decorator_preserves_inspection(decorated_callable, extra_params: List[str]):
    inspection = inspect.getfullargspec(decorated_callable)

    assert inspection.args == extra_params + ["a", "b"]
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


@pytest.mark.parametrize(
    "decorated_callable",
    create_callables(),
)
def test_decorator_creates_info_log(decorated_callable: Callable, caplog):
    with caplog.at_level(logging.INFO):
        decorated_callable(1)

    assert len(caplog.records) == 1
    assert caplog.records[0].levelno == logging.INFO

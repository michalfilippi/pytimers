from __future__ import annotations
import inspect
from typing import Callable

import pytest

from pytimers import Timer
from pytimers.triggers.dummy_trigger import DummyTrigger


@pytest.fixture()
def trigger() -> DummyTrigger:
    return DummyTrigger()


@pytest.fixture()
def timer(trigger) -> Timer:
    return Timer(triggers=[trigger])


def create_test_cases() -> list[
    tuple[Callable[[Timer], Callable[..., int]], list[str], str]
]:
    def create_callable_function(timer: Timer):
        @timer
        def callable_name(a, b: int = 1, *args: int, c: int = 1, **kwargs: int) -> int:
            """Callable docstring."""
            return a + b + sum(args) + c + sum(kwargs.values())

        return callable_name

    def create_callable_method(timer: Timer):
        class ClassWithMethod:
            @timer
            def callable_name(
                self, a, b: int = 1, *args: int, c: int = 1, **kwargs: int
            ) -> int:
                """Callable docstring."""
                return a + b + sum(args) + c + sum(kwargs.values())

        return ClassWithMethod().callable_name

    def create_callable_static_method_from_class(timer: Timer):
        class ClassWithStaticMethod:
            @staticmethod
            @timer
            def callable_name(
                a, b: int = 1, *args: int, c: int = 1, **kwargs: int
            ) -> int:
                """Callable docstring."""
                return a + b + sum(args) + c + sum(kwargs.values())

        return ClassWithStaticMethod.callable_name

    def create_callable_static_method_from_instance(timer: Timer):
        class ClassWithStaticMethod:
            @staticmethod
            @timer
            def callable_name(
                a, b: int = 1, *args: int, c: int = 1, **kwargs: int
            ) -> int:
                """Callable docstring."""
                return a + b + sum(args) + c + sum(kwargs.values())

        return ClassWithStaticMethod().callable_name

    def create_callable_class_method_from_class(timer: Timer):
        class ClassWithClassMethod:
            @classmethod
            @timer
            def callable_name(
                cls, a, b: int = 1, *args: int, c: int = 1, **kwargs: int
            ) -> int:
                """Callable docstring."""
                return a + b + sum(args) + c + sum(kwargs.values())

        return ClassWithClassMethod.callable_name

    def create_callable_class_method_from_instance(timer: Timer):
        class ClassWithClassMethod:
            @classmethod
            @timer
            def callable_name(
                cls, a, b: int = 1, *args: int, c: int = 1, **kwargs: int
            ) -> int:
                """Callable docstring."""
                return a + b + sum(args) + c + sum(kwargs.values())

        return ClassWithClassMethod().callable_name

    return [
        (create_callable_function, [], "function"),
        (create_callable_method, ["self"], "method"),
        (create_callable_static_method_from_class, [], "static_method_from_class"),
        (
            create_callable_static_method_from_instance,
            [],
            "static_method_from_instance",
        ),
        (create_callable_class_method_from_class, ["cls"], "class_method_from_class"),
        (
            create_callable_class_method_from_instance,
            ["cls"],
            "class_method_from_instance",
        ),
    ]


test_cases, test_cases_extra_params, test_cases_names = list(zip(*create_test_cases()))


@pytest.mark.parametrize(
    argnames="decorated_callable_builder",
    argvalues=test_cases,
    ids=test_cases_names,
)
def test_decorator_preserves_output(
    timer: Timer,
    decorated_callable_builder: Callable[[Timer], Callable[..., int]],
):
    decorated_callable = decorated_callable_builder(timer)
    assert decorated_callable(2) == 4


@pytest.mark.parametrize(
    argnames="decorated_callable_builder",
    argvalues=test_cases,
    ids=test_cases_names,
)
def test_decorator_preserves_name(
    timer: Timer,
    decorated_callable_builder: Callable[[Timer], Callable[..., int]],
):
    decorated_callable = decorated_callable_builder(timer)
    assert decorated_callable.__name__ == "callable_name"


@pytest.mark.parametrize(
    argnames="decorated_callable_builder",
    argvalues=test_cases,
    ids=test_cases_names,
)
def test_decorator_preserves_doc(
    timer: Timer,
    decorated_callable_builder: Callable[[Timer], Callable[..., int]],
):
    decorated_callable = decorated_callable_builder(timer)
    assert decorated_callable.__doc__ == "Callable docstring."


@pytest.mark.parametrize(
    argnames="decorated_callable_builder,extra_params",
    argvalues=zip(test_cases, test_cases_extra_params),
    ids=test_cases_names,
)
def test_decorator_preserves_inspection(
    timer: Timer,
    decorated_callable_builder: Callable[[Timer], Callable[..., int]],
    extra_params: list[str],
):
    decorated_callable = decorated_callable_builder(timer)
    inspection = inspect.getfullargspec(decorated_callable)

    assert inspection.args == extra_params + ["a", "b"]
    assert inspection.varargs == "args"
    assert inspection.varkw == "kwargs"
    assert inspection.defaults == (1,)
    assert inspection.kwonlyargs == ["c"]
    assert inspection.kwonlydefaults == {"c": 1}
    assert inspection.annotations == {
        "b": "int",
        "args": "int",
        "c": "int",
        "kwargs": "int",
        "return": "int",
    }


@pytest.mark.parametrize(
    argnames="decorated_callable_builder",
    argvalues=test_cases,
    ids=test_cases_names,
)
def test_decorator_calls_trigger(
    trigger: DummyTrigger,
    timer: Timer,
    decorated_callable_builder: Callable[[Timer], Callable[..., int]],
):
    decorated_callable = decorated_callable_builder(timer)
    decorated_callable(1)

    assert len(trigger.calls) == 1

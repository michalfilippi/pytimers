import inspect
import logging
from asyncio import sleep

import pytest

from pytimers import timer


pytestmark = pytest.mark.asyncio


async def test_async_function_decorator_preserves_output():
    @timer
    async def func(a):
        return a

    assert (await func(4)) == 4


async def test_async_function_decorator_preserves_name():
    @timer
    async def func(a):
        return a

    assert func.__name__ == "func"


async def test_async_function_decorator_preserves_doc():
    @timer
    async def func(a):
        """Function func docstring."""
        return a

    assert func.__doc__ == "Function func docstring."


async def test_async_function_decorator_preserves_inspection():
    @timer
    async def func(a, b: int = 1, *args: int, c: int = 1, **kwargs: int):
        return a + b + sum(args) + c + sum(kwargs.values())

    inspection = inspect.getfullargspec(func)
    print(inspection)

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


async def test_async_function_decorator_logs_after_function_ends(caplog):
    log_message = "Inside Function."

    @timer
    async def func(a):
        await sleep(0.1)
        logging.getLogger(__name__).info(log_message)
        return a

    with caplog.at_level(logging.INFO):
        await func(1)

    assert len(caplog.records) == 2
    assert caplog.records[0].message == log_message

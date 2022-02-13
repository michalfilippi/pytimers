import pytest

from pytimers.immutable_stack import ImmutableStack


def test_empty_stack():
    stack = ImmutableStack.create_empty()
    assert stack.empty()

    with pytest.raises(IndexError):
        stack.pop()


def test_create_from_iterable():
    stack = ImmutableStack.create_from_iterable([1, 2, 3])

    assert not stack.empty()

    value, stack = stack.pop()
    assert value == 3

    value, stack = stack.pop()
    assert value == 2

    value, stack = stack.pop()
    assert value == 1

    with pytest.raises(IndexError):
        stack.pop()

from __future__ import annotations

from typing import Generic, Iterable, TypeVar


T = TypeVar("T")


class ImmutableStack(Generic[T]):
    def __init__(self, head: T, tail: ImmutableStack[T]):
        self._head = head
        self._tail = tail

    def empty(self) -> bool:
        return False

    def add(self, item: T) -> ImmutableStack[T]:
        return ImmutableStack(item, self)

    def pop(self) -> tuple[T, ImmutableStack[T]]:
        return self._head, self._tail

    @staticmethod
    def create_empty() -> ImmutableStack[T]:
        return EmptyImmutableStack[T]()

    @staticmethod
    def create_from_iterable(iterable: Iterable[T]) -> ImmutableStack[T]:
        stack: ImmutableStack[T] = ImmutableStack.create_empty()
        for value in iterable:
            stack = stack.add(value)
        return stack


class EmptyImmutableStack(ImmutableStack[T]):
    def __init__(self) -> None:
        pass

    def empty(self) -> bool:
        return True

    def pop(self) -> tuple[T, ImmutableStack[T]]:
        raise IndexError("pop from emtpy stack")

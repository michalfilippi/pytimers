from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Iterable, TypeVar


T = TypeVar("T")


class ImmutableStack(Generic[T], ABC):
    @abstractmethod
    def push(self, item: T) -> ImmutableStack[T]:
        pass

    @abstractmethod
    def pop(self) -> tuple[T, ImmutableStack[T]]:
        pass

    @abstractmethod
    def empty(self) -> bool:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass

    @staticmethod
    def create_empty() -> ImmutableStack[T]:
        return EmptyImmutableStack[T]()

    @staticmethod
    def create_from_iterable(iterable: Iterable[T]) -> ImmutableStack[T]:
        stack: ImmutableStack[T] = ImmutableStack.create_empty()
        for value in iterable:
            stack = stack.push(value)
        return stack


class NonemptyImmutableStack(ImmutableStack[T]):
    def __init__(self, head: T, tail: ImmutableStack[T]):
        self._head = head
        self._tail = tail
        self._len = len(tail) + 1

    def push(self, item: T) -> ImmutableStack[T]:
        return NonemptyImmutableStack(item, self)

    def pop(self) -> tuple[T, ImmutableStack[T]]:
        return self._head, self._tail

    def empty(self) -> bool:
        return False

    def __len__(self) -> int:
        return self._len


class EmptyImmutableStack(ImmutableStack[T]):
    def push(self, item: T) -> ImmutableStack[T]:
        return NonemptyImmutableStack(item, self)

    def pop(self) -> tuple[T, ImmutableStack[T]]:
        raise IndexError("pop from emtpy stack")

    def empty(self) -> bool:
        return True

    def __len__(self) -> int:
        return 0

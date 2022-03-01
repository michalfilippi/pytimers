from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Iterable, TypeVar


T = TypeVar("T")


class ImmutableStack(Generic[T], ABC):
    """Minimalistic implementation of an immutable stack. The stack is guaranteed
    to never change and any potential change creates a new instance of the stack.
    """

    @abstractmethod
    def push(self, item: T) -> ImmutableStack[T]:
        pass

    @abstractmethod
    def pop(self) -> tuple[T, ImmutableStack[T]]:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass

    def empty(self) -> bool:
        return len(self) == 0

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

    def __len__(self) -> int:
        return self._len


class EmptyImmutableStack(ImmutableStack[T]):
    def push(self, item: T) -> ImmutableStack[T]:
        return NonemptyImmutableStack(item, self)

    def pop(self) -> tuple[T, ImmutableStack[T]]:
        raise IndexError("pop from emtpy stack")

    def __len__(self) -> int:
        return 0

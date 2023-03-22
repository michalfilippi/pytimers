from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Iterable, TypeVar

T = TypeVar("T")


class ImmutableStack(Generic[T], ABC):
    """Minimalistic implementation of an immutable stack. The stack is guaranteed
    to never change and any potential change creates a new instance of the stack.
    """

    def push(self, item: T) -> ImmutableStack[T]:
        """Pushes a new item to the top of the stack.

        :param item: An item to be pushed to the stack.
        :return: New immutable stack object containing the new item and all items
            present in the original stack.
        """
        return NonemptyImmutableStack(item, self)

    @abstractmethod
    def pop(self) -> tuple[T, ImmutableStack[T]]:
        """Pops the top item from the stack.

        :return: Tuple of the popped item and the new immutable stack containing all
            items from the original stack except the top item.
        :raises: IndexError
        """

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

    def pop(self) -> tuple[T, ImmutableStack[T]]:
        return self._head, self._tail

    def __len__(self) -> int:
        return self._len


class EmptyImmutableStack(ImmutableStack[T]):
    def pop(self) -> tuple[T, ImmutableStack[T]]:
        raise IndexError("pop from emtpy stack")

    def __len__(self) -> int:
        return 0

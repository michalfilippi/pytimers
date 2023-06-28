from __future__ import annotations

from typing import (Any, Callable, Dict, Iterable, Optional, overload, TypeVar, Union)
from warnings import warn

from pytimers.timer import Timer
from pytimers.triggers import BaseTrigger

ReturnT = TypeVar("ReturnT")


class TimerFactory:
    def __init__(
        self,
        triggers: Iterable[BaseTrigger] = (),
        default_args: Optional[Dict[str, Any]] = None,
    ) -> None:
        """

        :param triggers:
        :param default_args:
        """
        self._triggers = list(triggers)
        self._default_args = {} if default_args is None else default_args

    @overload
    def __call__(
        self,
        wrapped: Callable[..., ReturnT],
        /,
    ) -> Callable[..., ReturnT]:
        pass

    @overload
    def __call__(
        self,
        *,
        label: Optional[str] = None,
        **kwargs: Any,
    ) -> Timer:
        pass

    def __call__(
        self,
        wrapped: Optional[Callable[..., ReturnT]] = None,
        *,
        label: Optional[str] = None,
        **kwargs: Any,
    ) -> Union[Callable[..., ReturnT], Timer]:
        pt = Timer(
            triggers=self._triggers,
            label=label,
            **{
                **self._default_args,
                **kwargs,
            },
        )
        if wrapped is None:
            return pt
        else:
            return pt(wrapped)

    def label(self, text: str) -> Timer:
        """Calls internally :py:meth:`pytimers.TimerFactory.__call__` while renaming
        `text` parameter to `label` parameter. This method exists only for a backward
        compatibility and will be removed in future versions.

        This makes the two following code snippets equivalent.

        .. highlight:: python
        .. code-block:: python

            from pytimers import Timer
            timer = Timer()
            with timer.label("example")
                pass

        .. highlight:: python
        .. code-block:: python

            from pytimers import Timer
            timer = Timer()
            with timer(label="example")
                pass

        :param text: Label text.
        :return: Returns ``ParametrizedTimer``.

        .. deprecated:: 4.0
        """

        warn(
            message=(
                "The `label` method will no longer be supported in future versions. "
                "Please use `__call__` method instead with `label` param set."
            ),
            category=DeprecationWarning,
        )

        return self(label=text)

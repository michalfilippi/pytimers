from __future__ import annotations

from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Optional,
    TypeVar,
    Union,
    overload,
)
from warnings import warn

from pytimers.parametrized_timer import ParameterizedTimer
from pytimers.triggers import BaseTrigger

ReturnT = TypeVar("ReturnT")


class Timer:
    def __init__(
        self,
        triggers: Iterable[BaseTrigger] = (),
        default_args: Optional[Dict[str, Any]] = None,
    ) -> None:
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
    ) -> ParameterizedTimer:
        pass

    def __call__(
        self,
        wrapped: Optional[Callable[..., ReturnT]] = None,
        *,
        label: Optional[str] = None,
        **kwargs: Any,
    ) -> Union[Callable[..., ReturnT], ParameterizedTimer]:
        params = {
            **self._default_args,
            **kwargs,
        }
        if wrapped is None:
            return ParameterizedTimer(
                triggers=self._triggers,
                label=label,
                **params,
            )
        else:
            pt = ParameterizedTimer(
                triggers=self._triggers,
                label=label,
                **params,
            )
            return pt(wrapped)

    def label(self, text: str) -> ParameterizedTimer:
        """

        :param text:
        :return:

        .. deprecated:: 4.0
        """
        warn(
            message=(
                "The `named` method will no longer be supported in future versions. "
                "Please use `label` method instead."
            ),
            category=DeprecationWarning,
        )

        return self(label=text)

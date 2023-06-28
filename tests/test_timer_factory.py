import pytest

from pytimers.timer import Timer
from pytimers.timer_factory import TimerFactory
from pytimers.triggers.dummy_trigger import DummyTrigger


@pytest.fixture()
def trigger() -> DummyTrigger:
    return DummyTrigger()


@pytest.fixture()
def timer_factory(trigger: DummyTrigger) -> TimerFactory:
    return TimerFactory(triggers=[trigger])


def test_decorator(
    trigger: DummyTrigger,
    timer_factory: TimerFactory,
) -> None:
    def f() -> str:
        return "hello"

    decorated_f = timer_factory(f)

    assert f() == decorated_f()
    assert len(trigger.calls) == 1


def test_call(
    trigger: DummyTrigger,
    timer_factory: TimerFactory,
) -> None:
    label = "l"
    timer = timer_factory(label=label)

    assert isinstance(timer, Timer)
    assert timer.label == label

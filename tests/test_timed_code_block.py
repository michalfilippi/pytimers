from asyncio import gather, sleep

import pytest

from pytimers.timer_factory import TimerFactory
from pytimers.triggers.dummy_trigger import DummyTrigger


@pytest.fixture()
def trigger() -> DummyTrigger:
    return DummyTrigger()


@pytest.fixture()
def timer(trigger: DummyTrigger) -> TimerFactory:
    return TimerFactory(triggers=[trigger])


def test_timer_calls_trigger_with_correct_params(
    timer: TimerFactory, trigger: DummyTrigger
) -> None:
    with timer():
        pass

    assert len(trigger.calls) == 1

    assert 0 < trigger.calls[0]["duration_s"]
    assert trigger.calls[0]["decorator"] is False
    assert trigger.calls[0]["label"] is None


def test_timer_preserves_exception(timer: TimerFactory, trigger: DummyTrigger) -> None:
    with pytest.raises(ValueError, match="msg"), timer():
        raise ValueError("msg")

    assert len(trigger.calls) == 1


def test_timer_supports_deprecated_label(timer: TimerFactory, trigger: DummyTrigger) -> None:
    label = "name_1"
    with timer.label(label):
        pass

    assert trigger.calls[0]["label"] == label


def test_timer_uses_proper_label(timer: TimerFactory, trigger: DummyTrigger) -> None:
    label = "name_1"
    with timer(label=label):
        pass

    assert trigger.calls[0]["label"] == label


def test_timer_uses_proper_name_in_nesting(
    timer: TimerFactory,
    trigger: DummyTrigger,
) -> None:
    label_1 = "name_1"
    label_2 = "name_2"
    label_3 = "name_3"

    with timer(label=label_1), timer(), timer(label=label_2), timer(label=label_3):
        pass

    assert trigger.calls[0]["label"] == label_3
    assert trigger.calls[1]["label"] == label_2
    assert trigger.calls[2]["label"] is None
    assert trigger.calls[3]["label"] == label_1


def test_timer_stores_duration(timer: TimerFactory) -> None:
    with timer() as clock:
        pass

    assert clock.duration() > 0


def test_timer_duration_round(timer: TimerFactory) -> None:
    with timer() as clock:
        pass

    assert clock.duration(0) == 0


def test_timer_exposes_current_duration(timer: TimerFactory) -> None:
    with timer() as clock:
        assert clock.current_duration() > 0


def test_timer_clock_is_running(timer: TimerFactory) -> None:
    with timer() as clock:
        assert clock.current_duration() != clock.current_duration()


def test_timer_current_duration_round(timer: TimerFactory) -> None:
    with timer() as clock:
        assert clock.current_duration(0) == 0


async def test_timer_is_robust_to_async(
    timer: TimerFactory,
    trigger: DummyTrigger,
) -> None:
    async def async_sleep(seconds: float, label: str) -> None:
        with timer(label=label):
            await sleep(seconds)

    await gather(
        async_sleep(0.003, "3ms"),
        async_sleep(0.004, "4ms"),
        async_sleep(0.002, "2ms"),
        async_sleep(0.005, "5ms"),
        async_sleep(0.001, "1ms"),
    )

    labels = [call["label"] for call in trigger.calls]

    assert labels == [
        "1ms",
        "2ms",
        "3ms",
        "4ms",
        "5ms",
    ]

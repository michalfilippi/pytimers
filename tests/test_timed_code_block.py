from asyncio import gather, sleep

import pytest

from pytimers.exceptions import UnfinishedTimer
from pytimers.timer import Timer
from pytimers.triggers.dummy_trigger import DummyTrigger


@pytest.fixture()
def trigger() -> DummyTrigger:
    return DummyTrigger()


@pytest.fixture()
def timer(trigger) -> Timer:
    return Timer(triggers=[trigger])


def test_custom_trigger_as_function():
    calls = []
    timer = Timer(triggers=[lambda *args: calls.append(args)])

    with timer.label("label"):
        pass

    assert len(calls) == 1

    duration_s, decorator, label = calls[0]
    assert 0 < duration_s
    assert decorator is False
    assert label == "label"


def test_timer_calls_trigger_with_correct_params(timer: Timer, trigger: DummyTrigger):
    with timer:
        pass

    assert len(trigger.calls) == 1

    duration_s, decorator, label = trigger.calls[0]
    assert 0 < duration_s
    assert decorator is False
    assert label is None


def test_timer_preserves_exception(timer: Timer, trigger: DummyTrigger):
    with pytest.raises(ValueError):
        with timer:
            raise ValueError()

    assert len(trigger.calls) == 1


def test_timer_uses_proper_label(timer: Timer, trigger: DummyTrigger):
    label = "name_1"
    with timer.label(label):
        pass

    assert trigger.calls[0][2] == label


def test_timer_uses_proper_name_in_nesting(timer: Timer, trigger: DummyTrigger):
    label_1 = "name_1"
    label_2 = "name_2"
    label_3 = "name_3"

    with timer.label(label_1):
        with timer:
            with timer.label(label_2):
                with timer.label(label_3):
                    pass

    assert trigger.calls[0][2] == label_3
    assert trigger.calls[1][2] == label_2
    assert trigger.calls[2][2] is None
    assert trigger.calls[3][2] == label_1


def test_timer_protects_unfinished_time(timer: Timer):
    with pytest.raises(UnfinishedTimer):
        with timer as clock:
            _ = clock.time


def test_timer_stores_time(timer: Timer):
    with timer as clock:
        pass

    assert clock.time > 0


def test_timer_exposes_current_duration(timer: Timer):
    with timer as clock:
        assert clock.current_duration > 0


def test_timer_clock_is_running(timer: Timer):
    with timer as clock:
        assert clock.current_duration != clock.current_duration


async def test_timer_is_robust_to_async(timer: Timer, trigger: DummyTrigger):
    async def async_sleep(seconds: float, label: str) -> None:
        with timer.label(label):
            await sleep(seconds)

    await gather(
        async_sleep(0.003, "3ms"),
        async_sleep(0.004, "4ms"),
        async_sleep(0.002, "2ms"),
        async_sleep(0.005, "5ms"),
        async_sleep(0.001, "1ms"),
    )

    labels = [call[2] for call in trigger.calls]

    assert labels == [
        "1ms",
        "2ms",
        "3ms",
        "4ms",
        "5ms",
    ]

from asyncio import gather, sleep

import pytest

from pytimers.exceptions import ClockStillRunning
from pytimers.timer import Timer
from pytimers.triggers.dummy_trigger import DummyTrigger


@pytest.fixture()
def trigger() -> DummyTrigger:
    return DummyTrigger()


@pytest.fixture()
def timer(trigger: DummyTrigger) -> Timer:
    return Timer(triggers=[trigger])


def test_custom_trigger_as_function() -> None:
    calls = []
    timer = Timer(triggers=[lambda *args: calls.append(args)])

    with timer.label("label"):
        pass

    assert len(calls) == 1

    duration_s, decorator, label = calls[0]
    assert 0 < duration_s
    assert decorator is False
    assert label == "label"


def test_timer_calls_trigger_with_correct_params(
    timer: Timer, trigger: DummyTrigger
) -> None:
    with timer:
        pass

    assert len(trigger.calls) == 1

    duration_s, decorator, label = trigger.calls[0]
    assert 0 < duration_s
    assert decorator is False
    assert label is None


def test_timer_preserves_exception(timer: Timer, trigger: DummyTrigger) -> None:
    with pytest.raises(ValueError):
        with timer:
            raise ValueError()

    assert len(trigger.calls) == 1


def test_timer_uses_proper_label(timer: Timer, trigger: DummyTrigger) -> None:
    label = "name_1"
    with timer.label(label):
        pass

    assert trigger.calls[0][2] == label


def test_timer_supports_deprecated_named(timer: Timer, trigger: DummyTrigger) -> None:
    label = "name_1"
    with pytest.deprecated_call():
        with timer.named(label):
            pass

    assert trigger.calls[0][2] == label


def test_timer_uses_proper_name_in_nesting(timer: Timer, trigger: DummyTrigger) -> None:
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


def test_timer_protects_unfinished_duration(timer: Timer) -> None:
    with pytest.raises(ClockStillRunning):
        with timer as clock:
            _ = clock.duration()


def test_timer_stores_duration(timer: Timer) -> None:
    with timer as clock:
        pass

    assert clock.duration() > 0


def test_timer_duration_round(timer: Timer) -> None:
    with timer as clock:
        pass

    assert clock.duration(0) == 0


def test_timer_exposes_current_duration(timer: Timer) -> None:
    with timer as clock:
        assert clock.current_duration() > 0


def test_timer_clock_is_running(timer: Timer) -> None:
    with timer as clock:
        assert clock.current_duration() != clock.current_duration()


def test_timer_current_duration_round(timer: Timer) -> None:
    with timer as clock:
        assert clock.current_duration(0) == 0


async def test_timer_is_robust_to_async(timer: Timer, trigger: DummyTrigger) -> None:
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

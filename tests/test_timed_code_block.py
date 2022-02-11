import pytest

from pytimers import Timer
from pytimers.triggers.dummy_trigger import DummyTrigger


@pytest.fixture()
def trigger() -> DummyTrigger:
    return DummyTrigger()


@pytest.fixture()
def timer(trigger) -> Timer:
    return Timer(triggers=[trigger])


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


def test_timer_starts_with_empty_time(timer: Timer):
    assert timer.time is None


def test_timer_stores_time(timer: Timer):
    with timer:
        pass

    assert timer.time is not None

from pytimers.triggers.dummy_trigger import DummyTrigger


def test_correct_call_content() -> None:
    trigger = DummyTrigger()
    duration_s = 1.0
    decorator = True
    label = "label"
    kwargs = {"extra": 1}
    trigger(
        duration_s=duration_s,
        decorator=decorator,
        label=label,
        **kwargs,
    )

    assert len(trigger.calls) == 1
    assert trigger.calls[0] == {
        "duration_s": duration_s,
        "decorator": decorator,
        "label": label,
        "kwargs": kwargs,
    }

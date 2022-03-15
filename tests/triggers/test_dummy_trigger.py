from pytimers.triggers.dummy_trigger import DummyTrigger


def test_correct_call_content():
    trigger = DummyTrigger()
    params = (1.0, True, "label")
    trigger(*params)

    assert len(trigger.calls) == 1
    assert trigger.calls[0] == params

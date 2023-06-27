from pytimers.triggers.profiler_trigger import ProfilerItem, ProfilerTrigger


def test_() -> None:
    trigger = ProfilerTrigger()
    trigger(1.0, False, profiler_part="aa.1")
    trigger(1.0, False, profiler_part="aa.1")
    trigger(1.0, False, profiler_part="aa.2")
    trigger(1.0, False, profiler_part="b")

    j = trigger.data.to_json()
    print(j)
    assert False

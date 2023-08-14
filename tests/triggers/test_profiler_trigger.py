from pytimers.triggers.profiler_trigger import ProfilerTrigger


def test_basic_call() -> None:
    trigger = ProfilerTrigger()
    trigger(1.0, False, profiler_part="aa.1")
    trigger(1.0, False, profiler_part="aa.1")
    trigger(1.0, False, profiler_part="aa.2")
    trigger(1.0, False, profiler_part="b")

    trigger.data.to_json()
    # ToDo finish test

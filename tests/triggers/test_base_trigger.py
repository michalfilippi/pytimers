from pytimers.triggers.base_trigger import BaseTrigger


def test_humanize_hours() -> None:
    humanized = BaseTrigger.humanized_duration(3 * 60**2 + 32 * 60 + 27.023561)

    assert humanized == "3h 32m 27s 24ms"


def test_humanize_minutes() -> None:
    humanized = BaseTrigger.humanized_duration(32 * 60 + 27.023561)

    assert humanized == "32m 27s 24ms"


def test_humanize_seconds() -> None:
    humanized = BaseTrigger.humanized_duration(27.023561)

    assert humanized == "27s 24ms"


def test_humanize_milliseconds() -> None:
    humanized = BaseTrigger.humanized_duration(0.023561)

    assert humanized == "24ms"


def test_humanize_milliseconds_with_precision() -> None:
    humanized = BaseTrigger.humanized_duration(0.023561, 2)

    assert humanized == "23.56ms"

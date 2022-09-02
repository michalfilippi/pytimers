from logging import INFO

from _pytest.logging import LogCaptureFixture

from pytimers.triggers.logger_trigger import LoggerTrigger


def test_creates_log(caplog: LogCaptureFixture) -> None:
    trigger = LoggerTrigger()
    with caplog.at_level(INFO):
        trigger(1.0, False, "label")

    assert len(caplog.records) == 1
    assert caplog.records[0].levelno == INFO


def test_trigger_uses_default_label(caplog: LogCaptureFixture) -> None:
    def_label = "def_label"
    trigger = LoggerTrigger(
        template="${label}",
        default_code_block_label=def_label,
    )
    with caplog.at_level(INFO):
        trigger(1.0, False)

    assert caplog.records[0].msg == def_label

from logging import INFO

from pytimers.triggers.logger_trigger import LoggerTrigger


def test_creates_log(caplog):
    trigger = LoggerTrigger()
    with caplog.at_level(INFO):
        trigger(1.0, False, "label")

    assert len(caplog.records) == 1
    assert caplog.records[0].levelno == INFO

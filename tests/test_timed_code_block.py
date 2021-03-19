import logging

import pytest

from pytimers import timer, Timer


def test_timer_creates_info_log(caplog):
    with caplog.at_level(logging.INFO):
        with timer:
            pass

    assert len(caplog.records) == 1
    assert caplog.records[0].levelno == logging.INFO


def test_timer_preserves_exception_and_logs(caplog):
    with caplog.at_level(logging.INFO):
        with pytest.raises(ValueError):
            with timer:
                raise ValueError()

    assert len(caplog.records) == 1


def test_timer_uses_proper_name(caplog):
    with caplog.at_level(logging.INFO):
        with timer.named("name_1"):
            pass

    assert "name_1" in caplog.records[0].message


def test_timer_uses_proper_name_in_nesting(caplog):
    with caplog.at_level(logging.INFO):
        with timer.named("name_1"):
            with timer:
                with timer.named("name_2"):
                    with timer.named("name_3"):
                        with timer.named("name_4"):
                            pass

    assert "name_4" in caplog.records[0].message
    assert "name_3" in caplog.records[1].message
    assert "name_2" in caplog.records[2].message
    assert "name_1" in caplog.records[4].message


def test_timer_creates_custom_log_message(caplog):
    template = "Template"
    with caplog.at_level(logging.INFO):
        with Timer(log_template=template):
            pass

    assert caplog.records[0].message == template


def test_timer_creates_custom_log_message_with_name(caplog):
    name = "block_name"
    with caplog.at_level(logging.INFO):
        with Timer(log_template="${name}").named(name):
            pass

    assert caplog.records[0].message == name

import logging

import pytest

from pytimers import Timer


@pytest.fixture
def default_timer():
    return Timer()


def test_timer_creates_info_log(default_timer, caplog):
    with caplog.at_level(logging.INFO):
        with default_timer:
            pass

    assert len(caplog.records) == 1
    assert caplog.records[0].levelno == logging.INFO


def test_timer_preserves_exception_and_logs(default_timer, caplog):
    with caplog.at_level(logging.INFO):
        with pytest.raises(ValueError):
            with default_timer:
                raise ValueError()

    assert len(caplog.records) == 1


def test_timer_uses_proper_name(default_timer, caplog):
    with caplog.at_level(logging.INFO):
        with default_timer.named("name_1"):
            pass

    assert "name_1" in caplog.records[0].message


def test_timer_uses_proper_name_in_nesting(default_timer, caplog):
    with caplog.at_level(logging.INFO):
        with default_timer.named("name_1"):
            with default_timer:
                with default_timer.named("name_2"):
                    with default_timer.named("name_3"):
                        with default_timer.named("name_4"):
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


def test_timer_starts_with_empty_time(default_timer):
    assert default_timer.time is None


def test_timer_stores_time(default_timer):
    with default_timer:
        pass

    assert default_timer.time is not None

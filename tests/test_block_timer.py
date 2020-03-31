from time import sleep

from block_timer import BlockTimer


def test_block_timer_time():
    with BlockTimer() as timer:
        sleep(0.1)

    assert type(timer.time) is float

    assert timer.time > 0

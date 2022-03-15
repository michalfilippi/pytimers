class ClockStillRunning(Exception):
    """Custom exception to be raised while accessing properties of
    :py:class:`pytimers.clock.Clock` before being stopped.
    """

    pass

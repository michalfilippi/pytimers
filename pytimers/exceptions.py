class TimerNotRunning(Exception):
    """Custom exception to be raised on attempt to read timer duration before
    starting it.
    """

    pass

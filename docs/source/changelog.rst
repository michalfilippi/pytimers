Changelog
=========

Release 3.0
-----------

* Implemented support for async context manage usage using :py:class:`contextvars.ContextVar`.
* Context manager now returns :py:class:`pytimers.started_clock.StartedClock` to expose :py:meth:`pytimers.started_clock.StartedClock.time` and :py:meth:`pytimers.started_clock.StartedClock.current_duration`.
* Logging moved outside of the :py:class:`pytimers.Timer` class and implemented as a separate trigger.
* Deprecating :py:meth:`pytimers.Timer.named` for :py:meth:`pytimers.Timer.label`.
* Sphinx documentation added.

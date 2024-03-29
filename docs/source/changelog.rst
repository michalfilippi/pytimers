Changelog
=========

Release 3.1
-----------

* Added ``py.typed`` file to mark full type checking compliance.
* Created manually triggered release pipeline to `Test PyPi <https://test.pypi.org/project/pytimers/>`_.


Release 3.0
-----------

* Implemented support for async context manage usage using :py:class:`contextvars.ContextVar`.
* Context manager now returns :py:class:`pytimers.clock.Clock` to expose :py:meth:`pytimers.clock.Clock.duration` and :py:meth:`pytimers.clock.Clock.current_duration`.
* Logging moved outside of the :py:class:`pytimers.Timer` class and implemented as a separate trigger.
* Deprecating :py:meth:`pytimers.Timer.named` for :py:meth:`pytimers.Timer.label`.
* Sphinx documentation added.

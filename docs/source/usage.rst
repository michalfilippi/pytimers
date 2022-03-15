Usage
=====

The whole purpose of this micro library is to provide easy and quick access to measuring the time it takes to run a piece of code without populating the codebase with reoccurring and unnecessary variables. The library allows you to measure the run time of your code in two ways. Using decorators for callables and using context manager to measure run time of any code block using the ``with`` statement.

The timer on it's own does not do anything unless provided with triggers (see :ref:`triggers`). In the following examples we will be using ``pytimers.timer`` which is a provided instance of :py:class:`pytimers.Timer` containing single trigger that logs measured time to std output using standard logging library :py:mod:`logging` using a trigger instance of :py:class:`pytimers.LoggerTrigger`.


Timer Decorator
---------------

The timer decorator can be applied to both synchronous and asynchronous functions and methods. PyTimers leverage python library `decorator <https://github.com/micheles/decorator>`_ to make sure decorating will preserve the function/method signature, name and docstring.

.. note::
    Decorating classes is currently not supported and will raise :py:exc:`TypeError`.

.. code-block:: python

    import logging
    from time import sleep

    from pytimers import timer


    logging.basicConfig(level=logging.INFO)

    @timer
    def func(*args: int):
        print("Hello from func.")
        sleep(1)
        return sum(args)


    if __name__ == "__main__":
        func(1, 2, 3)


.. code-block:: console

    Hello from func.
    INFO:pytimers.triggers.logger_trigger:Finished func in 1s 1.061ms [1.001s].

Class Methods and Static methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To combine ``timer`` decorator with decorators :py:func:`staticmethod` and :py:func:`classmethod` you have to first apply ``timer`` decorator. Applying the decorators the other way around will result in :py:exc:`TypeError` exception.

.. code-block:: python

    import logging
    from time import sleep

    from pytimers import timer


    logging.basicConfig(level=logging.INFO)

    class Foo:
        @staticmethod
        @timer
        def method(*args: int):
            print("Hello from static method.")
            sleep(1)
            return sum(args)


    if __name__ == "__main__":
        foo = Foo()
        foo.method(1, 2, 3)

.. code-block:: console

    Hello from static method.
    INFO:pytimers.triggers.logger_trigger:Finished Foo.method in 1s 1.025ms [1.001s].

Timer Context Manager
---------------------

To measure time of any piece of code not enclosed in a callable object you can use ``timer`` context manager capabilities.

.. code-block:: python

    import logging
    from time import sleep

    from pytimers import timer


    logging.basicConfig(level=logging.INFO)

    if __name__ == "__main__":
        with timer:
            print("Hello from code block.")
            sleep(1)

.. code-block:: console

    Hello from code block.
    INFO:pytimers.triggers.logger_trigger:Finished code block in 1s 1.143ms [1.001s].

Entering the context manager actually returns an instance of a :py:class:`pytimers.clock.Clock`. This allows you to access the current duration from inside of the code block but also the measured duration after the context manager is closed.

.. code-block:: python

    import logging
    from time import sleep

    from pytimers import timer


    logging.basicConfig(level=logging.INFO)

    if __name__ == "__main__":
        with timer as t:
            sleep(1)
            print(f"We want to run this under 5s and so far it took {t.current_duration}.")
            sleep(1)
        print(f"We still had {5 - t.duration}s remaining.")

.. code-block:: console

    We want to run this under 5s and so far it took 1.0001475979988754.
    INFO:pytimers.triggers.logger_trigger:Finished code block in 2s 1.384ms [2.001s].
    We still had 2.998615708000216s remaining.

Block of code can also be named to increase log readability.

.. code-block:: python

    import logging
    from time import sleep

    from pytimers import timer

    logging.basicConfig(level=logging.INFO)

    if __name__ == "__main__":
        with timer.label("data processing pipeline"):
            print("Hello from code block.")
            sleep(1)

.. code-block:: console

    Hello from code block.
    INFO:pytimers.triggers.logger_trigger:Finished data processing pipeline in 1s 0.625ms [1.001s].


Timer context manager also allows you to stack context managers freely without a worry of interference.

.. code-block:: python

    import logging
    from time import sleep

    from pytimers import timer

    logging.basicConfig(level=logging.INFO)

    if __name__ == "__main__":
        with timer.label("data collecting pipeline"):
            print("Hello from code block n.1.")
            sleep(1)
            with timer:
                print("Hello from code block n.2.")
                sleep(1)
                with timer.label("data processing pipeline"):
                    print("Hello from code block n.3.")
                    sleep(1)

.. code-block:: console

    Hello from code block n.1.
    Hello from code block n.2.
    Hello from code block n.3.
    INFO:pytimers.triggers.logger_trigger:Finished data processing pipeline in 1s 1.207ms [1.001s].
    INFO:pytimers.triggers.logger_trigger:Finished code block in 2s 2.895ms [2.003s].
    INFO:pytimers.triggers.logger_trigger:Finished data collecting pipeline in 3s 4.176ms [3.004s].


.. note::
    Timer context manager fully supports async code execution using :py:class:`contextvars.ContextVar`.


.. _triggers:

Triggers
--------

Triggers are an abstraction for the action performed after each timer is finished. The simplest trigger can just log the measured time using standard :py:mod:`logging` library. Trigger doing just that is already provided in the library as :py:class:`pytimers.LoggerTrigger`.

Triggers can be implemented in two ways. Either using a function with keywords arguments ``duration_s: float, decorator: bool, label: str`` or by defining a :py:class:`pytimers.BaseTrigger` subclass.

The following two examples shows how to implement a trivial custom trigger using both methods.

Function Based Trigger
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import logging
    from time import sleep

    from pytimers import Timer


    def custom_trigger(duration_s: float, decorator: bool, label: str):
        print(f"Measured duration is {duration_s}s.")

    if __name__ == "__main__":
        timer = Timer([custom_trigger])

        with timer:
            sleep(1)

.. code-block:: console

    Measured duration is 1.0010350150005252s.

BaseTrigger Subclass Trigger
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import logging
    from time import sleep
    from typing import Optional

    from pytimers import Timer, BaseTrigger


    class CustomTrigger(BaseTrigger):
        def __call__(
            self,
            duration_s: float,
            decorator: bool,
            label: Optional[str] = None,
        ) -> None:
            print(f"Measured duration is {duration_s}s.")


    if __name__ == "__main__":
        timer = Timer([CustomTrigger()])

        with timer:
            sleep(1)

.. code-block:: console

    Measured duration is 1.0010350150005252s.

Usage
=====

The whole purpose of this micro library is to provide easy and quick access to measuring the time it takes to run a piece of code without populating the codebase with reoccurring and unnecessary variables. The library allows you to measure the run time of your code in two ways. Using decorators for callables and using context manager to measure run time of any code block using the ``with`` statement.

The timer on it's own does not do anything. But when the time

The

Timer Decorator
---------------

The timer decorator can be applied to both synchronous and asynchronous functions and methods. Decorating classes is currently not supported and will raise :py:exc:`TypeError`. PyTimers leverage python library `decorator <https://github.com/micheles/decorator>`_ to make sure decorating will preserve the function/method signature, name and docstring.

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

To combine timer decorator with decorators :py:func:`staticmethod` and :py:func:`classmethod` you have to first apply timer decorator. Applying the decorators the other way around will result in :py:exc:`TypeError` exception.

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

To measure time of any code not enclosed in a callable object you can use timer context manager.

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

You can use the latest time measurement from the timer in your own code by accessing the `time` field.

.. code-block:: python

    import logging
    from time import sleep

    from pytimers import timer


    logging.basicConfig(level=logging.INFO)

    if __name__ == "__main__":
        with timer as t:
            print("We want to run this under 5s.")
            sleep(1)
        print(f"We still had {5 - t.time}s remaining.")

.. code-block:: console

    We want to run this under 5s.
    INFO:pytimers.triggers.logger_trigger:Finished code block in 1s 1.177ms [1.001s].
    We still had 3.998822992987698s remaining.

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

Async Compatibility
-------------------

Custom Triggers
---------------

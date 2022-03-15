
Pytimers is a python micro library that allows you to quickly measure time to run functions, methods or individual blocks of codes. Here's a quick demo.


.. code-block:: python

    import logging
    from time import sleep

    from pytimers import timer

    logging.basicConfig(level=logging.INFO)


    @timer
    def foo() -> None:
        print("Some heavy lifting.")
        sleep(2)


    if __name__ == "__main__":

        print("Let's call the function decorated with timer.")
        foo()

        print("Use timer context manager.")
        with timer.label("sleeping block"):
            print("Some more work to do.")
            sleep(1)


.. code-block:: console

    Let's call the function decorated with timer.
    Some heavy lifting.
    INFO:pytimers.triggers.logger_trigger:Finished foo in 2s 0.494ms [2.0s].
    Use timer context manager.
    Some more work to do.
    INFO:pytimers.triggers.logger_trigger:Finished sleeping block in 1s 1.247ms [1.001s].

# PyTimers
Python micro library for easy to use code timing with times logged using the standard library.

Requires Python3.6+.

## How to Install

```bash
# pip install pytimers
```

## Usage Example

The library allows you to measure the run time of your code in two way. Using decorators and
 using context manager to measure run time of any code block.

### Decorator Timer

```python
import logging
from time import sleep

from pytimers import timer


logging.basicConfig(level=logging.INFO)

@timer
def func(*args: int):
    print("Hello from func.")
    sleep(1)
    return sum(args)


if __name__ == '__main__':
    func(1, 2, 3)
```

```
Hello from func.
INFO:timer:Finished function func in 1.0018878109985963s.
```

PyTimers leverage python library [wrapt](https://wrapt.readthedocs.io/en/latest/) to make sure
 decorators can be applied to all function, methods, static methods and also class methods while
  not changing the callable signature in any way.

### Block Timer

```python
import logging
from time import sleep

from pytimers import timer


logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    with timer:
        print("Hello from code block.")
        sleep(1)
```

```
Hello from code block.
INFO:timer:Finished code block in 1.0027356049977243s.
```

```python
import logging
from time import sleep

from pytimers import timer


logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    with timer.name("data processing pipeline"):
        print("Hello from code block.")
        sleep(1)
```

```
Hello from code block.
INFO:timer:Finished data processing pipeline in 1.0051407059945632s.
```

```python
import logging
from time import sleep

from pytimers import timer


logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    with timer.name("data collecting pipeline"):
        print("Hello from code block n.1.")
        sleep(1)
        with timer.name("data processing pipeline"):
            print("Hello from code block n.2.")
            sleep(1)
```

```
Hello from code block n.1.
Hello from code block n.2.
INFO:timer:Finished data processing pipeline in 1.0008160540019162s.
INFO:timer:Finished data collecting pipeline in 2.0029643359885085s.
```

## When default setting is not enough

```python
import logging
from time import sleep

from pytimers import Timer


logging.basicConfig(level=logging.INFO)

custom_timer = Timer(
    log_template="Processing ${name} took ${duration}s.",
    log_level=logging.WARNING,
)

@custom_timer
def func(*args: int):
    print("Hello from func.")
    sleep(1)
    return sum(args)


if __name__ == '__main__':
    func(1, 2, 3)
```

```
Hello from func.
WARNING:timer:Processing function func took 1.0028993980085943s.
```

## Build Status

![tests](https://github.com/michalfilippi/pytimers/workflows/tests/badge.svg)

![flake8](https://github.com/michalfilippi/pytimers/workflows/flake8/badge.svg)

![black](https://github.com/michalfilippi/pytimers/workflows/black/badge.svg)

## PyPi

[
    ![PyPI](https://img.shields.io/pypi/v/pytimers)
](https://pypi.python.org/pypi/pytimers/)

[
    ![PyPI - License](https://img.shields.io/pypi/l/pytimers)
](https://pypi.python.org/pypi/pytimers/)

[
    ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytimers)
](https://pypi.python.org/pypi/pytimers/)

[
    ![PyPI - Implementation](https://img.shields.io/pypi/implementation/pytimers)
](https://pypi.python.org/pypi/pytimers/)




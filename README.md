# PyTimers
Python micro library for easy to use code timing.

Requires Python3.6+.

## How to Install

```bash
# pip install pytimers
```

## Usage Example

### Decorator

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

[![PyPI version fury.io](https://badge.fury.io/py/ansicolortags.svg)](https://pypi.python.org/pypi/pytimers/)

[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.python.org/pypi/pytimers/)

[![PyPI format](https://img.shields.io/pypi/format/ansicolortags.svg)](https://pypi.python.org/pypi/pytimers/)

[![PyPI pyversions](https://img.shields.io/pypi/pyversions/ansicolortags.svg)](https://pypi.python.org/pypi/pytimers/)

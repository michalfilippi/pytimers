# PyTimers
Python micro library for easy to use code timing with the elapsed times logged using the standard
 logging library.

Requires Python 3.6 and higher.

## How to Install

```bash
# pip install pytimers
```

## Usage Example

The library allows you to measure the run time of your code in two ways. Using decorators and 
 using  context manager to measure run time of any code block.

### Timer Decorator

The timer decorator can be applied to both synchronous and asynchronous functions and methods.
 Decorating classes is not supported and will raise `TypeError`. PyTimers leverage python library 
 [decorator](https://github.com/micheles/decorator) to make sure decorating will preserve the 
 function/method signature, name and docstring.

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


if __name__ == "__main__":
    func(1, 2, 3)
```

```
Hello from func.
INFO:pytimers.timer:Finished func in 1.0018878109985963s.
```

#### Class Methods and Static methods

To combine timer decorator with decorators `@staticmethoid` and `@classmethod` you have to first
 apply timer decorator. Applying the decorators the other way around will result in `TypeError`
 exception. 
 
```python
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
```

```
Hello from static method.
INFO:pytimers.timer:Finished Foo.method in 1.0001546249259263s.
```

### Block Timer
  
To measure time of any code not enclosed in a callable object you can use timer context manager.
  
```python
import logging
from time import sleep

from pytimers import timer


logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    with timer:
        print("Hello from code block.")
        sleep(1)
```

```
Hello from code block.
INFO:pytimers.timer:Finished code block in 1.0027356049977243s.
```

You can use the latest time measurement from the timer in your own code by accessing the `time` 
field.

```python
import logging
from time import sleep

from pytimers import timer


logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    with timer:
        print("We want to run this under 5s.")
        sleep(1)
    print(f"We still had {5 - timer.time}s remaining.")
```

```
We want to run this under 5s.
INFO:pytimers.timer:Finished code block in 1.003774584038183s.
We still had 3.996225415961817s remaining.
```

Block of code can also be named to increase log readability.

```python
import logging
from time import sleep

from pytimers import timer


logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    with timer.named("data processing pipeline"):
        print("Hello from code block.")
        sleep(1)
```

```
Hello from code block.
INFO:pytimers.timer:Finished data processing pipeline in 1.0051407059945632s.
```

Timer context manager also allows you to stack context managers freely without a worry of
 interference. 

```python
import logging
from time import sleep

from pytimers import timer


logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    with timer.named("data collecting pipeline"):
        print("Hello from code block n.1.")
        sleep(1)
        with timer:
            print("Hello from code block n.2.")
            sleep(1)
            with timer.named("data processing pipeline"):
                print("Hello from code block n.3.")
                sleep(1)
```

```
Hello from code block n.1.
Hello from code block n.2.
Hello from code block n.3.
INFO:pytimers.timer:Finished data processing pipeline in 1.0008160540019162s.
INFO:pytimers.timer:Finished code block in 2.005773539072834s.
INFO:pytimers.timer:Finished data collecting pipeline in 3.007467524963431s.
```

## Timer Custom Configuration

If you need to customize the timer you can create your own timer using provided `Timer` class.
 Customization consists of disabling logging, setting the log level, setting the log message
 template as `string.Template` compatible stings and adding custom triggers.

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


if __name__ == "__main__":
    func(1, 2, 3)
```

```
Hello from func.
WARNING:pytimers.timer:Processing func took 1.0028993980085943s.
```

Triggers should be functions with the following signature.
  
```python
def trigger(duration: float, name: str, code_block: bool) -> None:
    pass
``` 

## Build Status

![tests](https://github.com/michalfilippi/pytimers/workflows/tests/badge.svg)

![flake8](https://github.com/michalfilippi/pytimers/workflows/flake8/badge.svg)

![black](https://github.com/michalfilippi/pytimers/workflows/black/badge.svg)

![mypy](https://github.com/michalfilippi/pytimers/workflows/mypy/badge.svg)

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

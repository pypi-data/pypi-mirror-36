# pyinvoke

`pyinvoke` is a simple module that is used to invoked Python applications
using a full function specifier, similar to distlib entrypoints.

The key advantage is that the Python application you want to run will be
loaded as its proper module instead of as the `__main__` module. `pyinvoke`
will be the `__main__` module for this operation.

One of the motivating cases where `pyinvoke` comes in handy is the following:

    $ python -m module.main
    Traceback (most recent call last):
      File "module/main.py", line 7, in <module>
        from .stuff import ham
    SystemError: Parent module '' not loaded, cannot perform relative import

To run the application with `pyinvoke`:

    $ python3 -m pyinvoke module.main:main

Applications that depend on restarting can read the original commandline
from `sys.__argv__`:

```python
argv = getattr(sys, '__argv__', sys.argv)
```

---

<p align="center">Copyright &copy; 2018 Niklas Rosenstein</p>

"""
error models for pybugsnag
"""


class PyBugsnagException(Exception):
    """base pybugsnag exception class"""

    def __init__(self, *args, **kwargs):
        extra = ""
        if args:
            extra = '\n| extra info: "{extra}"'.format(extra=args[0])
        print(
            "[{exception}]: {doc}{extra}".format(
                exception=self.__class__.__name__, doc=self.__doc__, extra=extra
            )
        )
        Exception.__init__(self, *args, **kwargs)


class RateLimited(PyBugsnagException):
    """request received a 429 - you are currently rate limited"""

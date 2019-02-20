""" Utility functions for *pysg*."""
import inspect
import math
from functools import wraps

from pysg.error import PyrrTypeError
import numpy as np


def pyrr_type_checker(var: object, var_type: type) -> object:
    """ Makes sure that pyrr types are used as input. Tries to cast and raises PyrrTypeError if not possible.

    Args:
        var: Input variable.
        var_type: Type of input variable.

    Returns:
        Variable in correct type. Otherwise raise PyrrTypeError exception.

    """
    if type(var) is not var_type:
        try:
            return var_type(var)
        except Exception as e:
            raise PyrrTypeError(var, "Unsupported type. Expected %s type as input" % var_type)
    return var


def parameters_as_angles_deg_to_rad(*args_to_convert):
    """Converts specific angle arguments to angles in radians.

    Used as a decorator to reduce duplicate code.

    Arguments are specified by their argument name.
    For example
    ::

        @parameters_as_angles_deg_to_rad('a', 'b', 'optional')
        def myfunc(a, b, *args, **kwargs):
            pass

        myfunc(20, [15,15], optional=[80,80,80])
    """

    def decorator(fn):
        # wraps allows us to pass the docstring back
        # or the decorator will hide the function from our doc generator

        try:
            getfullargspec = inspect.getfullargspec
        except AttributeError:
            getfullargspec = inspect.getargspec

        @wraps(fn)
        def wrapper(*args, **kwargs):
            # get the arguments of the function we're decorating
            fn_args = getfullargspec(fn)

            # convert any values that are specified
            # if the argument isn't in our list, just pass it through

            # convert the *args list
            # we zip the args with the argument names we received from
            # the inspect function
            args = list(args)
            for i, (k, v) in enumerate(zip(fn_args.args, args)):
                if k in args_to_convert and v is not None:
                    if type(v) == float or type(v) == int:
                        args[i] = math.radians(v)
                    else:
                        args[i] = np.radians(v)

            # convert the **kwargs dict
            for k, v in kwargs.items():
                if k in args_to_convert and v is not None:
                    if type(v) == float or type(v) == int:
                        kwargs[k] = math.radians(v)
                    else:
                        kwargs[k] = np.radians(v)

            # pass the converted values to our function
            return fn(*args, **kwargs)

        return wrapper

    return decorator

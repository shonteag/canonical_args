"""
Provides decorators and utilities for interfacing
``canonical_args`` with python methods.
"""
from __future__ import absolute_import

import functools
import json
import types

from . import structure
from . import registry



FUNC_SPEC_VAR = "__canonical_arg_spec"
GET_SPEC_FUNC = "get_spec"

def arg_spec(spec, register=True):
    """
    method decorator for checking an argspec.
    """
    def inner(func):
        # register the spec to the function,
        if register and not hasattr(func, FUNC_SPEC_VAR):
            register_spec(func, spec)

        @functools.wraps(func)
        def _inner(*args, **kwargs):
            if register:
                spec = getattr(func, FUNC_SPEC_VAR)
            structure.check_args(spec, args, kwargs)
            return func(*args, **kwargs)
        return _inner
    return inner


def register_spec(func, spec):
    """
    add the argspec var to the function scope
    """
    setattr(func, FUNC_SPEC_VAR, spec)
    setattr(func, GET_SPEC_FUNC, types.MethodType(get_spec, func, type(func)))

def get_spec(func):
    if not hasattr(func, FUNC_SPEC_VAR):
        raise AttributeError("{} does not have a registered spec."\
                             " Consider using the ``register=True``"\
                             " flag in the ``arg_spec`` decorator.".format(
            func))
    return getattr(func, FUNC_SPEC_VAR)
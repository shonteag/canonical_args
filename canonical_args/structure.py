"""
Provides utilities for checking the structure of a list
or dict against provided structure mandates and details.
"""
from __future__ import absolute_import

import json



def check_list(names, types, values, arg):
    """
    recursively check a list of argument values (``arg``).
    usually used to check positional arguments passed to a
    function call.
    """
    # length
    try:
        assert len(types) == len(arg)
    except AssertionError, e:
        raise AssertionError("expected {} positional arguments, only"\
                             " got {}".format(len(types), len(arg)))

    for subname, subtype, subvalues, subarg in zip(names, types, values, arg):

        if isinstance(subtype, str) or isinstance(subtype, unicode):
            try:
                subtype = eval(subtype)
            except NameError:
                # THIS IS A CLASS, not a type!!!!!!
                # do the imports
                impo = ".".join(s for s in subtype.split(".")[:-1])
                exec("import {}".format(impo))
                subtype = eval(subtype)
        
        # recurse if list or tuple
        if (isinstance(subtype, list) or
            isinstance(subtype, tuple)):
            subname = ["{}#{}".format(subname, i) \
                       for i in range(0, len(subtype))]
            check_list(subname, subtype, subvalues, subarg)
            continue

        # check the type
        try:
            assert isinstance(subarg, subtype) or subarg is None
        except AssertionError, e:
            raise AssertionError("expected argument '{}' of type {}."\
                                 " got {}".format(
                subname, subtype, type(subarg)))

        # check the value
        # whitelisting
        if isinstance(subvalues, list):
            try:
                assert subarg in subvalues
            except AssertionError, e:
                raise AssertionError("`{}` is not a permitted value for"\
                                     " arg '{}'. expected value from"\
                                     " {}".format(subarg, subname, subvalues))

        # number ranging (int and float)
        elif ((isinstance(subvalues, str) or
               isinstance(subvalues, unicode)) and
              subvalues.startswith("range")):
            ran = eval(subvalues.replace("range", ""))
            try:
                assert ran[0] <= subarg and subarg <= ran[-1]
            except AssertionError, e:
                raise AssertionError("`{}` is not in range({}, {}) for"\
                                     " arg '{}'".format(subarg,
                                                        ran[0],
                                                        ran[-1],
                                                        subname))

def check_dict(structure_dict, kwargs):
    """
    usually used for checking kwargs
    """

    for kw, arg in kwargs.items():

        # make sure the keyword argument is registered
        assert kw in structure_dict
        struct = structure_dict[kw]

        if (isinstance(struct["type"], str) or
            isinstance(struct["type"], unicode)):
            kwtype = eval(struct["type"])

        if isinstance(kwtype, list) or isinstance(kwtype, tuple):
            subname = ["{}#{}".format(kw, i) for i in range(0, len(kwtype))]
            check_list(subname, kwtype, struct["values"], arg)
            continue

        # check the type
        try:
            assert isinstance(arg, kwtype) or arg is None
        except AssertionError, e:
            raise AssertionError("expected argument '{}' of type {}".format(
                kw, kwtype))

        # check the value
        # whitelisting
        if isinstance(struct["values"], list):
            try:
                assert arg in struct["values"]
            except AssertionError, e:
                raise AssertionError("`{}` is not a permitted value for"\
                                     " arg '{}'".format(arg, kw))

        # number ranging (int and float)
        elif ((isinstance(struct["values"], str) or
               isinstance(struct["values"], unicode)) and
              struct["values"].startswith("range")):
            ran = eval(struct["values"].replace("range", ""))
            try:
                assert ran[0] <= arg and arg <= ran[-1]
            except AssertionError, e:
                raise AssertionError("`{}` is not in range({}, {}) for"\
                                     " arg '{}'".format(arg,
                                                        ran[0],
                                                        ran[-1],
                                                        kw))

def check_args(struct, args, kwargs):
    """
    check the arguments provided against the structure.

    :param dict struct: the dict detailing the argument structure
    :param list args: the args to check against struct
    :param dict kwargs: the kwargs to check against the struct
    :raises AssertionError: when args or kwargs do not match struct
    """
    names = [sub["name"] for sub in struct["args"]]
    types = [sub["type"] for sub in struct["args"]]
    values = [sub["values"] for sub in struct["args"]]
    # args = args

    check_list(names, types, values, args)
    if kwargs:  # kwargs are optional!
        check_dict(struct["kwargs"], kwargs)


Arg Specs
=========

For ``canonical_args`` "specs" are ``dict``-formatted metadata
governing method arguments.  They provide the configurable
functionality of the module's ``check_args`` method, and associated
method decorators.

The basics of a Spec are as folows:

- they are of type ``dict``
- they contain at least the section ``"args"`` and may optionally
	contain the section ``"kwargs"``.
- each positional argument entry (``"args"``) contains the keys:
	``"name"``, ``"type"``, and ``"values"``.
- each keyword argument entry (``"kwargs"``) contains is of structure: ::
	
	{
		"kwarg-name": {
			"type": ...,
			"values": ...
		}
	}

- types and values may be nested to allow for lists and object-typed
	arguments.

Positional Arguments
--------------------

To define positional arguments for a method, let's first look at an
example: ::

	def somemethod(arg1, arg2, arg3):
		"""
		ensure ``arg1/arg2`` is an entry in ``arg3`` (list).
		"""
		return (arg1/arg2) in arg3

``somemethod`` requires three positional arguments. Let's first decide
the requirements for each of the arguments:

- ``arg1``
	- an integer
- ``arg2``
	- an integer
	- greater than 0 (to avoid ``ZeroDivisionError``'s)
- ``arg3``
	- a list

Now we model it in a ``dict``: ::

	[
		{
			"name": "arg1",
			"type": int,
			"values": None
		},
		{
			"name": "arg2",
			"type": int,
			"values": ">0"
		},
		{
			"name": "arg3",
			"type": list,
			"values": None
		}
	]

``arg1`` is defined as an ``int``, but has no value constraint, hence ``"values": None``.

``arg2`` is defined as an ``int``, but *must* be greater than 0, hence ``"values": ">0"``.

``arg3`` is defined as a ``list``, but again, has no value constraints.

.. note :: The ``"values"`` entry for ``"arg2"`` can take the following form:
	``">{}"``, ``"<{}"``, ``">={}"``, or ``"<={}"``, where ``"{}"`` is replaced
	by an integer or float.

.. note :: To add value and structure constraints to a list argument, we would do the following: ::
	
		{
			"name": "list_arg",
			"type": "list([int, float, str])",
			"values": [
				"range(0, 15)",
				">=50",
				["A", "B", "C"]
			]
		}

	``list_arg`` must be a list of length 3, with positon 0 as an integer between 0 and 14, position 1 as a float greater than or equal to 50, and position 2 a string equal to ``"A"``, ``"B"``, or ``"C"``.

Keyword Arguments
-----------------

Keyword arguments have no guaranteed position, and are not required input to a method.  Let's look at another example: ::

	def anothermethod(complete, total, percent=False):
		"""
		calculate completion, if percent flag is True,
		return answer as a percent.
		"""
		percentage = float(complete) / float(total)
		if percent:
			return percentage * 100.0
		return percentage

The above function takes two floats as positional arguments (above), and one
boolean flag as a keyword argument, defaulting to False.  In a spec dict: ::

	{
		"args": [
			{
				"name": "complete",
				"type": "float",
				"values": None
			},
			{
				"name": "total",
				"type": "float",
				"values": None
			}
		],
		"kwargs": {
			"percent": {
				"type": "bool",
				"values": None
			}
		}
	}

``complete`` is a float with no value constraints.

``total`` is a float with no value constraints.

``percent`` is a keyword argument of type ``bool`` with no value constraints.

.. note :: We can call ``anothermethod`` without specifying a ``percent`` argument, and the default value will be checked against the spec.

Nested Types and Values
-----------------------

Specs allow us to nest types and values very easily.  Consider a positional argument that must be a list containing:

- an integer greater than or equal to 0
- an integer between -10 and 10
- and a string equal to "A" or "B"

And the accompanying spec dict: ::

	{
		"args": [
			{
				"name": "arg1",
				"type": [int, int, str],
				"values": [
					">=0",
					"range(-10, 10)"
					["A", "B"]
				]
			}
		]
	}

Note that ``"values"`` and ``"type"`` now take the form of lists, with an entry for each required position in the argument.

Objects as Parameters
---------------------

It is often necessary to pass instantiated objects as parameters to methods.  This can also be handled by ``canonical_args``.  Let's assume we have a class located at ``a_package.a_module.SomeClass``.  To require a parameter to either instance **or subinstance** this class, we do the following: ::

	{
		"args": [
			{
				"name": "object_argument",
				"type": "a_package.a_module.SomeClass",
				"values": None
			}
		]
	}

``canonical_args`` will now ensure the parameter passed for ``"object_parameter"`` is of type ``"a_package.a_module.SomeClass"``, and will even import ``SomeClass`` from ``a_package.a_module`` automatically.

.. warning :: Ensure that any object path is to trusted code, or the import process can open a potential security vulnerability!!


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
			"values": ...,
			"required": ...
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
	- an integer or float
- ``arg2``
	- an integer or float
	- greater than 0 (to avoid ``ZeroDivisionError``'s)
- ``arg3``
	- a list

Now we model it in a ``dict``: ::

	[
		{
			"name": "arg1",
			"type": "one([int, float])"
			"values": {
				"int": None,
				"float": None
			}
		},
		{
			"name": "arg2",
			"type": "one([int, float])",
			"values": {
				"int": ">0",
				"float": ">0"
			}
		},
		{
			"name": "arg3",
			"type": list,
			"values": None
		}
	]

``arg1`` is defined as an ``int`` of ``float``, but has no value constraint, hence ``"values": None``.

``arg2`` is defined as an ``int`` or ``float``, but *must* be greater than 0, hence ``"values": {"int": ">0", "float": ">0"}``.  For choice of one type refs, the "values" key always contains an entry for each possible type.

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


Required vs. Non-Required Dictionary Keys
-----------------------------------------
By default, if a ``"type"`` is a ``dict``, all keys that appear within that dict are considered to be required.  We can turn this off by adding a key to the spec as follows: ::

	{
		"args": [],
		"kwargs": {
			"percent": {
				"type": bool,
				"values": None,
				"required": False
			}
		}
	}

The ``"required": False`` flag indicates to the ``structure.check_dict`` method that the key ``"percent"`` may be missing from the passed in ``dict``.


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

``dict``'s are slightly more complicated. Essentially, we nest the arg spec for a ``dict`` in the parent's ``"type"`` entry, and let recursion do the work.  Once again, let's use an example: ::

	{
		"args": [
			{
				"name": "arg1",
				"type": {
					"dict-keyword": {
						"type": int,
						"values": None
					},
					"dict-keywork2": {
						"type": float,
						"values": ">=0"
					}
				},
				"values": None
			}
		]
	}

This defines a method that takes a single argument of type ``dict``.  The ``dict`` however, in this case, **must** contain the keys ``"dict-keyword"`` (of type ``int`` with no value constraints), ``"dict-keyword2"`` (of type ``float`` and greater than or equal to 0).

.. note :: We can continue to nest as many ``dict``'s, ``list``'s and ``tuple``'s as we choose.

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


Syntax Cheat Sheet
==================

The syntax can be challenging at first, but once you master it, it's pretty powerful. We'll give the bellow cheat sheet, and some examples too! ::

	{
		"args": [
			{
				"name": "arg1",
				"type": TYPE_REF,
				"values": VALUE_REF
			}
		],
		"kwargs": {
			"kwarg1": {
				"type": TYPE_REF,
				"values": VALUE_REF
			}
		}
	}

Let's take a look at the keys step-by-step.

TYPE\_REF
---------

Type refs are formatted strings or types in python.  Here's the potential values, and what they do:


**Native type**: ``"int"`` or ``int``  

This is a native type. This works for all non-nested native types. ::

	{
		"type": "int",
		"values": VALUE_REF for int
	}


**NoneType**: ``"NoneType"``  

This is a native type of ``None``, or ``type(None)``. ::

	{
		"type": "NoneType",
		"values": null  # always null for NoneType
	}

.. note ::
	
	This may seem useless, as an argument that has to be None cannot pass any usable input, but this is not the case when nested. ::
	
		{
			"type": "one([int, float, NoneType])",
			"values": {
				"int": VALUE_REF for int,
				"float": VALUE_REF for float,
				"NoneType": null
			}
		}

	This argument can be an integer, a float, or None.


**Native type, iterable, unstructured**: ``"list"`` or ``list``  

This is a list native type. It has no required structure. ::

	{
		"type": "list",
		"values": null   # we cannot assign a value to an unstructured type
	}


**Native type, iterable, structured**: ``"list([int, str])"`` or ``list([int, str])``  

This is a list native type. It requires one integer, and one string, in that order. ::

	{
		"type": "list([int, str])"
		"values": [
			VALUE_REF for position 0, int
			VALUE_REF for position 1, str
		]
	}


**Native type, keyed, unstructured**: ``"dict"`` or ``dict``  

This is a dict native type. It has no required structure or keys. ::

	{
		"type": "dict",
		"values": null
	}


**Native type, keyed, structured**: ``{"a": {"type": int, "values": None}``  

This is a nested dict type. It indicates that the arg must be of type dict, and must contain the key ``"a"`` corresponding to an integer value. ::

	{
		"type": dict
		"values": {
			"subkey1": {
				"type": TYPE_REF for key subkey1,
				"values": VALUE_REF for key subkey1,
				"required": true (default)/false
			},
			...
		}
	}


**Native type, choice**: ``"one([int, float])"`` or ``canonical_args.check.ChoiceOfOne([int, float])``  

This is a "ChoiceOfOne" type. It indicates the arg can be one of either ``int`` or ``float`` types. ::

	{
		"type": "one([int, float])",
		"values": {
			"int": VALUE_REF for arg if arg is int,
			"float": VALUE_REF for arg if arg is float
		}
	}

.. note :: The ``"values"`` key is of type ``dict``, and contains an entry for each possible type in the ``"type": "one([int, float])"`` type ref.


**Class type**: ``"cls('import.string.to.ClassObject')"``  

This is a Class type. It indicates that the argument will instance or subinstance the class located at ``'import.string.to.ClassObject'``.  Imports will be made automatically. ::

	{
		"type": "cls('mymodule.MyClass')",
		"values": null  # cannot value check objects at this time
	}


**Type type**: ``"TypeType"``  

This is used to ensure the value of an argument itself *is* a type. So, for instance, passing ``int`` would pass the ``<type 'type'>`` check, but passing ``1`` would raise an ``AssertionError``. ::

	{
		"type": "TypeType",
		"values": [int, float]
	}

The value of the argument would have to be either ``int`` or ``float`` to pass the check.


VALUE\_REF
----------

Value refs are ``str``, ``list`` or ``dict`` in type, and detail the permissable values for the argument to which they correspond.

**Comparison**:  ``">{}"``, ``"<{}"``, ``">={}"``, ``"<={}"``, ``"!={}"``

This value ref compares a number to the number replacing the ``"{}"``. Obviously enough, only use these for TYPE\_REF ``float`` or ``int``. ::

	{
		"type": "int",
		"values": ">0"
	}

.. note ::
	
	Chaining comparison value refs is acceptable, and done as follows: ::

		"((<10||>10)&&!=5)||(<=0&&!=-3)"

	The number must be:

	- less than 10 or greater than 10, but not equal to 5, **or**
	- less than or equal to 0, but not equal to -3


**Range**: ``"range({}, {})"``  

This value ref ensures a numerical argument input falls between two numbers. **Note** that the range is inclusive, as in ``{}<=arg<={}``. ::
	
	{
		"type": "float",
		"values": "range(-5.5, 10.6)"
	}


**Preset list**: ``["SAMME", "SAMME.R"]``  

Ensure a argument input is in this list.  Good for control arguments, asking for algorithm names, for example. ::

	{
		"type": "str",
		"values": ["A", "B", "C"]
	}


.. note :: For details on nesting Type refs and value refs, see :doc:`specs`.


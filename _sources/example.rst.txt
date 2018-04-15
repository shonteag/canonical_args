An Example
==========

Now let's take a look at a more complex example where we implement a plug'n'play message handler of sorts.

.. note :: The purpose of this example is not to implement a message handler, but to show how dynamically run code can benefit from using ``canonical_args``.

To start, we begin with the project structure: ::

	mhandler/
		__init__.py
		handler.py
		handler_message1.py
		handler_message2.py

We have a directory containing the main code, ``handler.py`` and then several message-specific handler submodules.  The idea is to enable drag-and-drop functionality to the message handler (although if you head over to www.reddit.com/r/python, you can enter into an egaging debate as to why this is a bad or good idea).

Some basic assumptions, each submodule name ``"handler_*.py"`` will contain a method ``handle()`` and a spec dictionary ``argspec``.

``handler.py``: ::

	import os
	import glob
	import imp
	from canonical_args import check_args
	here = os.path.dirname(os.path.abspath(__name__))

	handlers = {}

	for filename in glob.glob(here, recursive=False):
		if filename.startswith("handler_") and filename.endswith(".py"):
			name = filename.replay(".py", "")
			handlers[name] = imp.load_source(name, filename)

	def handle(message_type, *args, **kwargs):
		if message_type not in handlers:
			raise KeyError("unkown message type")

		handler_module = handlers[message_type]

		# check the arguments
		check_args(handler_module.argspec, *args, **kwargs)

		return handler_module.handle(*args, **kwargs)

``handler_message1.py``: ::

	"""
	provide a handler for "message1" message type.
	"""
	argspec = {
		"args": [
			{
				"name": "recode_id",
				"type": str,
				"values": None
			}
		],
		"kwargs": {
			"filter": {
				"type": bool,
				"values": None
			},
			"sort": {
				"type": str,
				"values": [None, "ascending", "descending"]
			}
		}
	}

	def handle(record_id, filter=False, sort=None):
		"""
		return a list of entries corresponding to ``record_id``.
		"""
		...
		return records

We now have a argument-checked interface to add new handlers for message types whenever we like. ``handler_message2.py`` is not shown, as it simply follows the form of ``handler_message1.py``.

.. note :: There is another method of checking arguments without calling ``check_args`` in ``handler.handle`` method.  We can decorate each of the sub-handlers (eg. ``handler_message1.handle``) with the ``arg_spec`` decorator as follows: ::
	
		@arg_spec(
			{
				"args": [
					{
						"name": "recode_id",
						"type": str,
						"values": None
					}
				],
				"kwargs": {
					"filter": {
						"type": bool,
						"values": None
					},
					"sort": {
						"type": str,
						"values": [None, "ascending", "descending"]
					}
				}
			})
		def handle(record_id, filter=False, sort=None):
			...
			return records

	Of course, if we do this, we will have to change the ``handler.handle`` method in ``handler.py`` to match the refactor.


Getting Even More Complex
-------------------------

To take a closer look at nested types and values, let's implement ``handler_message2.py``: ::

	"""
	provide a handler for "message1" message type.
	"""
	from canonical_args.check import cls, one, NoneType, TypeType

	argspec = {
		"args": [
			{
				"name": "arg1",
				"type": "one([int, float, str])",
				"values": {
					"int": ">0&&!=5",
					"float": "<5.3||>7.8",
					"str": ["A", "B", "C", "X"]
				}
			},
			{
				"name": "arg2",
				"type": dict,
				"values": {
					"subkey1": {
						"type": cls('package.module.AClass'),
						"values": None,
						"required": True
					},
					"subkey2": {
						"type": TypeType,
						"values": [int, float],
						"required": False
					}
				}
			}
		],
		"kwargs": {
			"kwarg1": {
				"type": one([int, float, dict, NoneType]),
				"values": {
					"int": "!=100",
					"float": "range(0, 99)",
					"dict": {
						"subkey1": {
							"type": int,
							"values": ">=0&&!=10",
							"required": True
						},
						"subkey2": {
							"type": float,
							"values": None,
							"required": True
						}
					},
					"NoneType": None
				}
			},
			"kwarg2": {
				"type": one([int, NoneType]),
				"values": {
					"int": "(>10||<10)&&!=5",
					"NoneType": None
				}
			}
		}
	}

	@arg_spec(argspec)
	def handle(arg1, arg2, kwarg1=None, kwarg2=None):
		"""
		do something interesting, then return the result
		"""
		...
		return result

This is pretty overwhelming at first, so let's break it down argument by argument.

**arg1**:

- can be an ``int``, ``float``, or ``str``.
	- if ``int``, it must be greater than 0, but not equal to 5
	- if ``float``, it must be less than 5.3 or greater than 7.8
	- if ``str``, it must be one of "A", "B", "C" or "X"

**arg2**:

- is of type ``dict``
- must contain the subkeys:
	- "subkey1"
		- "subkey1" must be an object of type 'package.module.AClass'
- it can *optionally* contain:
	- "subkey2"
		- "subkey2" must be a TypeType, aka, a ``<type 'type'>``.
		- must be either ``int`` or ``float``

**kwarg1**:

- optional
- must be one of type ``int``, ``float``, ``dict`` or ``NoneType``.
- if ``int``, must not be equal to 100
- if ``float``, must be in inclusive range from 0 to 99
- if ``dict``, it must contain the subkeys:
	- "subkey1":
		- must be of type ``int``
		- must be greater than or equal to 0, but not equal to 10
	- "subkey2":
		- must be of type ``float``
- if ``NoneType``, it must simply be ``None``.

**kwarg2**:

- must be one of types ``int`` or ``NoneType``.
- if ``int``, must be greater than 10 or less than 10 **and** it cannot be equal to 5
- if ``NoneType``, it must simply be ``None``.

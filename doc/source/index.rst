.. canonical_args documentation master file, created by
   sphinx-quickstart on Thu Apr 12 11:19:59 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to canonical_args's documentation!
==========================================

canonical_args is a package designed to provide some certainty around
abstract method calls.  Consider, for instance: ::

	types = {
		"thing1": submodule.handle_thing1,
		"thing2": submodule2.handle_thing2
	}

	def message_handler(message_type, *args, **kwargs):
		return types[message_type](*args, **kwargs)

The above code implements an incredibly simple message handler. There is
no way to know, however, if the ``args`` and ``kwargs`` passed to the
subhandler method will be of the correct structure and/or types.  Enter
``canonical_args``.

Let's look at ``submodule.handle_thing1``. ::

	def handle_thing1(arg1, arg2, kwarg1=1):
		return float(arg1+arg2)/float(kwarg1)

Quite simply, ``arg1`` and ``arg2`` must be integers or floats and
``kwarg1`` must be greather than 0 for the method to successfully
execute.  We can represent this as JSON: ::

	{
		"args": [
			{
				"name": "arg1",
				"type": "float",
				"values": null
			},
			{
				"name": "arg2",
				"type": "float",
				"values": null
			}
		],
		"kwargs": {
			"kwarg1": {
				"type": "float",
				"values": ">0"
			}
		}
	}

Assuming we can store this JSON in a file or python variable, we can
modify the message handler like so: ::

	from canonical_args import check_args

	types = {
		"thing1": {
			"handler": submodule.handle_thing1,
			"argspec": submodule.handle_thing1_spec
		}
		"thing2": {
			"handler": submodule2.handle_thing2,
			"argspec": submodule2.handle_thing2_spec
		}
	}

	def message_handler(message_type, *args, **kwargs):
		spec = types[message_type]["argspec"]
		check_args(spec, *args, **kwargs)

		return types[message_type]["handler"](*args, **kwargs)

This may seem unecessary, since we can always add type checking code in
the message handling methods themselves, but what if we didn't write them,
and do not control them (like a 3rd party python package)? The
``check_args`` method call allows the implementer ensure the passed in
positional and keyword arguments match the method.  If they do not,
``check_args`` throws an ``AssertionError`` with further details as to
the failing argument.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   specs
   example
   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

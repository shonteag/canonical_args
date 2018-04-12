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


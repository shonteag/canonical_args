Registering Specs to Methods
============================

Methods can be made to remember their arg specs.  This can be quite handy when dynamically generating front-end code, for instance.

Registering with decorators
---------------------------
Methods decorated with the ``arg_spec`` decorator by default remember their specs. This allows us to retrieve them whenever we like, directly from the method itself.
Take the following method:

``amodule.py``: ::
	
	from canonical_args import arg_spec

	@arg_spec(
		{
			"args": [
				{
					"name": "arg1",
					"type": int,
					"values": None
				},
				{
					"name": "arg2",
					"type": float,
					"values": None
				}
			],
			"kwargs": {
				"kwarg1": {
					"type": str,
					"values": None
				}
			}
		}
	)
	def some_function(*args, **kwargs):
		return args, kwargs

We can now import this module from the python environment, and call up its Spec like so.

	>>> import amodule
	>>> amodule.some_function.get_spec()
	{"args": [{"name": "arg1", "type": int, "values": None},
			  {"name": "arg2", "type": float, "values": None}],
	 "kwargs": {"kwarg1": {"type": str, "values": None}}}

By doing such, we can even dynamically generate a front-end for in HTML or any other format for that matter, with proper type and value checking in Javascript.

Registering without decorators
------------------------------
Although decorators are quite useful, what if we do not control the source code containing the method to be decorated?  Quite simply, we can use the ``canonical_args`` module to ensure a method remembers its spec: ::

	from canonical_args import function, check_args
	# this is a third-party method we don't control
	from thirdparty_module import amethod

	function.register_spec(
		amethod,
		{"args": [{"name": "arg1", "type": int, "values": None}]})

	def passthrough(*args, **kwargs):
		check_args(amethod.get_spec(), *args, **kwargs)
		return amethod(*args, **kwargs)

Thusly, we create a ``passthrough`` method, which automatically checks the arguments for us.

.. note :: It is possible to force a method call to always call ``check_args`` upon execution by overriding its ``__call__`` instance method.  When working with code you do not control, however, this could cause some seriously whacky side-effects. So probably just don't do that.


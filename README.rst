canonical\_args
===============

.. image:: https://travis-ci.org/shonteag/canonical_args.svg?branch=master
    :target: https://travis-ci.org/shonteag/canonical_args

canonical_args is a package designed to provide some certainty around abstract method calls.  Consider, for instance, that we need to call one of many possible methods for a package we do not control.  Each of these methods has the same arguments, but the potential values change depending on the function.  We can write ``canonical_args`` arg specs for each of these methods, allowing us some clarity as to what each argument needs to be (types, values, etc.) when we execute dynamically: ::

	{
		"args": [
			{
				"name": "argument1",
				"type": int,
				"values": "range(0, 15)"
			},
			{
				"name": "argument2",
				"type": "one([int, float, str])",
				"values": {
					"int": ">0",
					"float": ">0",
					"str": ["A", "B", "C"]
				}
			}
		],
		"kwargs": {
			"loss_function": {
				"type": str,
				"values": ["quadratic", "0-1"]
			}
		}
	}

We can associate this spec with a method, either by registering it (if we do not control the method source): ::

	from canonical_args import register_spec

	# associates the spec to the method
	register_spec(somemethod, spec)

	# method instance method returns the registered spec
	print somemethod.get_spec()

or by decorating a method, if we do control it (let's say for a dynamically imported method handler sub-method). ::

	from canonical_args import argspec

	@arg_spec(spec, register=True)
	def ourmethod(argument1, argument2, loss_function="quadratic"):
		pass

	print ourmethod.get_spec()

This could potentially be of great use to dynamically generate frontend code with type and value-checking code.  The specs themselves could be stored in a file or database, allowing for fully dynamic method calls: ::

	from canonical_args import check_args
	import pymongo

	conn = pymongo.MongoClient("localhost", 27017)

	def handle(message_type, *args, **kwargs):
		spec = conn.somedatabase.arg_specs.find_one(
			{"message_type": message_type})
		subhandler = conn.somedatabase.handlers.find_one(
			{"message_type": message_type})

		# use canonical_args to check the unknown arguments
		# against the retrieved spec. will raise AssertionError
		# if fails.
		check_args(spec, *args, **kwargs)

		# if no errors raised, fire the retrieved handler method
		return subhandler(*args, **kwargs)

	def get_handler_spec(message_type):
		"""
		get the arg spec without executing the function. can
		be used at front end (eg. HTML) for generating an
		appropriate form for method calls.
		"""
		return conn.somedatabase.handlers.find_one(
			{"message_type": message_type})

The code above **does not** register the spec directly to the ``subhandler`` method, as it may not always be desirable to do so.  The choice is yours.

Full Documentation
------------------
https://shonteag.github.io/canonical_args/

Future Work
-----------
I aim to provide frontend code generation directly within the module, probably in a subpackage.  At least to handle HTML ``<form>`` generation, possibly with Javascript type matching.


Installation
------------
Simple as: ::

	pip install canonical_args

To run tests: ::

	git clone https://github.com/shonteag/canonical_args
	nosetests

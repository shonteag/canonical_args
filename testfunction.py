from __future__ import absolute_import

from canonical_args import arg_spec, check_args, register_spec
import json


class Obj(object):
	pass

@arg_spec(
	{
		"args": [
			{
				"name": "arg1",
				"type": str,
				"values": [
					"SAMME",
					"SAMME.R"
				]
			},
			{
				"name": "arg2",
				"type": "testfunction.Obj",
				"values": None
			}
		],
	}
)
def test(arg1, arg2):
	print arg1, arg2


@arg_spec("example.json")
def test2(arg1, arg2, arg3, kwarg1=None):
	print arg1, arg2, arg3, kwarg1


def test3(*args, **kwargs):
	with open("example.json") as f:
		spec = json.load(f)
	check_args(spec, args, kwargs)

	print args, kwargs

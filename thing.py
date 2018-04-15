from canonical_args.check import one, cls, NoneType, TypeType
from canonical_args import structure

class TestObj(object):
	pass

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
					"type": cls('__main__.TestObj'),
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

structure.check_args(
	argspec,
	["A", {"subkey1": TestObj(), "subkey2": int}],
	{"kwarg1": {"subkey1": 5, "subkey2": 93.1},
	 "kwarg2": 0})

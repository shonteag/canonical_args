from canonical_args.structure import checkspec



argspec = {
	"args": [
	],
	"kwargs": {
		"kwarg1": {
			"type": "one([int, float, dict])",
			"values": {
				"int": ">=0",
				"float": None,
				"dict": {
					"subkey1": {
						"type": "one([str, int, float, list([int, int])])",
						"values": {
							"str": ["A", "B", "C"],
							"int": ">0",
							"float": "<10||>20",
							"list": [
								"range(0, 100)",
								"!=50"
							]
						}
					}
				}
			}
		}
	}
}

checkspec(argspec, [], {"kwarg1": {"subkey1": [10, 49]}})
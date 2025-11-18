"""
Block configuration file - defines all Tetris blocks in a data-driven format.
To add a new block, simply add a new entry to the BLOCKS dictionary.
"""
from position import Position

BLOCKS = {
	"L": {
		"id": 1,
		"name": "L Block",
		"cells": {
			0: [Position(0, 2), Position(1, 0), Position(1, 1), Position(1, 2)],
			1: [Position(0, 1), Position(1, 1), Position(2, 1), Position(2, 2)],
			2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 0)],
			3: [Position(0, 0), Position(0, 1), Position(1, 1), Position(2, 1)]
		},
		"initial_offset": (0, 3),  # (row_offset, column_offset)
		"preview_offset": (270, 270)  # (x, y) for next block preview
	},
	"J": {
		"id": 2,
		"name": "J Block",
		"cells": {
			0: [Position(0, 0), Position(1, 0), Position(1, 1), Position(1, 2)],
			1: [Position(0, 1), Position(0, 2), Position(1, 1), Position(2, 1)],
			2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 2)],
			3: [Position(0, 1), Position(1, 1), Position(2, 0), Position(2, 1)]
		},
		"initial_offset": (0, 3),
		"preview_offset": (270, 270)
	},
	"I": {
		"id": 3,
		"name": "I Block",
		"cells": {
			0: [Position(1, 0), Position(1, 1), Position(1, 2), Position(1, 3)],
			1: [Position(0, 2), Position(1, 2), Position(2, 2), Position(3, 2)],
			2: [Position(2, 0), Position(2, 1), Position(2, 2), Position(2, 3)],
			3: [Position(0, 1), Position(1, 1), Position(2, 1), Position(3, 1)]
		},
		"initial_offset": (-1, 3),
		"preview_offset": (255, 290)  # Special offset for I block
	},
	"O": {
		"id": 4,
		"name": "O Block",
		"cells": {
			0: [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1)]
		},
		"initial_offset": (0, 4),
		"preview_offset": (255, 280)  # Special offset for O block
	},
	"S": {
		"id": 5,
		"name": "S Block",
		"cells": {
			0: [Position(0, 1), Position(0, 2), Position(1, 0), Position(1, 1)],
			1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 2)],
			2: [Position(1, 1), Position(1, 2), Position(2, 0), Position(2, 1)],
			3: [Position(0, 0), Position(1, 0), Position(1, 1), Position(2, 1)]
		},
		"initial_offset": (0, 3),
		"preview_offset": (270, 270)
	},
	"T": {
		"id": 6,
		"name": "T Block",
		"cells": {
			0: [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2)],
			1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 1)],
			2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1)],
			3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 1)]
		},
		"initial_offset": (0, 3),
		"preview_offset": (270, 270)
	},
	"Z": {
		"id": 7,
		"name": "Z Block",
		"cells": {
			0: [Position(0, 0), Position(0, 1), Position(1, 1), Position(1, 2)],
			1: [Position(0, 2), Position(1, 1), Position(1, 2), Position(2, 1)],
			2: [Position(1, 0), Position(1, 1), Position(2, 1), Position(2, 2)],
			3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 0)]
		},
		"initial_offset": (0, 3),
		"preview_offset": (270, 270)
	},
	"P": {
		"id": 8,
		"name": "Plus Block",
		"cells": {
			0: [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1)],
			1: [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1)],
			2: [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1)],
			3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1)]
		},
		"initial_offset": (0, 3),
		"preview_offset": (270, 270)
	},
	"U": {
		"id": 9,
		"name": "U Block",
		"cells": {
			0: [Position(0, 0), Position(0, 2), Position(1, 0), Position(1, 1), Position(1, 2)],
			1: [Position(0, 0), Position(0, 1), Position(1, 0), Position(2, 0), Position(2, 1)],
			2: [Position(0, 0), Position(0, 1), Position(0, 2), Position(1, 0), Position(1, 2)],
			3: [Position(0, 1), Position(0, 2), Position(1, 2), Position(2, 1), Position(2, 2)]
		},
		"initial_offset": (0, 3),
		"preview_offset": (270, 270)
	},
	"X": {
		"id": 10,
		"name": "X Block",
		"cells": {
			0: [Position(0, 0), Position(0, 2), Position(1, 1), Position(2, 0), Position(2, 2)],
			1: [Position(0, 0), Position(0, 2), Position(1, 1), Position(2, 0), Position(2, 2)],
			2: [Position(0, 0), Position(0, 2), Position(1, 1), Position(2, 0), Position(2, 2)],
			3: [Position(0, 0), Position(0, 2), Position(1, 1), Position(2, 0), Position(2, 2)]
		},
		"initial_offset": (0, 3),
		"preview_offset": (270, 270)
	},
	"LINE3": {
		"id": 11,
		"name": "Line 3",
		"cells": {
			0: [Position(1, 0), Position(1, 1), Position(1, 2)],
			1: [Position(0, 1), Position(1, 1), Position(2, 1)],
			2: [Position(1, 0), Position(1, 1), Position(1, 2)],
			3: [Position(0, 1), Position(1, 1), Position(2, 1)]
		},
		"initial_offset": (0, 3),
		"preview_offset": (270, 270)
	},
	"LONG_L": {
		"id": 12,
		"name": "Long L",
		"cells": {
			0: [Position(0, 2), Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 0)],
			1: [Position(0, 0), Position(0, 1), Position(1, 1), Position(2, 1), Position(2, 2)],
			2: [Position(0, 2), Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 0)],
			3: [Position(0, 0), Position(0, 1), Position(1, 1), Position(2, 1), Position(2, 2)]
		},
		"initial_offset": (0, 3),
		"preview_offset": (270, 270)
	}
}

def get_all_block_keys():
	"""Returns a list of all block keys in the configuration"""
	return list(BLOCKS.keys())

def get_block_config(block_key):
	"""Returns the configuration for a specific block"""
	return BLOCKS.get(block_key)

def get_block_preview_offset(block_key):
	"""Returns the preview offset for a block, or default if not found"""
	config = get_block_config(block_key)
	if config:
		return config["preview_offset"]
	return (270, 270)  # Default offset

def get_preview_offset_by_id(block_id):
	"""Returns the preview offset for a block by its ID"""
	for config in BLOCKS.values():
		if config["id"] == block_id:
			return config["preview_offset"]
	return (270, 270)  # Default offset

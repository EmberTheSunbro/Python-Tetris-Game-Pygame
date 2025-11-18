# Block Configuration Guide

This Tetris game now uses a **configuration-based block system**, making it easy to add new block types without modifying game logic.

## How It Works

All blocks are defined in `block_config.py` as data structures. The `BlockFactory` reads this configuration and creates block instances dynamically.

## Adding a New Block

To add a new block type, simply add a new entry to the `BLOCKS` dictionary in `block_config.py`:

```python
"NEW_BLOCK": {
    "id": 8,  # Unique ID (must not conflict with existing blocks)
    "name": "New Block",
    "cells": {
        0: [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 0)],  # Rotation state 0
        1: [Position(0, 0), Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 2)],  # Rotation state 1
        2: [Position(0, 2), Position(1, 1), Position(1, 2), Position(2, 1), Position(2, 2)],  # Rotation state 2
        3: [Position(0, 0), Position(1, 0), Position(1, 1), Position(2, 1), Position(2, 2)]   # Rotation state 3
    },
    "initial_offset": (0, 3),  # (row_offset, column_offset) - starting position
    "preview_offset": (270, 270)  # (x, y) - position in the "Next" preview box
}
```

### Field Descriptions

- **id**: Unique numeric identifier (used for colors and grid storage)
- **name**: Human-readable name for the block
- **cells**: Dictionary mapping rotation states (0, 1, 2, 3) to lists of Position objects
  - Each Position(row, col) represents one cell of the block
  - Positions are relative to the block's origin
  - Use 0-3 rotation states (or fewer if block doesn't rotate)
- **initial_offset**: Starting position offset when block spawns (row, col)
- **preview_offset**: Pixel coordinates for drawing in the "Next" preview area

### Example: Adding a 5-Cell Block

```python
"PENTOMINO": {
    "id": 8,
    "name": "Pentomino",
    "cells": {
        0: [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1)],
        1: [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1)],
        2: [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1)],
        3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1)]
    },
    "initial_offset": (0, 3),
    "preview_offset": (270, 270)
}
```

## Color Support

To add a color for your new block, update `colors.py`:

```python
@classmethod
def get_cell_colors(cls):
    return [
        cls.dark_grey,  # 0 - empty
        cls.green,      # 1 - L block
        cls.red,        # 2 - J block
        cls.orange,     # 3 - I block
        cls.yellow,     # 4 - O block
        cls.purple,     # 5 - S block
        cls.cyan,       # 6 - T block
        cls.blue,       # 7 - Z block
        cls.your_color  # 8 - Your new block
    ]
```

The color at index `id` will be used for that block.

## Benefits

✅ **No code changes needed** - Just add to config  
✅ **Easy to test** - Modify config, restart game  
✅ **Non-programmers can add blocks** - Just need to understand Position coordinates  
✅ **Centralized definitions** - All blocks in one place  
✅ **Automatic integration** - Game automatically picks up new blocks  

## Current Blocks

- **L**: L-shaped block (id: 1)
- **J**: J-shaped block (id: 2)
- **I**: Line block (id: 3)
- **O**: Square block (id: 4)
- **S**: S-shaped block (id: 5)
- **T**: T-shaped block (id: 6)
- **Z**: Z-shaped block (id: 7)

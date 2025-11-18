# Block Configuration Guide

This Tetris game now uses a **configuration-based block system**, making it easy to add new block types without modifying game logic.

## How It Works

All blocks are defined in `block_config.py` as data structures. The `BlockFactory` reads this configuration and creates block instances dynamically.

## Adding a New Block

To add a new block type, simply add a new entry to the `BLOCKS` dictionary in `block_config.py`. **You only need to define the base shape** - all rotation states are generated automatically!

```python
"NEW_BLOCK": {
    "id": 13,  # Unique ID (must not conflict with existing blocks)
    "name": "New Block",
    "base_shape": [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 0)],
    "initial_offset": (0, 3),  # (row_offset, column_offset) - starting position
    "preview_offset": (270, 270)  # (x, y) - position in the "Next" preview box
}
```

### Field Descriptions

- **id**: Unique numeric identifier (used for colors and grid storage)
- **name**: Human-readable name for the block
- **base_shape**: List of Position objects representing the block's base shape (rotation state 0)
  - Each Position(row, col) represents one cell of the block
  - Positions are relative to the block's origin (typically starting from (0,0))
  - **All rotation states (0°, 90°, 180°, 270°) are automatically generated!**
- **initial_offset**: Starting position offset when block spawns (row, col)
- **preview_offset**: Pixel coordinates for drawing in the "Next" preview area

### Example: Adding a 5-Cell Plus Block

```python
"PLUS": {
    "id": 13,
    "name": "Plus Block",
    "base_shape": [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1)],
    "initial_offset": (0, 3),
    "preview_offset": (270, 270)
}
```

**That's it!** The system will automatically:
- Generate all 4 rotation states (or fewer if the block is symmetric)
- Handle rotation around the block's center
- Normalize positions correctly

### Rotation Behavior

- **Symmetric blocks** (like O, Plus, X): Will automatically detect that rotations repeat and only generate unique states
- **Asymmetric blocks** (like L, J, S, Z): Will generate all 4 rotation states
- **Blocks with 2-fold symmetry** (like I, LINE3): Will generate 2 rotation states

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

### Standard Tetrominoes (4-cell blocks)
- **L**: L-shaped block (id: 1) - Green
- **J**: J-shaped block (id: 2) - Red
- **I**: Line block (id: 3) - Orange
- **O**: Square block (id: 4) - Yellow
- **S**: S-shaped block (id: 5) - Purple
- **T**: T-shaped block (id: 6) - Cyan
- **Z**: Z-shaped block (id: 7) - Blue

### Extended Blocks (5-cell and 3-cell)
- **P**: Plus/Cross block (id: 8) - Pink - 5-cell symmetric cross shape
- **U**: U-shaped block (id: 9) - Lime - 5-cell U shape
- **X**: X-shaped block (id: 10) - Teal - 5-cell X shape (diagonal cross)
- **LINE3**: 3-cell line block (id: 11) - Maroon - Smaller version of I block
- **LONG_L**: Extended L block (id: 12) - Navy - 5-cell L variant

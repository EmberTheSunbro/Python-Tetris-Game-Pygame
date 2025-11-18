# High-Level Approaches for Expanding Block Types

## Current State Analysis
The current implementation has blocks individually checked and hardcoded:
- Blocks are defined as separate classes in `blocks.py`
- Block list is hardcoded in `Game.__init__()`: `[IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]`
- Drawing logic in `Game.draw()` has hardcoded checks for specific block IDs (3 and 4) for positioning
- Each block manually defines rotation states and initial positions

---

## Approach 1: Registry Pattern with Block Metadata

### Overview
Create a centralized block registry that stores block definitions and metadata. Blocks register themselves automatically, and the game queries the registry instead of hardcoding block lists.

### Key Components:
1. **BlockRegistry Class**: A singleton/class-level registry that maintains:
   - List of all available block classes
   - Block metadata (name, ID, preview offset, spawn position, etc.)
   - Factory method to create instances

2. **Block Metadata**: Each block class would define:
   - Display name
   - Preview rendering offset (x, y)
   - Default spawn position offset
   - Color ID mapping
   - Any special properties

3. **Automatic Registration**: Blocks register themselves via decorator or class inheritance:
   ```python
   @register_block(preview_offset=(270, 270))
   class NewBlock(Block):
       ...
   ```

### Benefits:
- Adding a new block = create class + register (no changes to Game class)
- Centralized metadata management
- Easy to query available blocks
- Can enable/disable blocks dynamically
- Preview positioning handled automatically

### Changes Required:
- Create `BlockRegistry` class
- Add registration mechanism to block classes
- Replace hardcoded list in `Game.__init__()` with registry query
- Replace hardcoded drawing logic with metadata-based positioning

---

## Approach 2: Configuration-Driven Block System

### Overview
Move block definitions to external configuration (JSON/YAML) or data structures. Blocks become data-driven rather than code-driven, with a generic Block class handling all block types.

### Key Components:
1. **Block Configuration Format**: JSON/YAML file or Python dict defining:
   ```json
   {
     "blocks": [
       {
         "id": 8,
         "name": "UBlock",
         "cells": {
           "0": [[0,0], [0,1], [0,2], [1,0], [1,2]],
           "1": [[0,1], [1,1], [2,0], [2,1], [2,2]],
           ...
         },
         "spawn_offset": [0, 3],
         "preview_offset": [270, 270],
         "color_id": 8
       }
     ]
   }
   ```

2. **Generic Block Class**: Single `Block` class that takes configuration:
   - Loads cell positions from config
   - Handles all rotation logic generically
   - Uses config for positioning and colors

3. **Block Loader**: Utility to load block definitions from config files

### Benefits:
- No code changes needed to add blocks (just edit config)
- Non-programmers can add blocks
- Easy to test different block configurations
- Can load different block sets for different game modes
- Version control friendly (easy to see diffs)

### Changes Required:
- Create configuration file format
- Refactor `Block` class to be generic/config-driven
- Create block loader utility
- Update `Game` class to load blocks from config
- Update drawing logic to use config-based offsets

---

## Approach 3: Plugin Architecture with Abstract Base Class

### Overview
Use Python's ABC (Abstract Base Class) to define a block interface. Each block type is a plugin that implements the interface. Blocks are discovered automatically from a blocks directory.

### Key Components:
1. **AbstractBlock Interface**: Defines required methods:
   - `get_cell_positions()` - returns cells for current rotation
   - `get_preview_offset()` - returns (x, y) for preview rendering
   - `get_spawn_offset()` - returns initial spawn position
   - `get_id()` - returns unique identifier

2. **Block Discovery System**: Automatically scans `blocks/` directory:
   - Imports all Python files
   - Finds classes inheriting from `AbstractBlock`
   - Registers them automatically

3. **Block Base Class Enhancements**: Add default implementations:
   - Standard preview offset calculation
   - Automatic spawn position calculation
   - Common rotation logic

### Benefits:
- True separation of concerns (each block in own file)
- Automatic discovery - just add file to blocks directory
- Easy to test individual blocks
- Can have different block sets by directory
- Follows open/closed principle (open for extension, closed for modification)

### Changes Required:
- Create `AbstractBlock` ABC
- Refactor existing blocks to inherit from ABC
- Create block discovery/loader module
- Split blocks.py into individual files (optional but recommended)
- Update `Game` class to use discovered blocks
- Add default preview offset logic to base class

---

## Comparison Summary

| Aspect | Registry Pattern | Config-Driven | Plugin Architecture |
|--------|-----------------|---------------|---------------------|
| **Ease of Adding Blocks** | Medium (code + register) | Easy (edit config) | Easy (add file) |
| **Flexibility** | High | Very High | High |
| **Code Changes Needed** | Moderate | High refactoring | Moderate |
| **Runtime Performance** | Fast | Fast | Fast |
| **Non-Programmer Friendly** | No | Yes | No |
| **Type Safety** | High | Medium | High |
| **Best For** | Structured expansion | Rapid prototyping | Large-scale expansion |

---

## Recommendation
For this Tetris game, **Approach 1 (Registry Pattern)** offers the best balance:
- Maintains code structure and type safety
- Minimal refactoring required
- Easy to add new blocks (just create class + decorator)
- Preview positioning handled automatically
- Can be implemented incrementally

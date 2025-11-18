# High-Level Approaches for Expanding Block Types

## Current State Analysis
The current implementation has blocks individually hardcoded:
- Each block type is a separate class (LBlock, JBlock, IBlock, etc.)
- Blocks are manually listed in arrays: `[IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]`
- Next block drawing has hardcoded checks: `if self.next_block.id == 3:` and `elif self.next_block.id == 4:`
- Each block manually defines rotation states and initial positions

---

## Approach 1: Registry Pattern with Block Configuration

### Overview
Create a centralized block registry that stores block configurations as data structures rather than individual classes. New blocks can be added by simply registering a configuration dictionary.

### Key Components:
1. **Block Registry**: A dictionary or class that stores all block definitions
   - Each entry contains: block ID, name, cell positions for each rotation, initial offset, color mapping
2. **Generic Block Class**: Replace individual block classes with a single `Block` class that takes configuration
3. **Block Factory**: A method that creates blocks from registry entries
4. **Metadata System**: Store block-specific metadata (draw offset, special properties) in the registry

### Implementation Flow:
- Register blocks: `BlockRegistry.register("LBlock", {...config...})`
- Create blocks: `BlockRegistry.create("LBlock")` or `BlockRegistry.create_random()`
- Drawing offsets stored in registry metadata instead of hardcoded checks

### Benefits:
- Adding new blocks = adding one dictionary entry
- No need to create new classes
- Centralized configuration makes it easy to see all blocks
- Easy to load blocks from external files (JSON/YAML)

### Example Structure:
```python
BLOCK_REGISTRY = {
    "LBlock": {
        "id": 1,
        "cells": {0: [...], 1: [...], 2: [...], 3: [...]},
        "initial_offset": (0, 3),
        "draw_offset": (270, 270),
        "color_id": 1
    },
    # Add new blocks here...
}
```

---

## Approach 2: Plugin-Based Architecture with Base Block Class

### Overview
Keep the class-based structure but make it extensible through a base class with required methods and a plugin registration system. New block types inherit from a base class and register themselves.

### Key Components:
1. **Abstract Base Block Class**: Defines interface that all blocks must implement
   - Required methods: `get_cells()`, `get_initial_offset()`, `get_draw_offset()`, `get_id()`
2. **Block Plugin Registry**: Blocks register themselves on import/initialization
3. **Factory Method**: Creates blocks from registered types
4. **Metadata Interface**: Blocks provide their own metadata through methods

### Implementation Flow:
- New block classes inherit from `BaseBlock` and implement required methods
- Blocks auto-register on class definition or explicit registration
- Factory uses registry to create instances: `BlockFactory.create_all_types()` or `BlockFactory.create_by_name("LBlock")`
- Drawing logic queries block for its offset instead of checking IDs

### Benefits:
- Maintains OOP structure (good for complex block behaviors)
- Easy to add special behaviors per block type
- Type safety through inheritance
- Blocks can have custom logic if needed

### Example Structure:
```python
class BaseBlock:
    def get_cells(self): raise NotImplementedError
    def get_initial_offset(self): raise NotImplementedError
    def get_draw_offset(self): raise NotImplementedError
    
class LBlock(BaseBlock):
    def get_cells(self): return {...}
    # Auto-registers on definition

BlockFactory.get_all_types()  # Returns all registered blocks
```

---

## Approach 3: Data-Driven Configuration with Block Descriptors

### Overview
Separate block data (shapes, rotations) from block behavior (movement, drawing). Use descriptor objects that define blocks declaratively, with a unified system for rendering and positioning.

### Key Components:
1. **Block Descriptor Class**: Data class that holds all block information
   - Shape definitions, rotation states, metadata
2. **Block Manager**: Centralized manager that handles all block operations
   - Creation, rotation, drawing, positioning
3. **Configuration File/Module**: External definition of all blocks
4. **Unified Drawing System**: Calculates draw positions algorithmically based on block properties (size, shape) rather than hardcoded values

### Implementation Flow:
- Define blocks as descriptor objects: `BlockDescriptor(name="LBlock", id=1, shapes=[...], ...)`
- BlockManager loads all descriptors and provides access
- Drawing system calculates offsets based on block bounding box or metadata
- New blocks = new descriptor definition

### Benefits:
- Complete separation of data and logic
- Very easy to add blocks (just data)
- Can support loading from external files
- Drawing logic becomes generic (no special cases)
- Easy to test and modify block data

### Example Structure:
```python
@dataclass
class BlockDescriptor:
    name: str
    id: int
    rotation_states: Dict[int, List[Position]]
    initial_offset: Tuple[int, int]
    # Drawing calculated from bounding box or explicit metadata

block_descriptors = [
    BlockDescriptor("LBlock", 1, {...}, (0, 3)),
    # Add new blocks...
]

BlockManager.load_descriptors(block_descriptors)
```

---

## Comparison Summary

| Aspect | Registry Pattern | Plugin Architecture | Data-Driven Descriptors |
|--------|-----------------|-------------------|------------------------|
| **Ease of Adding Blocks** | Very Easy (dict entry) | Easy (new class) | Very Easy (descriptor) |
| **Code Complexity** | Low | Medium | Low-Medium |
| **Flexibility** | Medium | High (custom logic) | Medium |
| **Maintainability** | High | Medium-High | High |
| **Type Safety** | Low | High | Medium |
| **External Config** | Easy | Medium | Very Easy |

---

## Recommendation
For this Tetris game, **Approach 1 (Registry Pattern)** or **Approach 3 (Data-Driven)** would be most suitable as they minimize code changes and make adding blocks trivial. Approach 2 is better if you anticipate needing custom behaviors per block type in the future.

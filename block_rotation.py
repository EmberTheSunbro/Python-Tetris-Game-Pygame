"""
Block rotation utilities - generates rotation states programmatically
"""
from position import Position

def rotate_positions_90_clockwise(positions):
	"""
	Rotate a list of positions 90 degrees clockwise around their geometric center.
	
	Uses the transpose-and-reverse method for 90° clockwise rotation:
	1. Convert positions to a grid representation
	2. Transpose the grid (swap row and col)
	3. Reverse each row (for clockwise rotation)
	4. Convert back to position list
	
	This method preserves the exact shape of the block.
	
	Args:
		positions: List of Position objects representing a block shape
		
	Returns:
		List of Position objects representing the rotated shape, normalized to start from (0,0)
	"""
	if not positions:
		return []
	
	# Create a copy of positions to avoid modifying the original
	positions = [Position(p.row, p.column) for p in positions]
	
	# Find bounding box
	min_row = min(p.row for p in positions)
	max_row = max(p.row for p in positions)
	min_col = min(p.column for p in positions)
	max_col = max(p.column for p in positions)
	
	width = max_col - min_col + 1
	height = max_row - min_row + 1
	
	# Create a grid representation (2D list)
	# Initialize grid with False (empty)
	grid = [[False for _ in range(width)] for _ in range(height)]
	
	# Mark positions as True (filled)
	for pos in positions:
		grid_row = pos.row - min_row
		grid_col = pos.column - min_col
		grid[grid_row][grid_col] = True
	
	# Rotate 90° clockwise: transpose then reverse each row
	# Transpose: swap dimensions (height x width -> width x height)
	transposed = [[grid[row][col] for row in range(height)] for col in range(width)]
	
	# Reverse each row for clockwise rotation
	rotated_grid = [row[::-1] for row in transposed]
	
	# Convert rotated grid back to position list
	rotated = []
	new_height = len(rotated_grid)
	new_width = len(rotated_grid[0]) if rotated_grid else 0
	
	for row in range(new_height):
		for col in range(new_width):
			if rotated_grid[row][col]:
				rotated.append(Position(row, col))
	
	# Result is already normalized (starts from 0,0)
	return rotated

def normalize_shape(positions):
	"""
	Normalize a shape to start from (0, 0).
	
	Args:
		positions: List of Position objects
		
	Returns:
		Normalized list of Position objects starting from (0, 0)
	"""
	if not positions:
		return []
	
	min_row = min(p.row for p in positions)
	min_col = min(p.column for p in positions)
	return [Position(p.row - min_row, p.column - min_col) for p in positions]

def generate_rotation_states(base_shape, max_rotations=4):
	"""
	Generate all rotation states from a base shape.
	
	Args:
		base_shape: List of Position objects representing the base shape (rotation state 0)
		max_rotations: Maximum number of rotation states to generate (default 4)
		
	Returns:
		Dictionary mapping rotation state (0, 1, 2, 3) to list of Position objects
	"""
	# Create a deep copy of the base shape and normalize it
	normalized_base = normalize_shape([Position(p.row, p.column) for p in base_shape])
	rotation_states = {0: normalized_base}
	
	current_shape = normalized_base
	for rotation in range(1, max_rotations):
		# Create a fresh copy of current_shape for rotation
		shape_copy = [Position(p.row, p.column) for p in current_shape]
		
		# Rotate the shape copy
		rotated = rotate_positions_90_clockwise(shape_copy)
		
		# Validate that rotated positions are reasonable (not way off the grid)
		# Check if any position has very large coordinates (likely an error)
		max_coord = max(max(abs(p.row), abs(p.column)) for p in rotated) if rotated else 0
		if max_coord > 20:  # Sanity check - blocks shouldn't be this large
			raise ValueError(f"Rotation produced invalid coordinates: {rotated}")
		
		# Check if this rotation is the same as a previous one (for symmetric blocks)
		# Compare by converting to sorted tuples for comparison
		def shape_to_key(shape):
			return tuple(sorted((p.row, p.column) for p in shape))
		
		current_key = shape_to_key(rotated)
		# Check if we've seen this shape before
		seen_before = False
		for prev_state in range(rotation):
			if shape_to_key(rotation_states[prev_state]) == current_key:
				seen_before = True
				break
		
		if seen_before:
			# This rotation repeats a previous one, stop generating
			break
		
		# Store a fresh copy of the rotated shape
		rotation_states[rotation] = [Position(p.row, p.column) for p in rotated]
		current_shape = rotation_states[rotation]
	
	return rotation_states

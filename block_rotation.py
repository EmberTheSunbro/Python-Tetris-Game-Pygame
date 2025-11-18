"""
Block rotation utilities - generates rotation states programmatically
"""
from position import Position

def rotate_positions_90_clockwise(positions):
	"""
	Rotate a list of positions 90 degrees clockwise around their geometric center.
	
	In a grid coordinate system where:
	- row increases downward (positive = down)
	- col increases rightward (positive = right)
	
	90° clockwise rotation: (row, col) -> (col, -row) relative to origin
	But we need to account for the fact that -row means "up" in our system.
	
	The rotation is performed around the center of the bounding box,
	then the result is normalized to start from (0, 0).
	
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
	
	# Calculate center of bounding box
	# Use floating point for precision, then round
	center_row = (min_row + max_row) / 2.0
	center_col = (min_col + max_col) / 2.0
	
	# Rotate each position 90 degrees clockwise around the center
	# For 90° clockwise: translate to origin, rotate, translate back
	# Rotation formula: (row, col) -> (col, -row) around origin
	rotated = []
	for pos in positions:
		# Translate to center-origin coordinates
		rel_row = float(pos.row) - center_row
		rel_col = float(pos.column) - center_col
		
		# Apply 90° clockwise rotation: (row, col) -> (col, -row)
		# This means: new_row = old_col, new_col = -old_row
		new_rel_row = rel_col
		new_rel_col = -rel_row
		
		# Translate back from center
		new_row = center_row + new_rel_row
		new_col = center_col + new_rel_col
		
		# Round to nearest integer
		rotated.append(Position(int(round(new_row)), int(round(new_col))))
	
	# Normalize to start from (0, 0) by finding the new minimum
	if rotated:
		min_rot_row = min(p.row for p in rotated)
		min_rot_col = min(p.column for p in rotated)
		normalized = [Position(p.row - min_rot_row, p.column - min_rot_col) for p in rotated]
	else:
		normalized = []
	
	return normalized

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

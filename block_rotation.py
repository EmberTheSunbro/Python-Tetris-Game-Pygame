"""
Block rotation utilities - generates rotation states programmatically
"""
from position import Position

def rotate_positions_90_clockwise(positions):
	"""
	Rotate a list of positions 90 degrees clockwise around their center.
	
	Args:
		positions: List of Position objects representing a block shape
		
	Returns:
		List of Position objects representing the rotated shape, normalized to start from (0,0)
	"""
	if not positions:
		return []
	
	# Find bounding box
	min_row = min(p.row for p in positions)
	max_row = max(p.row for p in positions)
	min_col = min(p.column for p in positions)
	max_col = max(p.column for p in positions)
	
	# Calculate center (use center of bounding box)
	# For integer coordinates, use the midpoint
	center_row = (min_row + max_row) / 2.0
	center_col = (min_col + max_col) / 2.0
	
	# Rotate each position 90 degrees clockwise around center
	# Formula for 90° clockwise: (row, col) -> (col, -row) relative to origin
	# Around center: translate to origin, rotate, translate back
	rotated = []
	for pos in positions:
		# Translate to center-origin coordinates
		rel_row = pos.row - center_row
		rel_col = pos.column - center_col
		
		# Rotate 90 degrees clockwise: (row, col) -> (col, -row)
		new_rel_row = rel_col
		new_rel_col = -rel_row
		
		# Translate back and round to nearest integer
		new_row = int(round(center_row + new_rel_row))
		new_col = int(round(center_col + new_rel_col))
		
		rotated.append(Position(new_row, new_col))
	
	# Normalize to start from (0,0) by finding minimum and shifting
	min_rot_row = min(p.row for p in rotated)
	min_rot_col = min(p.column for p in rotated)
	normalized = [Position(p.row - min_rot_row, p.column - min_rot_col) for p in rotated]
	
	return normalized

def generate_rotation_states(base_shape, max_rotations=4):
	"""
	Generate all rotation states from a base shape.
	
	Args:
		base_shape: List of Position objects representing the base shape (rotation state 0)
		max_rotations: Maximum number of rotation states to generate (default 4)
		
	Returns:
		Dictionary mapping rotation state (0, 1, 2, 3) to list of Position objects
	"""
	rotation_states = {0: base_shape}
	
	current_shape = base_shape
	for rotation in range(1, max_rotations):
		# Rotate the current shape
		rotated = rotate_positions_90_clockwise(current_shape)
		
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
		
		rotation_states[rotation] = rotated
		current_shape = rotated
	
	return rotation_states

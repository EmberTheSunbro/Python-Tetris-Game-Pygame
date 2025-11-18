"""
Block rotation utilities - generates rotation states programmatically
"""
from position import Position

def rotate_positions_90_clockwise(positions):
	"""
	Rotate a list of positions 90 degrees clockwise around their geometric center.
	
	Uses proper rotation matrix mathematics:
	For 90° clockwise rotation: (x, y) -> (y, -x)
	In grid coordinates (row, col): (row, col) -> (col, -row)
	
	The rotation is performed around the center of the bounding box,
	then the result is normalized to start from (0, 0).
	
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
	
	# Calculate center of bounding box
	# Center can be half-integer for even-sized blocks (e.g., 2x2 block has center at 0.5, 0.5)
	center_row = (min_row + max_row) / 2.0
	center_col = (min_col + max_col) / 2.0
	
	# Rotate each position 90 degrees clockwise around the center
	# Rotation matrix for 90° clockwise: [0  1]   [x]   [y]
	#                                    [-1 0] * [y] = [-x]
	# In grid coords: (row, col) -> (col, -row) relative to origin
	rotated = []
	for pos in positions:
		# Step 1: Translate to center-origin coordinates
		rel_row = pos.row - center_row
		rel_col = pos.column - center_col
		
		# Step 2: Apply 90° clockwise rotation matrix
		# (row, col) -> (col, -row)
		new_rel_row = rel_col
		new_rel_col = -rel_row
		
		# Step 3: Translate back from center
		new_row = center_row + new_rel_row
		new_col = center_col + new_rel_col
		
		# Step 4: Round to nearest integer (grid positions must be integers)
		rotated.append(Position(int(round(new_row)), int(round(new_col))))
	
	# Step 5: Normalize to start from (0, 0) by finding the new minimum
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

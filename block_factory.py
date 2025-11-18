"""
Block Factory - Creates block instances from configuration
"""
from block import Block
from block_config import BLOCKS, get_block_config
from block_rotation import generate_rotation_states

class BlockFactory:
	"""Factory class for creating blocks from configuration"""
	
	@staticmethod
	def create_block(block_key):
		"""
		Create a block instance from configuration
		
		Args:
			block_key: String key identifying the block (e.g., "L", "I", "O")
		
		Returns:
			Block instance configured according to the block_key
		"""
		config = get_block_config(block_key)
		if not config:
			raise ValueError(f"Unknown block key: {block_key}")
		
		# Create block with ID from config
		block = Block(config["id"])
		
		# Generate rotation states from base_shape
		base_shape = config["base_shape"]
		rotation_states = generate_rotation_states(base_shape, max_rotations=4)
		
		# Set cells with generated rotation states
		block.cells = rotation_states
		
		# Apply initial offset
		row_offset, col_offset = config["initial_offset"]
		block.move(row_offset, col_offset)
		
		return block
	
	@staticmethod
	def create_all_blocks():
		"""
		Create instances of all blocks defined in configuration
		
		Returns:
			List of Block instances
		"""
		return [BlockFactory.create_block(key) for key in BLOCKS.keys()]
	
	@staticmethod
	def get_block_keys():
		"""Returns list of all available block keys"""
		return list(BLOCKS.keys())

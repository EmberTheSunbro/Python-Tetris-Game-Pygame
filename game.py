from grid import Grid
from blocks import *
import random
import pygame
import time

class Game:
	def __init__(self):
		self.grid = Grid()
		self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		self.current_block = self.get_random_block()
		self.next_block = self.get_random_block()
		self.game_over = False
		self.score = 0
		self.difficulty = 1.0  # Default difficulty multiplier (1.0 = normal)
		self.game_start_time = time.time()
		self.rotate_sound = pygame.mixer.Sound("Sounds/rotate.ogg")
		self.clear_sound = pygame.mixer.Sound("Sounds/clear.ogg")

		pygame.mixer.music.load("Sounds/music.ogg")
		pygame.mixer.music.play(-1)
	
	def set_difficulty(self, difficulty):
		"""Set difficulty multiplier (0.5 to 2.0)"""
		self.difficulty = max(0.5, min(2.0, difficulty))
	
	def get_speed_multiplier(self):
		"""Calculate speed multiplier based on difficulty and elapsed time"""
		elapsed_time = time.time() - self.game_start_time
		# Base speed increases over time, multiplied by difficulty
		# At difficulty 1.0, speed increases by 0.1 every 10 seconds
		time_based_speed = 1.0 + (elapsed_time / 100.0)  # Gradual increase
		return time_based_speed * self.difficulty
	
	def get_score_multiplier(self):
		"""Get score multiplier based on difficulty"""
		return self.difficulty

	def update_score(self, lines_cleared, move_down_points):
		score_multiplier = self.get_score_multiplier()
		if lines_cleared == 1:
			self.score += int(100 * score_multiplier)
		elif lines_cleared == 2:
			self.score += int(300 * score_multiplier)
		elif lines_cleared == 3:
			self.score += int(500 * score_multiplier)
		self.score += int(move_down_points * score_multiplier)

	def get_random_block(self):
		if len(self.blocks) == 0:
			self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		block = random.choice(self.blocks)
		self.blocks.remove(block)
		return block

	def move_left(self):
		self.current_block.move(0, -1)
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(0, 1)

	def move_right(self):
		self.current_block.move(0, 1)
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(0, -1)

	def move_down(self):
		self.current_block.move(1, 0)
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(-1, 0)
			self.lock_block()

	def lock_block(self):
		tiles = self.current_block.get_cell_positions()
		for position in tiles:
			self.grid.grid[position.row][position.column] = self.current_block.id
		self.current_block = self.next_block
		self.next_block = self.get_random_block()
		rows_cleared = self.grid.clear_full_rows()
		if rows_cleared > 0:
			self.clear_sound.play()
			self.update_score(rows_cleared, 0)
		if self.block_fits() == False:
			self.game_over = True

	def reset(self):
		self.grid.reset()
		self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		self.current_block = self.get_random_block()
		self.next_block = self.get_random_block()
		self.score = 0
		self.game_start_time = time.time()

	def block_fits(self):
		tiles = self.current_block.get_cell_positions()
		for tile in tiles:
			if self.grid.is_empty(tile.row, tile.column) == False:
				return False
		return True

	def rotate(self):
		self.current_block.rotate()
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.undo_rotation()
		else:
			self.rotate_sound.play()

	def block_inside(self):
		tiles = self.current_block.get_cell_positions()
		for tile in tiles:
			if self.grid.is_inside(tile.row, tile.column) == False:
				return False
		return True

	def draw(self, screen):
		self.grid.draw(screen)
		self.current_block.draw(screen, 11, 11)

		if self.next_block.id == 3:
			self.next_block.draw(screen, 255, 290)
		elif self.next_block.id == 4:
			self.next_block.draw(screen, 255, 280)
		else:
			self.next_block.draw(screen, 270, 270)
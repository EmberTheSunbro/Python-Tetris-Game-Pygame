import pygame
from colors import Colors

class Grid:
	def __init__(self):
		self.num_rows = 20
		self.num_cols = 10
		self.cell_size = 30
		self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
		self.colors = Colors.get_cell_colors()

	def print_grid(self):
		for row in range(self.num_rows):
			for column in range(self.num_cols):
				print(self.grid[row][column], end = " ")
			print()

	def is_inside(self, row, column):
		if row >= 0 and row < self.num_rows and column >= 0 and column < self.num_cols:
			return True
		return False

	def is_empty(self, row, column):
		if self.grid[row][column] == 0:
			return True
		return False

	def is_row_full(self, row):
		for column in range(self.num_cols):
			if self.grid[row][column] == 0:
				return False
		return True

	def clear_row(self, row):
		for column in range(self.num_cols):
			self.grid[row][column] = 0

	def move_row_down(self, row, num_rows):
		for column in range(self.num_cols):
			self.grid[row+num_rows][column] = self.grid[row][column]
			self.grid[row][column] = 0

	def clear_full_rows(self):
		"""
		Clear all full rows and move remaining rows down.
		Returns the number of rows cleared.
		"""
		completed = 0
		
		# Use a two-pointer approach: read from top, write to bottom
		# This ensures we don't overwrite data we haven't read yet
		write_row = self.num_rows - 1  # Start writing at the bottom
		
		# Scan from bottom to top, compacting non-full rows
		for read_row in range(self.num_rows - 1, -1, -1):
			if self.is_row_full(read_row):
				# This row is full, clear it and don't write it
				self.clear_row(read_row)
				completed += 1
			else:
				# This row is not full, keep it
				if read_row != write_row:
					# Copy the row to the write position
					for col in range(self.num_cols):
						self.grid[write_row][col] = self.grid[read_row][col]
					# Clear the source row
					self.clear_row(read_row)
				write_row -= 1
		
		# Clear any rows above the write pointer (these are now empty)
		for row in range(write_row, -1, -1):
			self.clear_row(row)
		
		return completed

	def reset(self):
		for row in range(self.num_rows):
			for column in range(self.num_cols):
				self.grid[row][column] = 0

	def draw(self, screen):
		for row in range(self.num_rows):
			for column in range(self.num_cols):
				cell_value = self.grid[row][column]
				cell_rect = pygame.Rect(column*self.cell_size + 11, row*self.cell_size + 11,
				self.cell_size -1, self.cell_size -1)
				pygame.draw.rect(screen, self.colors[cell_value], cell_rect)

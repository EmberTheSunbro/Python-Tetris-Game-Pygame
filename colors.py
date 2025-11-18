class Colors:
	dark_grey = (26, 31, 40)
	green = (47, 230, 23)
	red = (232, 18, 18)
	orange = (226, 116, 17)
	yellow = (237, 234, 4)
	purple = (166, 0, 247)
	cyan = (21, 204, 209)
	blue = (13, 64, 216)
	white = (255, 255, 255)
	dark_blue = (44, 44, 127)
	light_blue = (59, 85, 162)
	pink = (255, 105, 180)
	lime = (191, 255, 0)
	teal = (0, 128, 128)
	maroon = (128, 0, 0)
	navy = (0, 0, 128)

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
			cls.pink,       # 8 - Plus block
			cls.lime,       # 9 - U block
			cls.teal,       # 10 - X block
			cls.maroon,     # 11 - Line 3 block
			cls.navy        # 12 - Long L block
		]

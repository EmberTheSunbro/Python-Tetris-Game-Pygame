import pygame,sys
from game import Game
from colors import Colors

pygame.init()

title_font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 24)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
difficulty_surface = title_font.render("Difficulty", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)

score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)
difficulty_rect = pygame.Rect(320, 405, 170, 60)
slider_rect = pygame.Rect(330, 440, 150, 20)

screen = pygame.display.set_mode((500, 680))
pygame.display.set_caption("Python Tetris")

clock = pygame.time.Clock()

game = Game()

GAME_UPDATE = pygame.USEREVENT
base_update_interval = 200  # Base interval in milliseconds
pygame.time.set_timer(GAME_UPDATE, base_update_interval)

# Difficulty slider state
difficulty_value = 1.0  # Range: 0.5 to 2.0
slider_dragging = False
game.set_difficulty(difficulty_value)

def update_game_speed():
	"""Update game timer based on current speed multiplier"""
	speed_multiplier = game.get_speed_multiplier()
	# Higher speed multiplier = faster updates = lower interval
	new_interval = max(50, int(base_update_interval / speed_multiplier))
	pygame.time.set_timer(GAME_UPDATE, new_interval)

def get_slider_value_from_pos(x):
	"""Convert mouse x position to difficulty value"""
	min_x = slider_rect.left
	max_x = slider_rect.right
	normalized = max(0, min(1, (x - min_x) / (max_x - min_x)))
	return 0.5 + normalized * 1.5  # Range: 0.5 to 2.0

def get_slider_pos_from_value(value):
	"""Convert difficulty value to slider position"""
	normalized = (value - 0.5) / 1.5  # Normalize to 0-1
	return slider_rect.left + normalized * (slider_rect.width - 20)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if game.game_over == True:
				game.game_over = False
				game.reset()
				difficulty_value = 1.0
				game.set_difficulty(difficulty_value)
			if event.key == pygame.K_LEFT and game.game_over == False:
				game.move_left()
			if event.key == pygame.K_RIGHT and game.game_over == False:
				game.move_right()
			if event.key == pygame.K_DOWN and game.game_over == False:
				game.move_down()
				game.update_score(0, 1)
			if event.key == pygame.K_UP and game.game_over == False:
				game.rotate()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if slider_rect.collidepoint(event.pos) and not game.game_over:
				slider_dragging = True
				difficulty_value = get_slider_value_from_pos(event.pos[0])
				game.set_difficulty(difficulty_value)
				update_game_speed()
		if event.type == pygame.MOUSEBUTTONUP:
			slider_dragging = False
		if event.type == pygame.MOUSEMOTION:
			if slider_dragging and not game.game_over:
				difficulty_value = get_slider_value_from_pos(event.pos[0])
				game.set_difficulty(difficulty_value)
				update_game_speed()
		if event.type == GAME_UPDATE and game.game_over == False:
			game.move_down()
			update_game_speed()

	#Drawing
	score_value_surface = title_font.render(str(game.score), True, Colors.white)
	difficulty_text = f"{difficulty_value:.1f}x"
	difficulty_value_surface = small_font.render(difficulty_text, True, Colors.white)

	screen.fill(Colors.dark_blue)
	screen.blit(score_surface, (365, 20, 50, 50))
	screen.blit(next_surface, (375, 180, 50, 50))
	screen.blit(difficulty_surface, (350, 410, 50, 50))

	if game.game_over == True:
		screen.blit(game_over_surface, (320, 510, 50, 50))

	pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
	screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, 
		centery = score_rect.centery))
	pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
	
	# Draw difficulty slider
	pygame.draw.rect(screen, Colors.light_blue, difficulty_rect, 0, 10)
	pygame.draw.rect(screen, Colors.dark_grey, slider_rect, 0, 10)
	slider_handle_x = get_slider_pos_from_value(difficulty_value)
	slider_handle = pygame.Rect(slider_handle_x, slider_rect.top, 20, slider_rect.height)
	pygame.draw.rect(screen, Colors.white, slider_handle, 0, 5)
	screen.blit(difficulty_value_surface, difficulty_value_surface.get_rect(centerx = difficulty_rect.centerx, 
		centery = difficulty_rect.centery - 15))
	
	game.draw(screen)

	pygame.display.update()
	clock.tick(60)
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
difficulty_rect = pygame.Rect(320, 410, 170, 80)

screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Python Tetris")

clock = pygame.time.Clock()

game = Game()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)

# Difficulty slider state
slider_dragging = False
slider_min = 0.5
slider_max = 2.0
slider_x_min = difficulty_rect.x + 10
slider_x_max = difficulty_rect.x + difficulty_rect.width - 10
slider_handle_width = 20
last_speed_update = pygame.time.get_ticks()

def update_game_speed():
	"""Update the game timer based on current speed"""
	current_speed = game.get_current_speed()
	pygame.time.set_timer(GAME_UPDATE, current_speed)

update_game_speed()

while True:
	# Periodically update game speed (every 100ms to avoid constant timer resets)
	current_time = pygame.time.get_ticks()
	if current_time - last_speed_update > 100:
		update_game_speed()
		last_speed_update = current_time
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if game.game_over == True:
				game.game_over = False
				game.reset()
				update_game_speed()  # Reset speed timer on game reset
			if event.key == pygame.K_LEFT and game.game_over == False:
				game.move_left()
			if event.key == pygame.K_RIGHT and game.game_over == False:
				game.move_right()
			if event.key == pygame.K_DOWN and game.game_over == False:
				game.move_down()
				game.update_score(0, 1)
			if event.key == pygame.K_UP and game.game_over == False:
				game.rotate()
		if event.type == GAME_UPDATE and game.game_over == False:
			game.move_down()
		
		# Handle slider mouse events
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:  # Left mouse button
				mouse_x, mouse_y = event.pos
				# Check if clicking on slider track or handle
				slider_track_y = difficulty_rect.y + 40
				if (difficulty_rect.collidepoint(mouse_x, mouse_y) or 
					abs(mouse_y - slider_track_y) < 15):
					slider_dragging = True
		if event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				slider_dragging = False
		if event.type == pygame.MOUSEMOTION:
			if slider_dragging:
				mouse_x, mouse_y = event.pos
				# Convert mouse X position to difficulty value
				clamped_x = max(slider_x_min, min(slider_x_max, mouse_x))
				# Normalize to 0-1 range
				normalized = (clamped_x - slider_x_min) / (slider_x_max - slider_x_min)
				# Convert to difficulty range
				difficulty_value = slider_min + normalized * (slider_max - slider_min)
				game.set_difficulty(difficulty_value)
				update_game_speed()  # Update speed immediately when difficulty changes

	#Drawing
	score_value_surface = title_font.render(str(game.score), True, Colors.white)

	screen.fill(Colors.dark_blue)
	screen.blit(score_surface, (365, 20, 50, 50))
	screen.blit(next_surface, (375, 180, 50, 50))
	screen.blit(difficulty_surface, (350, 415, 50, 50))

	if game.game_over == True:
		screen.blit(game_over_surface, (320, 450, 50, 50))

	pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
	screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, 
		centery = score_rect.centery))
	pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
	
	# Draw difficulty slider
	pygame.draw.rect(screen, Colors.light_blue, difficulty_rect, 0, 10)
	
	# Draw slider track
	slider_track_y = difficulty_rect.y + 40
	pygame.draw.line(screen, Colors.dark_grey, 
		(slider_x_min, slider_track_y), 
		(slider_x_max, slider_track_y), 4)
	
	# Calculate handle position based on current difficulty
	difficulty_normalized = (game.difficulty - slider_min) / (slider_max - slider_min)
	handle_x = slider_x_min + difficulty_normalized * (slider_x_max - slider_x_min)
	handle_rect = pygame.Rect(handle_x - slider_handle_width // 2, 
		slider_track_y - 8, slider_handle_width, 16)
	pygame.draw.rect(screen, Colors.white, handle_rect, 0, 3)
	
	# Draw difficulty value
	difficulty_text = f"{game.difficulty:.1f}x"
	difficulty_value_surface = small_font.render(difficulty_text, True, Colors.white)
	screen.blit(difficulty_value_surface, 
		(difficulty_rect.x + 10, difficulty_rect.y + 55))
	
	game.draw(screen)

	pygame.display.update()
	clock.tick(60)
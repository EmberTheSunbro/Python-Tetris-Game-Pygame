import pygame,sys
from game import Game
from colors import Colors

pygame.init()

title_font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 24)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)
difficulty_surface = small_font.render("Difficulty", True, Colors.white)

score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)
difficulty_rect = pygame.Rect(320, 410, 170, 60)
slider_rect = pygame.Rect(330, 450, 150, 20)
slider_handle_rect = pygame.Rect(330, 450, 10, 20)

screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Python Tetris")

clock = pygame.time.Clock()

game = Game()

GAME_UPDATE = pygame.USEREVENT
current_speed = 200
pygame.time.set_timer(GAME_UPDATE, current_speed)

# Difficulty slider state
difficulty_value = 1.0  # Range: 0.5 to 2.0
slider_dragging = False

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if game.game_over == True:
				game.game_over = False
				game.reset()
				current_speed = 200
				pygame.time.set_timer(GAME_UPDATE, current_speed)
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
			# Update timer based on current speed
			new_speed = game.get_current_speed()
			if new_speed != current_speed:
				current_speed = new_speed
				pygame.time.set_timer(GAME_UPDATE, current_speed)
		
		# Handle slider interaction
		if event.type == pygame.MOUSEBUTTONDOWN:
			if slider_handle_rect.collidepoint(event.pos) or slider_rect.collidepoint(event.pos):
				slider_dragging = True
		if event.type == pygame.MOUSEBUTTONUP:
			slider_dragging = False
		if event.type == pygame.MOUSEMOTION and slider_dragging:
			# Calculate difficulty based on mouse x position
			mouse_x = max(slider_rect.left, min(slider_rect.right, event.pos[0]))
			# Map slider position to difficulty range (0.5 to 2.0)
			normalized = (mouse_x - slider_rect.left) / slider_rect.width
			difficulty_value = 0.5 + normalized * 1.5
			game.set_difficulty(difficulty_value)

	#Drawing
	score_value_surface = title_font.render(str(game.score), True, Colors.white)
	difficulty_value_surface = small_font.render(f"{difficulty_value:.2f}x", True, Colors.white)

	screen.fill(Colors.dark_blue)
	screen.blit(score_surface, (365, 20, 50, 50))
	screen.blit(next_surface, (375, 180, 50, 50))
	screen.blit(difficulty_surface, (365, 380, 50, 50))

	if game.game_over == True:
		screen.blit(game_over_surface, (320, 480, 50, 50))

	pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
	screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, 
		centery = score_rect.centery))
	pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
	
	# Draw difficulty slider
	pygame.draw.rect(screen, Colors.light_blue, difficulty_rect, 0, 10)
	screen.blit(difficulty_value_surface, difficulty_value_surface.get_rect(centerx = difficulty_rect.centerx, 
		centery = difficulty_rect.centery - 15))
	
	# Draw slider track
	pygame.draw.rect(screen, Colors.dark_grey, slider_rect, 0, 5)
	
	# Calculate slider handle position based on difficulty
	normalized = (difficulty_value - 0.5) / 1.5
	handle_x = slider_rect.left + int(normalized * (slider_rect.width - slider_handle_rect.width))
	slider_handle_rect.x = handle_x
	
	# Draw slider handle
	pygame.draw.rect(screen, Colors.white, slider_handle_rect, 0, 5)
	
	game.draw(screen)

	pygame.display.update()
	clock.tick(60)
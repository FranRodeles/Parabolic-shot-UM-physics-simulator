"""
Visualización básica con pygame (día 4).
"""

import pygame


def run_basic_animation(ideal_positions: list[tuple[float, float]], wind_positions: list[tuple[float, float]]) -> None:
	pygame.init()
	width, height = 800, 500
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption("Día 4 - Animación básica")
	clock = pygame.time.Clock()

	max_x = max(max(p[0] for p in ideal_positions), max(p[0] for p in wind_positions), 1.0)
	max_y = max(max(p[1] for p in ideal_positions), max(p[1] for p in wind_positions), 1.0)
	margin = 40
	scale_x = (width - 2 * margin) / max_x
	scale_y = (height - 2 * margin) / max_y

	def to_screen(p: tuple[float, float]) -> tuple[int, int]:
		x = int(margin + p[0] * scale_x)
		y = int(height - margin - p[1] * scale_y)
		return x, y

	idx = 0
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		screen.fill((30, 30, 30))
		pygame.draw.line(screen, (120, 120, 120), (margin, height - margin), (width - margin, height - margin), 2)
		pygame.draw.line(screen, (120, 120, 120), (margin, height - margin), (margin, margin), 2)

		idx_ideal = min(idx, len(ideal_positions) - 1)
		idx_wind = min(idx, len(wind_positions) - 1)

		for i in range(1, idx_ideal + 1):
			pygame.draw.line(screen, (0, 200, 255), to_screen(ideal_positions[i - 1]), to_screen(ideal_positions[i]), 2)
		for i in range(1, idx_wind + 1):
			pygame.draw.line(screen, (255, 150, 0), to_screen(wind_positions[i - 1]), to_screen(wind_positions[i]), 2)

		pygame.draw.circle(screen, (0, 200, 255), to_screen(ideal_positions[idx_ideal]), 6)
		pygame.draw.circle(screen, (255, 150, 0), to_screen(wind_positions[idx_wind]), 6)

		pygame.display.flip()
		clock.tick(60)

		idx += 1
		if idx >= max(len(ideal_positions), len(wind_positions)):
			idx = max(len(ideal_positions), len(wind_positions)) - 1

	pygame.quit()

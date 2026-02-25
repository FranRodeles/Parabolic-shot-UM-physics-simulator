from pathlib import Path

import numpy as np
import pygame

from simulation.simulator import SimulationResult


def _load_background_image(width: int, height: int) -> pygame.Surface | None:
	image_path = Path(__file__).resolve().parents[1] / "assets" / "background.png"
	if not image_path.exists():
		return None
	image = pygame.image.load(str(image_path)).convert()
	return pygame.transform.scale(image, (width, height))


def _draw_background(screen: pygame.Surface, width: int, height: int, background_image: pygame.Surface | None) -> None:
	if background_image is not None:
		screen.blit(background_image, (0, 0))
		return

	sky_top = (20, 30, 60)
	sky_bottom = (80, 120, 200)
	for y in range(height):
		ratio = y / max(height - 1, 1)
		color = (
			int(sky_top[0] + ratio * (sky_bottom[0] - sky_top[0])),
			int(sky_top[1] + ratio * (sky_bottom[1] - sky_top[1])),
			int(sky_top[2] + ratio * (sky_bottom[2] - sky_top[2])),
		)
		pygame.draw.line(screen, color, (0, y), (width, y))

	ground_height = int(height * 0.18)
	pygame.draw.rect(screen, (35, 90, 50), (0, height - ground_height, width, ground_height))


def run_pygame_animation(result_ideal: SimulationResult, result_wind: SimulationResult) -> None:
	pygame.init()
	info = pygame.display.Info()
	width, height = info.current_w, info.current_h
	screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
	pygame.display.set_caption("Tiro parabólico - pygame")
	clock = pygame.time.Clock()
	font = pygame.font.SysFont("arial", 18)

	background_image = _load_background_image(width, height)

	max_x = max(result_ideal.position_m[:, 0].max(), result_wind.position_m[:, 0].max())
	max_y = max(result_ideal.position_m[:, 1].max(), result_wind.position_m[:, 1].max())
	margin = 60
	scale_x = (width - 2 * margin) / max(max_x, 1.0)
	scale_y = (height - 2 * margin) / max(max_y, 1.0)

	def to_screen(point: np.ndarray) -> tuple[int, int]:
		x = int(margin + point[0] * scale_x)
		y = int(height - margin - point[1] * scale_y)
		return x, y

	idx = 0
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		_draw_background(screen, width, height, background_image)
		pygame.draw.line(screen, (100, 100, 100), (margin, height - margin), (width - margin, height - margin), 2)
		pygame.draw.line(screen, (100, 100, 100), (margin, height - margin), (margin, margin), 2)

		idx_ideal = min(idx, len(result_ideal.position_m) - 1)
		idx_wind = min(idx, len(result_wind.position_m) - 1)

		for i in range(1, idx_ideal + 1):
			pygame.draw.line(screen, (0, 200, 255), to_screen(result_ideal.position_m[i - 1]), to_screen(result_ideal.position_m[i]), 2)
		for i in range(1, idx_wind + 1):
			pygame.draw.line(screen, (255, 150, 0), to_screen(result_wind.position_m[i - 1]), to_screen(result_wind.position_m[i]), 2)

		pygame.draw.circle(screen, (0, 200, 255), to_screen(result_ideal.position_m[idx_ideal]), 6)
		pygame.draw.circle(screen, (255, 150, 0), to_screen(result_wind.position_m[idx_wind]), 6)

		label_ideal_pos = to_screen(result_ideal.position_m[idx_ideal])
		label_wind_pos = to_screen(result_wind.position_m[idx_wind])
		label_ideal = font.render("Ideal", True, (0, 200, 255))
		label_wind = font.render("Con viento", True, (255, 150, 0))
		screen.blit(label_ideal, (label_ideal_pos[0] + 8, label_ideal_pos[1] - 18))
		screen.blit(label_wind, (label_wind_pos[0] + 8, label_wind_pos[1] - 18))

		pygame.display.flip()
		clock.tick(60)

		idx += 1
		if idx >= max(len(result_ideal.position_m), len(result_wind.position_m)):
			idx = max(len(result_ideal.position_m), len(result_wind.position_m)) - 1

	pygame.quit()

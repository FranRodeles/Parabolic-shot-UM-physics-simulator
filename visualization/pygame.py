"""
Visualización del tiro parabólico.

Primero se utiliza pygame para la animación en tiempo real.
Al finalizar el recorrido y presionar la tecla 'm', se cierran las ventanas
de pygame y luego se muestran los gráficos con matplotlib.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable

import numpy as np
import pygame
import matplotlib.pyplot as plt

from simulation.simulator import SimulationResult


SimulateFn = Callable[[float, float, float, float, float, np.ndarray], tuple[SimulationResult, SimulationResult]]


def _load_background_image(width: int, height: int) -> pygame.Surface | None:
	"""
	Intenta cargar un fondo desde assets/background.png.

	La imagen es opcional: si no existe, se usa un fondo generado por código.
	"""

	image_path = Path(__file__).resolve().parents[1] / "assets" / "background.png"
	if not image_path.exists():
		return None

	image = pygame.image.load(str(image_path)).convert()
	return pygame.transform.scale(image, (width, height))


def _draw_background(
	screen: pygame.Surface,
	width: int,
	height: int,
	background_image: pygame.Surface | None,
) -> None:
	"""
	Dibuja un fondo sencillo con cielo y suelo, o una imagen si existe.

	El objetivo es que la visualización sea más clara y agradable.
	"""

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


def _draw_finish_instructions(
	screen: pygame.Surface,
	font: pygame.font.Font,
	result_ideal: SimulationResult,
	result_wind: SimulationResult,
	custom_ideal: SimulationResult | None,
	custom_wind: SimulationResult | None,
) -> None:
	"""
	Muestra instrucciones y distancias en la esquina superior izquierda.

	Las distancias salen de los resultados calculados por la simulación.
	"""

	text_lines = [
		"Animación finalizada",
		"R para reiniciar",
		"M para análisis en matplotlib",
		"Q para salir sin análisis",
		"E para editar parámetros",
	]

	distances = [
		f"Ideal base: {result_ideal.range_m:.2f} m",
		f"Viento base: {result_wind.range_m:.2f} m",
	]
	if custom_ideal is not None:
		distances.append(f"Ideal editado: {custom_ideal.range_m:.2f} m")
	if custom_wind is not None:
		distances.append(f"Viento editado: {custom_wind.range_m:.2f} m")
	y = 10
	for line in text_lines:
		text_surface = font.render(line, True, (255, 255, 255))
		screen.blit(text_surface, (10, y))
		y += 22

	y += 8
	for line in distances:
		text_surface = font.render(line, True, (255, 255, 0))
		screen.blit(text_surface, (10, y))
		y += 20


def _apply_edit_key(params: dict[str, float], key: int) -> None:
	"""
	Aplica cambios simples a los parámetros usando el teclado.

	Estos parámetros se usan para recalcular la simulación cuando el usuario
	presiona ENTER en el modo edición.
	"""

	if key == pygame.K_UP:
		params["initial_speed_m_s"] += 1.0
	if key == pygame.K_DOWN:
		params["initial_speed_m_s"] = max(0.0, params["initial_speed_m_s"] - 1.0)
	if key == pygame.K_RIGHT:
		params["launch_angle_deg"] = min(89.0, params["launch_angle_deg"] + 1.0)
	if key == pygame.K_LEFT:
		params["launch_angle_deg"] = max(1.0, params["launch_angle_deg"] - 1.0)

	if key == pygame.K_a:
		params["mass_kg"] = max(0.01, params["mass_kg"] + 0.01)
	if key == pygame.K_z:
		params["mass_kg"] = max(0.01, params["mass_kg"] - 0.01)

	if key == pygame.K_s:
		params["radius_m"] = max(0.005, params["radius_m"] + 0.001)
	if key == pygame.K_x:
		params["radius_m"] = max(0.005, params["radius_m"] - 0.001)

	if key == pygame.K_d:
		params["drag_coefficient"] = max(0.05, params["drag_coefficient"] + 0.01)
	if key == pygame.K_c:
		params["drag_coefficient"] = max(0.05, params["drag_coefficient"] - 0.01)

	if key == pygame.K_f:
		params["wind_x_m_s"] += 0.5
	if key == pygame.K_v:
		params["wind_x_m_s"] -= 0.5
	if key == pygame.K_g:
		params["wind_y_m_s"] += 0.5
	if key == pygame.K_b:
		params["wind_y_m_s"] -= 0.5


def _draw_edit_overlay(screen: pygame.Surface, font: pygame.font.Font, params: dict[str, float]) -> None:
	"""
	Muestra los parámetros editables y los controles asociados.

	La información se dibuja dentro de pygame para que el usuario sepa qué toca.
	"""

	panel = pygame.Surface((360, 210))
	panel.set_alpha(190)
	panel.fill((10, 10, 10))
	screen.blit(panel, (10, 120))

	lines = [
		"Modo edición",
		f"Velocidad (UP/DOWN): {params['initial_speed_m_s']:.1f} m/s",
		f"Ángulo (LEFT/RIGHT): {params['launch_angle_deg']:.1f}°",
		f"Masa (A/Z): {params['mass_kg']:.2f} kg",
		f"Radio (S/X): {params['radius_m']:.3f} m",
		f"Cd (D/C): {params['drag_coefficient']:.2f}",
		f"Viento X (F/V): {params['wind_x_m_s']:.1f} m/s",
		f"Viento Y (G/B): {params['wind_y_m_s']:.1f} m/s",
		"ENTER para simular con nuevos parámetros",
	]

	y = 130
	for line in lines:
		screen.blit(font.render(line, True, (255, 255, 255)), (20, y))
		y += 20


def run_pygame_animation(
	result_ideal: SimulationResult,
	result_wind: SimulationResult,
	simulate_fn: SimulateFn,
	editable_params: dict[str, float],
) -> tuple[
	bool,
	SimulationResult,
	SimulationResult,
	SimulationResult | None,
	SimulationResult | None,
	dict[str, float],
]:
	"""
	Muestra la animación del movimiento con pygame.

	- result_ideal y result_wind vienen de la simulación base.
	- simulate_fn es una función que recalcula la simulación si se editan parámetros.
	- editable_params es el diccionario que se edita en pantalla.

	Devuelve si se debe abrir matplotlib y, si hubo edición, los resultados nuevos.
	"""

	pygame.init()
	info = pygame.display.Info()
	width, height = info.current_w, info.current_h
	screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
	pygame.display.set_caption("Tiro parabólico - animación")
	clock = pygame.time.Clock()
	font = pygame.font.SysFont("arial", 18)

	background_image = _load_background_image(width, height)

	idx = 0
	running = True
	show_matplotlib = False
	animation_finished = False
	edit_mode = False
	custom_ideal: SimulationResult | None = None
	custom_wind: SimulationResult | None = None

	margin = 60

	def compute_bounds() -> tuple[float, float]:
		max_x = max(result_ideal.position_m[:, 0].max(), result_wind.position_m[:, 0].max())
		max_y = max(result_ideal.position_m[:, 1].max(), result_wind.position_m[:, 1].max())
		if custom_ideal is not None:
			max_x = max(max_x, custom_ideal.position_m[:, 0].max())
			max_y = max(max_y, custom_ideal.position_m[:, 1].max())
		if custom_wind is not None:
			max_x = max(max_x, custom_wind.position_m[:, 0].max())
			max_y = max(max_y, custom_wind.position_m[:, 1].max())
		return max_x, max_y

	max_x, max_y = compute_bounds()

	def compute_scale() -> tuple[float, float]:
		scale_x = (width - 2 * margin) / max(max_x, 1.0)
		scale_y = (height - 2 * margin) / max(max_y, 1.0)
		return scale_x, scale_y

	scale_x, scale_y = compute_scale()

	def to_screen(point: np.ndarray) -> tuple[int, int]:
		x = int(margin + point[0] * scale_x)
		y = int(height - margin - point[1] * scale_y)
		return x, y

	def recalc_frames() -> int:
		frames = [len(result_ideal.time_s), len(result_wind.time_s)]
		if custom_ideal is not None:
			frames.append(len(custom_ideal.time_s))
		if custom_wind is not None:
			frames.append(len(custom_wind.time_s))
		return max(frames)

	total_frames = recalc_frames()

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

			if event.type == pygame.KEYDOWN:
				if animation_finished and event.key == pygame.K_r:
					idx = 0
					animation_finished = False
					edit_mode = False
				if animation_finished and event.key == pygame.K_m:
					show_matplotlib = True
					running = False
				if animation_finished and event.key == pygame.K_q:
					show_matplotlib = False
					running = False
				if animation_finished and event.key == pygame.K_e:
					edit_mode = not edit_mode

				if animation_finished and edit_mode:
					_apply_edit_key(editable_params, event.key)
					if event.key == pygame.K_RETURN:
						custom_ideal, custom_wind = simulate_fn(
							editable_params["mass_kg"],
							editable_params["radius_m"],
							editable_params["drag_coefficient"],
							editable_params["initial_speed_m_s"],
							editable_params["launch_angle_deg"],
							np.array([
								editable_params["wind_x_m_s"],
								editable_params["wind_y_m_s"],
							], dtype=float),
						)
						max_x, max_y = compute_bounds()
						scale_x, scale_y = compute_scale()
						total_frames = recalc_frames()
						idx = 0
						animation_finished = False
						edit_mode = False

		_draw_background(screen, width, height, background_image)

		# Ejes simples
		pygame.draw.line(screen, (100, 100, 100), (margin, height - margin), (width - margin, height - margin), 2)
		pygame.draw.line(screen, (100, 100, 100), (margin, height - margin), (margin, margin), 2)

		idx_ideal = min(idx, len(result_ideal.position_m) - 1)
		idx_wind = min(idx, len(result_wind.position_m) - 1)

		# Trayectoria ideal
		for i in range(1, idx_ideal + 1):
			pygame.draw.line(
				screen,
				(0, 200, 255),
				to_screen(result_ideal.position_m[i - 1]),
				to_screen(result_ideal.position_m[i]),
				2,
			)

		# Trayectoria con viento
		for i in range(1, idx_wind + 1):
			pygame.draw.line(
				screen,
				(255, 150, 0),
				to_screen(result_wind.position_m[i - 1]),
				to_screen(result_wind.position_m[i]),
				2,
			)

		if custom_ideal is not None:
			idx_custom_ideal = min(idx, len(custom_ideal.position_m) - 1)
			for i in range(1, idx_custom_ideal + 1):
				pygame.draw.line(
					screen,
					(0, 220, 120),
					to_screen(custom_ideal.position_m[i - 1]),
					to_screen(custom_ideal.position_m[i]),
					2,
				)
		if custom_wind is not None:
			idx_custom_wind = min(idx, len(custom_wind.position_m) - 1)
			for i in range(1, idx_custom_wind + 1):
				pygame.draw.line(
					screen,
					(180, 120, 255),
					to_screen(custom_wind.position_m[i - 1]),
					to_screen(custom_wind.position_m[i]),
					2,
				)

		pygame.draw.circle(screen, (0, 200, 255), to_screen(result_ideal.position_m[idx_ideal]), 6)
		pygame.draw.circle(screen, (255, 150, 0), to_screen(result_wind.position_m[idx_wind]), 6)
		if custom_ideal is not None:
			pygame.draw.circle(
				screen,
				(0, 220, 120),
				to_screen(custom_ideal.position_m[min(idx, len(custom_ideal.position_m) - 1)]),
				6,
			)
		if custom_wind is not None:
			pygame.draw.circle(
				screen,
				(180, 120, 255),
				to_screen(custom_wind.position_m[min(idx, len(custom_wind.position_m) - 1)]),
				6,
			)

		label_ideal_pos = to_screen(result_ideal.position_m[idx_ideal])
		label_wind_pos = to_screen(result_wind.position_m[idx_wind])
		label_ideal = font.render("Ideal base", True, (0, 200, 255))
		label_wind = font.render("Viento base", True, (255, 150, 0))
		screen.blit(label_ideal, (label_ideal_pos[0] + 8, label_ideal_pos[1] - 18))
		screen.blit(label_wind, (label_wind_pos[0] + 8, label_wind_pos[1] - 18))

		if custom_ideal is not None:
			pos = to_screen(custom_ideal.position_m[min(idx, len(custom_ideal.position_m) - 1)])
			label = font.render("Ideal editado", True, (0, 220, 120))
			screen.blit(label, (pos[0] + 8, pos[1] - 18))
		if custom_wind is not None:
			pos = to_screen(custom_wind.position_m[min(idx, len(custom_wind.position_m) - 1)])
			label = font.render("Viento editado", True, (180, 120, 255))
			screen.blit(label, (pos[0] + 8, pos[1] - 18))

		if animation_finished:
			_draw_finish_instructions(
				screen,
				font,
				result_ideal,
				result_wind,
				custom_ideal,
				custom_wind,
			)
			if edit_mode:
				_draw_edit_overlay(screen, font, editable_params)

		pygame.display.flip()
		clock.tick(60)

		if not animation_finished:
			idx += 1
			if idx >= total_frames:
				idx = total_frames - 1
				animation_finished = True

		if animation_finished:
			clock.tick(30)
			continue

	pygame.quit()

	return (
		show_matplotlib,
		result_ideal,
		result_wind,
		custom_ideal,
		custom_wind,
		editable_params,
	)


def plot_trajectories(
	result_ideal: SimulationResult,
	result_wind: SimulationResult,
	custom_ideal: SimulationResult | None = None,
	custom_wind: SimulationResult | None = None,
) -> None:
	"""
	Grafica las trayectorias del tiro ideal y con viento.

	Si existen resultados editados, también se grafican para comparar.
	"""

	plt.figure(figsize=(8, 5))
	plt.plot(result_ideal.position_m[:, 0], result_ideal.position_m[:, 1], label="Ideal base")
	plt.plot(result_wind.position_m[:, 0], result_wind.position_m[:, 1], label="Viento base")
	if custom_ideal is not None:
		plt.plot(custom_ideal.position_m[:, 0], custom_ideal.position_m[:, 1], label="Ideal editado")
	if custom_wind is not None:
		plt.plot(custom_wind.position_m[:, 0], custom_wind.position_m[:, 1], label="Viento editado")
	plt.xlabel("x (m)")
	plt.ylabel("y (m)")
	plt.title("Trayectoria del proyectil")
	plt.legend()
	plt.grid(True, linestyle="--", alpha=0.5)

	_add_landing_annotation(result_ideal, "Ideal base", 0)
	_add_landing_annotation(result_wind, "Viento base", 1)
	if custom_ideal is not None:
		_add_landing_annotation(custom_ideal, "Ideal editado", 2)
	if custom_wind is not None:
		_add_landing_annotation(custom_wind, "Viento editado", 3)


def plot_speed(
	result_ideal: SimulationResult,
	result_wind: SimulationResult,
	custom_ideal: SimulationResult | None = None,
	custom_wind: SimulationResult | None = None,
) -> None:
	"""
	Grafica la rapidez del proyectil en función del tiempo.

	Permite comparar los casos base y los editados.
	"""

	speed_ideal = np.linalg.norm(result_ideal.velocity_m_s, axis=1)
	speed_wind = np.linalg.norm(result_wind.velocity_m_s, axis=1)
	speed_custom_ideal = None
	speed_custom_wind = None
	if custom_ideal is not None:
		speed_custom_ideal = np.linalg.norm(custom_ideal.velocity_m_s, axis=1)
	if custom_wind is not None:
		speed_custom_wind = np.linalg.norm(custom_wind.velocity_m_s, axis=1)

	plt.figure(figsize=(8, 5))
	plt.plot(result_ideal.time_s, speed_ideal, label="Ideal base")
	plt.plot(result_wind.time_s, speed_wind, label="Viento base")
	if speed_custom_ideal is not None and custom_ideal is not None:
		plt.plot(custom_ideal.time_s, speed_custom_ideal, label="Ideal editado")
	if speed_custom_wind is not None and custom_wind is not None:
		plt.plot(custom_wind.time_s, speed_custom_wind, label="Viento editado")
	plt.xlabel("t (s)")
	plt.ylabel("rapidez (m/s)")
	plt.title("Rapidez en función del tiempo")
	plt.legend()
	plt.grid(True, linestyle="--", alpha=0.5)


def plot_acceleration(
	result_ideal: SimulationResult,
	result_wind: SimulationResult,
	custom_ideal: SimulationResult | None = None,
	custom_wind: SimulationResult | None = None,
) -> None:
	"""
	Grafica la magnitud de la aceleración en función del tiempo.

	Permite comparar los casos base y los editados.
	"""

	acc_ideal = np.linalg.norm(result_ideal.acceleration_m_s2, axis=1)
	acc_wind = np.linalg.norm(result_wind.acceleration_m_s2, axis=1)
	acc_custom_ideal = None
	acc_custom_wind = None
	if custom_ideal is not None:
		acc_custom_ideal = np.linalg.norm(custom_ideal.acceleration_m_s2, axis=1)
	if custom_wind is not None:
		acc_custom_wind = np.linalg.norm(custom_wind.acceleration_m_s2, axis=1)

	plt.figure(figsize=(8, 5))
	plt.plot(result_ideal.time_s, acc_ideal, label="Ideal base")
	plt.plot(result_wind.time_s, acc_wind, label="Viento base")
	if acc_custom_ideal is not None and custom_ideal is not None:
		plt.plot(custom_ideal.time_s, acc_custom_ideal, label="Ideal editado")
	if acc_custom_wind is not None and custom_wind is not None:
		plt.plot(custom_wind.time_s, acc_custom_wind, label="Viento editado")
	plt.xlabel("t (s)")
	plt.ylabel("aceleración (m/s²)")
	plt.title("Aceleración en función del tiempo")
	plt.legend()
	plt.grid(True, linestyle="--", alpha=0.5)


def _add_landing_annotation(result: SimulationResult, label: str, index: int) -> None:
	"""
	Agrega el alcance final cerca del punto de caída.

	El índice se usa para separar los textos y evitar solapamientos.
	"""

	x = result.position_m[-1, 0]
	y = max(result.position_m[-1, 1], 0.0)
	plt.plot([x], [y], "o", color="black", markersize=4)
	offset_x = 6 + (index % 2) * 90
	offset_y = 10 + (index // 2) * 18
	plt.annotate(
		f"{label}: {x:.2f} m",
		xy=(x, y),
		xytext=(offset_x, offset_y),
		textcoords="offset points",
		fontsize=9,
		color="black",
	)

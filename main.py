"""
Punto de entrada del simulador de tiro parabólico.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from config.parameters import LAUNCH, PROJECTILE, SIMULATION
from physics.projectile import Projectile
from simulation.simulator import Simulator, SimulationResult
from visualization.pygame import (
	plot_acceleration,
	plot_speed,
	plot_trajectories,
	run_pygame_animation,
)


def build_projectile() -> Projectile:
	"""
	Construye el objeto Projectile a partir de los parámetros configurados.

	Los valores se leen desde config/parameters.py (masa, radio, coeficiente
	de arrastre y densidad del aire).
	"""
	return Projectile(
		mass_kg=PROJECTILE.mass_kg,
		radius_m=PROJECTILE.radius_m,
		drag_coefficient=PROJECTILE.drag_coefficient,
		air_density_kg_m3=PROJECTILE.air_density_kg_m3,
		area_m2=PROJECTILE.area_m2,
	)


def main() -> None:
	"""
	Ejecuta la simulación completa y genera gráficos.

	Flujo general:
	1) Toma parámetros iniciales definidos en config/parameters.py.
	2) Ejecuta la simulación base (ideal y con viento).
	3) Abre la animación en pygame.
	4) Si el usuario lo decide, abre los gráficos en matplotlib.
	"""

	initial_position = np.array(LAUNCH.initial_position_m, dtype=float)

	def simulate_with_params(
		mass_kg: float,
		radius_m: float,
		drag_coefficient: float,
		initial_speed_m_s: float,
		launch_angle_deg: float,
		wind_m_s: np.ndarray,
	) -> tuple[SimulationResult, SimulationResult]:
		"""
		Simula el tiro con parámetros que pueden venir del modo edición en pygame.

		- mass_kg, radius_m, drag_coefficient: parámetros físicos del proyectil.
		- initial_speed_m_s, launch_angle_deg: condiciones de lanzamiento.
		- wind_m_s: viento en x e y para el caso con resistencia.
		"""
		projectile = Projectile(
			mass_kg=mass_kg,
			radius_m=radius_m,
			drag_coefficient=drag_coefficient,
			air_density_kg_m3=PROJECTILE.air_density_kg_m3,
			area_m2=float(np.pi * radius_m**2),
		)
		simulator = Simulator(
			projectile=projectile,
			gravity_m_s2=SIMULATION.gravity_m_s2,
			time_step_s=SIMULATION.time_step_s,
			time_max_s=SIMULATION.time_max_s,
		)

		# Conversión de ángulo a radianes para construir el vector velocidad inicial.
		angle_rad = np.deg2rad(launch_angle_deg)
		initial_velocity = np.array(
			[
				initial_speed_m_s * np.cos(angle_rad),
				initial_speed_m_s * np.sin(angle_rad),
			],
			dtype=float,
		)

		result_ideal_local = simulator.run(
			initial_position_m=initial_position,
			initial_velocity_m_s=initial_velocity,
			include_drag=False,
		)

		result_wind_local = simulator.run(
			initial_position_m=initial_position,
			initial_velocity_m_s=initial_velocity,
			include_drag=True,
			wind_m_s=wind_m_s,
		)

		return result_ideal_local, result_wind_local

	# Copia de parámetros base que luego se pueden editar dentro de pygame.
	editable_params = {
		"mass_kg": PROJECTILE.mass_kg,
		"radius_m": PROJECTILE.radius_m,
		"drag_coefficient": PROJECTILE.drag_coefficient,
		"initial_speed_m_s": LAUNCH.initial_speed_m_s,
		"launch_angle_deg": LAUNCH.launch_angle_deg,
		"wind_x_m_s": SIMULATION.wind_m_s[0],
		"wind_y_m_s": SIMULATION.wind_m_s[1],
	}

	# Simulación inicial con los valores base del archivo de configuración.
	result_ideal, result_wind = simulate_with_params(
		editable_params["mass_kg"],
		editable_params["radius_m"],
		editable_params["drag_coefficient"],
		editable_params["initial_speed_m_s"],
		editable_params["launch_angle_deg"],
		np.array([editable_params["wind_x_m_s"], editable_params["wind_y_m_s"]], dtype=float),
	)

	print("Resultados sin rozamiento:")
	print(f"  Alcance: {result_ideal.range_m:.2f} m")
	print(f"  Altura máxima: {result_ideal.max_height_m:.2f} m")

	print("Resultados con viento:")
	print(f"  Alcance: {result_wind.range_m:.2f} m")
	print(f"  Altura máxima: {result_wind.max_height_m:.2f} m")

	(
		show_matplotlib,
		result_ideal,
		result_wind,
		custom_ideal,
		custom_wind,
		editable_params,
	) = run_pygame_animation(
		result_ideal,
		result_wind,
		simulate_with_params,
		editable_params,
	)

	# La animación devuelve si se desea abrir matplotlib y, si hubo edición,
	# también devuelve resultados nuevos.
	save_results(result_ideal, result_wind, editable_params)

	if show_matplotlib:
		plot_trajectories(result_ideal, result_wind, custom_ideal, custom_wind)
		plot_speed(result_ideal, result_wind, custom_ideal, custom_wind)
		plot_acceleration(result_ideal, result_wind, custom_ideal, custom_wind)

		import matplotlib.pyplot as plt

		plt.show()


def build_summary(result: SimulationResult) -> dict:
	"""
	Resume los datos principales para guardarlos en un archivo.

	Se usa dentro de save_results para escribir un JSON legible.
	"""

	flight_time = float(result.time_s[-1])
	final_speed = float(np.linalg.norm(result.velocity_m_s[-1]))

	return {
		"alcance_m": result.range_m,
		"altura_maxima_m": result.max_height_m,
		"tiempo_total_s": flight_time,
		"rapidez_final_m_s": final_speed,
	}


def save_results(
	result_ideal: SimulationResult,
	result_wind: SimulationResult,
	params: dict[str, float],
) -> None:
	"""
	Guarda un resumen de parámetros importantes de la simulación.

	Los parámetros provienen de config/parameters.py o de la edición en pygame.
	El archivo se crea en assets/simulation_results.json.
	"""

	output = {
		"parametros": {
			"masa_kg": params["mass_kg"],
			"radio_m": params["radius_m"],
			"coeficiente_arrastre": params["drag_coefficient"],
			"densidad_aire_kg_m3": PROJECTILE.air_density_kg_m3,
			"velocidad_inicial_m_s": params["initial_speed_m_s"],
			"angulo_inicial_deg": params["launch_angle_deg"],
			"posicion_inicial_m": LAUNCH.initial_position_m,
			"paso_tiempo_s": SIMULATION.time_step_s,
			"tiempo_max_s": SIMULATION.time_max_s,
			"gravedad_m_s2": SIMULATION.gravity_m_s2,
			"viento_m_s": [params["wind_x_m_s"], params["wind_y_m_s"]],
		},
		"ideal": build_summary(result_ideal),
		"con_viento": build_summary(result_wind),
	}

	output_path = Path(__file__).parent / "assets" / "simulation_results.json"
	output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
	main()

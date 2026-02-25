"""
Versión día 5 del proyecto.

Igual a la original pero sin gráficos de matplotlib.
"""

from __future__ import annotations

import numpy as np

from config.parameters import LAUNCH, PROJECTILE, SIMULATION
from physics.projectile import Projectile
from simulation.simulator import Simulator
from visualization.pygame import run_pygame_animation


def build_projectile() -> Projectile:
	return Projectile(
		mass_kg=PROJECTILE.mass_kg,
		radius_m=PROJECTILE.radius_m,
		drag_coefficient=PROJECTILE.drag_coefficient,
		air_density_kg_m3=PROJECTILE.air_density_kg_m3,
		area_m2=PROJECTILE.area_m2,
	)


def main() -> None:
	projectile = build_projectile()
	simulator = Simulator(
		projectile=projectile,
		gravity_m_s2=SIMULATION.gravity_m_s2,
		time_step_s=SIMULATION.time_step_s,
		time_max_s=SIMULATION.time_max_s,
	)

	initial_position = np.array(LAUNCH.initial_position_m, dtype=float)
	initial_velocity = LAUNCH.initial_velocity

	result_ideal = simulator.run(
		initial_position_m=initial_position,
		initial_velocity_m_s=initial_velocity,
		include_drag=False,
	)

	result_wind = simulator.run(
		initial_position_m=initial_position,
		initial_velocity_m_s=initial_velocity,
		include_drag=True,
		wind_m_s=np.array(SIMULATION.wind_m_s, dtype=float),
	)

	print("Resultados sin rozamiento:")
	print(f"  Alcance: {result_ideal.range_m:.2f} m")
	print(f"  Altura máxima: {result_ideal.max_height_m:.2f} m")

	print("Resultados con viento:")
	print(f"  Alcance: {result_wind.range_m:.2f} m")
	print(f"  Altura máxima: {result_wind.max_height_m:.2f} m")

	run_pygame_animation(result_ideal, result_wind)


if __name__ == "__main__":
	main()

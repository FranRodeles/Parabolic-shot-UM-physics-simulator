"""
Versión día 4 del proyecto.

Incluye una animación básica en pygame usando Euler y resistencia.
"""

from config.parameters import LAUNCH, PROJECTILE, SIMULATION
from simulation.simulator import simulate
from visualization.pygame import run_basic_animation


def main() -> None:
	ideal_positions = simulate(
		mass_kg=PROJECTILE["mass_kg"],
		radius_m=PROJECTILE["radius_m"],
		drag_coefficient=PROJECTILE["drag_coefficient"],
		air_density_kg_m3=PROJECTILE["air_density_kg_m3"],
		gravity_m_s2=SIMULATION["gravity_m_s2"],
		wind_x_m_s=0.0,
		wind_y_m_s=0.0,
		initial_speed_m_s=LAUNCH["initial_speed_m_s"],
		launch_angle_deg=LAUNCH["launch_angle_deg"],
		time_step_s=SIMULATION["time_step_s"],
		time_max_s=SIMULATION["time_max_s"],
		include_drag=True,
	)

	wind_positions = simulate(
		mass_kg=PROJECTILE["mass_kg"],
		radius_m=PROJECTILE["radius_m"],
		drag_coefficient=PROJECTILE["drag_coefficient"],
		air_density_kg_m3=PROJECTILE["air_density_kg_m3"],
		gravity_m_s2=SIMULATION["gravity_m_s2"],
		wind_x_m_s=SIMULATION["wind_m_s"][0],
		wind_y_m_s=SIMULATION["wind_m_s"][1],
		initial_speed_m_s=LAUNCH["initial_speed_m_s"],
		launch_angle_deg=LAUNCH["launch_angle_deg"],
		time_step_s=SIMULATION["time_step_s"],
		time_max_s=SIMULATION["time_max_s"],
		include_drag=True,
	)

	run_basic_animation(ideal_positions, wind_positions)


if __name__ == "__main__":
	main()

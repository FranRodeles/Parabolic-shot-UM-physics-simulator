"""
Simulación con Euler y resistencia del aire (día 3).
"""

from __future__ import annotations

import math

from numerics.euler import euler_step
from physics.mov_equations import state_derivative
from physics.projectile import area_from_radius


def simulate(
	mass_kg: float,
	radius_m: float,
	drag_coefficient: float,
	air_density_kg_m3: float,
	gravity_m_s2: float,
	wind_x_m_s: float,
	wind_y_m_s: float,
	initial_speed_m_s: float,
	launch_angle_deg: float,
	time_step_s: float,
	time_max_s: float,
	include_drag: bool,
) -> dict:
	"""
	Simula el movimiento con el método de Euler.
	Devuelve un resumen simple con alcance, altura máxima y tiempo de vuelo.
	"""

	angle_rad = math.radians(launch_angle_deg)
	vx0 = initial_speed_m_s * math.cos(angle_rad)
	vy0 = initial_speed_m_s * math.sin(angle_rad)

	state = [0.0, 0.0, vx0, vy0]
	area_m2 = area_from_radius(radius_m)

	max_height = state[1]
	t = 0.0

	def derivative(_t: float, st: list[float]) -> list[float]:
		return state_derivative(
			st,
			mass_kg,
			gravity_m_s2,
			air_density_kg_m3,
			drag_coefficient,
			area_m2,
			wind_x_m_s,
			wind_y_m_s,
			include_drag,
		)

	while t < time_max_s and state[1] >= 0.0:
		state = euler_step(derivative, t, state, time_step_s)
		t += time_step_s
		if state[1] > max_height:
			max_height = state[1]

	return {
		"alcance_m": state[0],
		"altura_max_m": max_height,
		"tiempo_s": t,
	}

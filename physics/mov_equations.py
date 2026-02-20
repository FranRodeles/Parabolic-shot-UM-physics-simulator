"""
Ecuaciones de movimiento para el día 3.
"""

from __future__ import annotations

from physics.forces import gravity_force, quadratic_drag_force


def state_derivative(
	state: list[float],
	mass_kg: float,
	gravity_m_s2: float,
	air_density_kg_m3: float,
	drag_coefficient: float,
	area_m2: float,
	wind_x_m_s: float,
	wind_y_m_s: float,
	include_drag: bool,
) -> list[float]:
	"""
	Devuelve la derivada temporal del estado [x, y, vx, vy].
	"""

	x, y, vx, vy = state

	fx, fy = gravity_force(mass_kg, gravity_m_s2)

	if include_drag:
		rel_vx = vx - wind_x_m_s
		rel_vy = vy - wind_y_m_s
		dfx, dfy = quadratic_drag_force(
			rel_vx,
			rel_vy,
			air_density_kg_m3,
			drag_coefficient,
			area_m2,
		)
		fx += dfx
		fy += dfy

	ax = fx / mass_kg
	ay = fy / mass_kg

	return [vx, vy, ax, ay]

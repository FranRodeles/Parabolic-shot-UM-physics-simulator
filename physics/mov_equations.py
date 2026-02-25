from __future__ import annotations

import numpy as np

from physics.forces import gravity_force, quadratic_drag_force
from physics.projectile import Projectile


def state_derivative(
	_t: float,
	state: np.ndarray,
	projectile: Projectile,
	gravity_m_s2: float,
	include_drag: bool,
	wind_m_s: np.ndarray | None,
) -> np.ndarray:
	x, y, vx, vy = state
	velocity = np.array([vx, vy], dtype=float)

	total_force = gravity_force(projectile.mass_kg, gravity_m_s2)
	if include_drag:
		relative_velocity = velocity
		if wind_m_s is not None:
			relative_velocity = velocity - wind_m_s
		total_force += quadratic_drag_force(
			relative_velocity,
			projectile.air_density_kg_m3,
			projectile.drag_coefficient,
			projectile.area_m2,
		)

	acceleration = total_force / projectile.mass_kg
	return np.array([vx, vy, acceleration[0], acceleration[1]], dtype=float)

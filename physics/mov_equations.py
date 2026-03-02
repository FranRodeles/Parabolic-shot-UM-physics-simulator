"""
Ecuaciones de movimiento para el tiro parabólico.

El estado del sistema se representa como:
	state = [x, y, vx, vy]
"""

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
	"""
	Devuelve la derivada temporal del estado.

	- state viene del integrador numérico y contiene [x, y, vx, vy].
	- projectile contiene las propiedades físicas del proyectil.
	- gravity_m_s2 sale de SIMULATION.gravity_m_s2.
	- include_drag indica si se calcula o no la resistencia del aire.
	- wind_m_s representa el viento y afecta la velocidad relativa del aire.
	"""

	x, y, vx, vy = state
	velocity = np.array([vx, vy], dtype=float)

	total_force = gravity_force(projectile.mass_kg, gravity_m_s2)

	if include_drag:
		relative_velocity = velocity
		if wind_m_s is not None:
			# El viento cambia la velocidad relativa del aire sobre el proyectil.
			relative_velocity = velocity - wind_m_s
		total_force += quadratic_drag_force(
			relative_velocity,
			projectile.air_density_kg_m3,
			projectile.drag_coefficient,
			projectile.area_m2,
		)

	acceleration = total_force / projectile.mass_kg

	return np.array([vx, vy, acceleration[0], acceleration[1]], dtype=float)

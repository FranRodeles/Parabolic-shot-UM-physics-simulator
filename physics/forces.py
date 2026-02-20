"""
Fuerzas para el día 3.
"""

from __future__ import annotations

import math


def gravity_force(mass_kg: float, gravity_m_s2: float) -> tuple[float, float]:
	"""
	Fuerza peso (hacia abajo).
	"""

	return (0.0, -mass_kg * gravity_m_s2)


def quadratic_drag_force(
	vx: float,
	vy: float,
	air_density_kg_m3: float,
	drag_coefficient: float,
	area_m2: float,
) -> tuple[float, float]:
	"""
	Fuerza de resistencia cuadrática del aire.
	"""

	speed = math.sqrt(vx * vx + vy * vy)
	if speed == 0.0:
		return (0.0, 0.0)

	magnitude = 0.5 * air_density_kg_m3 * drag_coefficient * area_m2 * speed * speed
	dir_x = -vx / speed
	dir_y = -vy / speed
	return (magnitude * dir_x, magnitude * dir_y)

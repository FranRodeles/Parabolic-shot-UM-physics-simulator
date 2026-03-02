"""
Funciones de fuerzas que actúan sobre el proyectil.
"""

from __future__ import annotations

import numpy as np


def gravity_force(mass_kg: float, gravity_m_s2: float) -> np.ndarray:
	"""
	Fuerza peso (vertical hacia abajo).

	- mass_kg sale del proyectil (config/parameters.py).
	- gravity_m_s2 sale de SIMULATION.gravity_m_s2.
	"""

	return np.array([0.0, -mass_kg * gravity_m_s2], dtype=float)


def quadratic_drag_force(
	velocity_m_s: np.ndarray,
	air_density_kg_m3: float,
	drag_coefficient: float,
	area_m2: float,
) -> np.ndarray:
	"""
	Fuerza de resistencia cuadrática del aire.

	Su magnitud es:
		F = 0.5 * rho * Cd * A * v^2
	y su dirección es opuesta a la velocidad.

	Los parámetros salen del proyectil y del aire definido en config/parameters.py.
	"""

	speed = float(np.linalg.norm(velocity_m_s))
	if speed == 0.0:
		return np.zeros(2, dtype=float)

	drag_magnitude = 0.5 * air_density_kg_m3 * drag_coefficient * area_m2 * speed**2
	drag_direction = -velocity_m_s / speed
	return drag_magnitude * drag_direction

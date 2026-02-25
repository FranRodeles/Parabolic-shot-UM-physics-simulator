from __future__ import annotations

import numpy as np


def gravity_force(mass_kg: float, gravity_m_s2: float) -> np.ndarray:
	return np.array([0.0, -mass_kg * gravity_m_s2], dtype=float)


def quadratic_drag_force(
	velocity_m_s: np.ndarray,
	air_density_kg_m3: float,
	drag_coefficient: float,
	area_m2: float,
) -> np.ndarray:
	speed = float(np.linalg.norm(velocity_m_s))
	if speed == 0.0:
		return np.zeros(2, dtype=float)
	drag_magnitude = 0.5 * air_density_kg_m3 * drag_coefficient * area_m2 * speed**2
	drag_direction = -velocity_m_s / speed
	return drag_magnitude * drag_direction
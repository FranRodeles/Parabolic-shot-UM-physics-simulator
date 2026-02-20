"""
Funciones auxiliares del proyectil para el día 3.
"""

import math


def area_from_radius(radius_m: float) -> float:
	"""
	Calcula el área frontal del proyectil usando su radio.
	"""

	return math.pi * radius_m * radius_m

"""
Clase que agrupa las propiedades físicas del proyectil.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Projectile:
	"""
	Contenedor de parámetros físicos del proyectil.

	Todos estos valores provienen de config/parameters.py.
	"""

	mass_kg: float           # masa del proyectil
	radius_m: float          # radio del proyectil
	drag_coefficient: float  # coeficiente de arrastre
	air_density_kg_m3: float # densidad del aire
	area_m2: float           # área frontal del proyectil
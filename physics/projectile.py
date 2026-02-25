
from dataclasses import dataclass


@dataclass(frozen=True)
class Projectile:
	mass_kg: float
	radius_m: float
	drag_coefficient: float
	air_density_kg_m3: float
	area_m2: float
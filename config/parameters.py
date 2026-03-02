"""
Parámetros globales del problema de tiro parabólico.

La idea es tener un único lugar donde ajustar valores físicos y numéricos
para que el resto del proyecto se mantenga limpio y fácil de leer.
"""

from dataclasses import dataclass

import numpy as np
from scipy.constants import g


@dataclass(frozen=True)
class ProjectileParams:
	"""
	Propiedades físicas del proyectil.

	Estos valores se usan para calcular fuerzas y aceleraciones.
	"""

	mass_kg: float
	radius_m: float
	drag_coefficient: float
	air_density_kg_m3: float

	@property
	def area_m2(self) -> float:
		"""
		Área frontal para el cálculo de la fuerza de arrastre.

		Sale del radio definido arriba y se usa en la fuerza de resistencia.
		"""

		return float(np.pi * self.radius_m**2)


@dataclass(frozen=True)
class LaunchParams:
	"""
	Condiciones iniciales del lanzamiento.

	Aquí se define cómo se lanza la pelota al inicio de la simulación.
	"""

	initial_speed_m_s: float
	launch_angle_deg: float
	initial_position_m: tuple[float, float]

	@property
	def initial_velocity(self) -> np.ndarray:
		"""
		Vector velocidad inicial en coordenadas cartesianas.

		Se calcula usando la velocidad y el ángulo definidos en este mismo bloque.
		"""

		angle_rad = np.deg2rad(self.launch_angle_deg)
		vx = self.initial_speed_m_s * np.cos(angle_rad)
		vy = self.initial_speed_m_s * np.sin(angle_rad)
		return np.array([vx, vy], dtype=float)


@dataclass(frozen=True)
class SimulationParams:
	"""
	Parámetros numéricos del integrador.

	Controlan el paso de tiempo, el tiempo máximo y el viento aplicado.
	"""

	time_step_s: float
	time_max_s: float
	gravity_m_s2: float
	wind_m_s: tuple[float, float]


# ---------------------------
# Valores por defecto
# ---------------------------

PROJECTILE = ProjectileParams(
	mass_kg=0.145,          # masa típica de una pelota de béisbol
	radius_m=0.0366,        # radio aproximado
	drag_coefficient=0.47,  # esfera en flujo turbulento
	air_density_kg_m3=1.225 # densidad del aire a nivel del mar
)

LAUNCH = LaunchParams(
	initial_speed_m_s=30.0,     # velocidad inicial
	launch_angle_deg=45.0,      # ángulo de lanzamiento
	initial_position_m=(0.0, 0.0) # punto de partida
)

SIMULATION = SimulationParams(
	time_step_s=0.01,            # tamaño del paso de integración
	time_max_s=10.0,             # tiempo máximo simulado
	gravity_m_s2=float(g),       # gravedad terrestre
	wind_m_s=(5.0, 0.0)          # viento en x e y
)

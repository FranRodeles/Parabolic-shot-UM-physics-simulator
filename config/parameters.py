import dataclass

import numpy as np
from scipy.constants import g


@dataclass(frozen=True)
class ProjectileParams:
	mass_kg: float
	radius_m: float
	drag_coefficient: float
	air_density_kg_m3: float

	@property
	def area_m2(self) -> float:
		return float(np.pi * self.radius_m**2)


@dataclass(frozen=True)
class LaunchParams:
	initial_speed_m_s: float
	launch_angle_deg: float
	initial_position_m: tuple[float, float]

	@property
	def initial_velocity(self) -> np.ndarray:
		angle_rad = np.deg2rad(self.launch_angle_deg)
		vx = self.initial_speed_m_s * np.cos(angle_rad)
		vy = self.initial_speed_m_s * np.sin(angle_rad)
		return np.array([vx, vy], dtype=float)


@dataclass(frozen=True)
class SimulationParams:
	time_step_s: float
	time_max_s: float
	gravity_m_s2: float
	wind_m_s: tuple[float, float]


PROJECTILE = ProjectileParams(
	mass_kg=0.145,
	radius_m=0.0366,
	drag_coefficient=0.47,
	air_density_kg_m3=1.225
)

LAUNCH = LaunchParams(
	initial_speed_m_s=30.0,
	launch_angle_deg=45.0,
	initial_position_m=(0.0, 0.0)
)

SIMULATION = SimulationParams(
	time_step_s=0.01,
	time_max_s=10.0,
	gravity_m_s2=float(g),
	wind_m_s=(5.0, 0.0)
)

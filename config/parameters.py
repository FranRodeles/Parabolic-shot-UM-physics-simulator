"""
Parámetros simples para la versión día 3.
"""

PROJECTILE = {
	"mass_kg": 0.145,
	"radius_m": 0.0366,
	"drag_coefficient": 0.47,
	"air_density_kg_m3": 1.225
}

LAUNCH = {
	"initial_speed_m_s": 30.0,
	"launch_angle_deg": 45.0,
	"initial_position_m": (0.0, 0.0)
}

SIMULATION = {
	"time_step_s": 0.02,
	"time_max_s": 10.0,
	"gravity_m_s2": 9.81,
	"wind_m_s": (5.0, 0.0)
}

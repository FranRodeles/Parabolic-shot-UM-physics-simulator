PROJECTILE = {
	"mass_kg": 0.145,          # masa típica de una pelota de béisbol
	"radius_m": 0.0366,        # radio aproximado
	"drag_coefficient": 0.47,  # coeficiente de arrastre
	"air_density_kg_m3": 1.225 # densidad del aire a nivel del mar
}

LAUNCH = {
	"initial_speed_m_s": 30.0,      # velocidad inicial
	"launch_angle_deg": 45.0,       # ángulo de lanzamiento
	"initial_position_m": (0.0, 0.0) # punto de partida
}

SIMULATION = {
	"time_step_s": 0.01,   # paso de tiempo
	"time_max_s": 10.0,    # tiempo máximo
	"gravity_m_s2": 9.81,  # gravedad aproximada
	"wind_m_s": (5.0, 0.0) # viento en x e y
}

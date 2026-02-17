
from __future__ import annotations

import math

from config.parameters import LAUNCH, SIMULATION

# Calculo de tiro ideal sin resistencia (altura maxima, tiempo de vuelo y alcance horizontal)
def compute_ideal_results(speed_m_s: float, angle_deg: float, gravity_m_s2: float) -> dict:

	angle_rad = math.radians(angle_deg)
	vx = speed_m_s * math.cos(angle_rad)
	vy = speed_m_s * math.sin(angle_rad)

	time_flight = 0.0
	if gravity_m_s2 > 0:
		time_flight = 2.0 * vy / gravity_m_s2

	max_height = 0.0
	if gravity_m_s2 > 0:
		max_height = (vy ** 2) / (2.0 * gravity_m_s2)

	range_m = vx * time_flight

	return {
		"tiempo_s": time_flight,
		"altura_max_m": max_height,
		"alcance_m": range_m,
	}

# Aproximación con viento constante en x
# Se usa el mismo tiempo de vuelo ideal y se ajusta la velocidad horizontal +sumando el viento
def compute_wind_results(
	speed_m_s: float,
	angle_deg: float,
	gravity_m_s2: float,
	wind_x_m_s: float,
) -> dict:

	angle_rad = math.radians(angle_deg)
	vx = speed_m_s * math.cos(angle_rad)
	vy = speed_m_s * math.sin(angle_rad)

	time_flight = 0.0
	if gravity_m_s2 > 0:
		time_flight = 2.0 * vy / gravity_m_s2

	vx_wind = vx + wind_x_m_s
	range_m = vx_wind * time_flight

	return {
		"tiempo_s": time_flight,
		"alcance_m": range_m,
	}

def main() -> None:

    print("\n[Proyectil]")
    print(f"Masa (kg): {PROJECTILE['mass_kg']}")
    print(f"Radio (m): {PROJECTILE['radius_m']}")
    print(f"Coef. arrastre: {PROJECTILE['drag_coefficient']}")
    print(f"Densidad aire (kg/m³): {PROJECTILE['air_density_kg_m3']}")

    print("\n[Lanzamiento]")
    print(f"Velocidad inicial (m/s): {LAUNCH['initial_speed_m_s']}")
    print(f"Ángulo (deg): {LAUNCH['launch_angle_deg']}")
    print(f"Posición inicial (m): {LAUNCH['initial_position_m']}")

    print("\n[Simulación]")
    print(f"Paso de tiempo (s): {SIMULATION['time_step_s']}")
    print(f"Tiempo máximo (s): {SIMULATION['time_max_s']}")
    print(f"Gravedad (m/s²): {SIMULATION['gravity_m_s2']}")
    print(f"Viento (m/s): {SIMULATION['wind_m_s']}")

    print("\nNota: los cálculos y la animación se agregan en etapas posteriores.")


if __name__ == "__main__":
    main()

from config.parameters import LAUNCH, PROJECTILE, SIMULATION

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

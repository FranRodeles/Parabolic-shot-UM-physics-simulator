"""
Conecta las ecuaciones físicas con el método numérico y genera los resultados.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from numerics.euler import rk4_step
from physics.mov_equations import state_derivative
from physics.projectile import Projectile


@dataclass(frozen=True)
class SimulationResult:
	"""
	Contenedor de resultados de la simulación.

	Se usa para pasar todos los datos a la visualización y al guardado en JSON.
	"""

	time_s: np.ndarray
	position_m: np.ndarray
	velocity_m_s: np.ndarray
	acceleration_m_s2: np.ndarray
	range_m: float
	max_height_m: float


class Simulator:
	"""
	Ejecuta la simulación de un tiro parabólico con o sin resistencia.

	Recibe el proyectil y los parámetros numéricos en el constructor.
	"""

	def __init__(
		self,
		projectile: Projectile,
		gravity_m_s2: float,
		time_step_s: float,
		time_max_s: float,
	) -> None:
		# Parámetros básicos de la simulación.
		self.projectile = projectile
		self.gravity_m_s2 = gravity_m_s2
		self.time_step_s = time_step_s
		self.time_max_s = time_max_s

	def run(
		self,
		initial_position_m: np.ndarray,
		initial_velocity_m_s: np.ndarray,
		include_drag: bool,
		wind_m_s: np.ndarray | None = None,
	) -> SimulationResult:
		"""
		Integra el movimiento hasta que el proyectil toca el suelo o se alcanza el tiempo máximo.

		- initial_position_m e initial_velocity_m_s vienen del lanzamiento.
		- include_drag define si se calcula la resistencia del aire.
		- wind_m_s afecta la resistencia cuando include_drag es True.
		"""

		state = np.array(
			[
				initial_position_m[0],
				initial_position_m[1],
				initial_velocity_m_s[0],
				initial_velocity_m_s[1],
			],
			dtype=float,
		)

		# Listas que guardan el historial para luego graficar.
		times = [0.0]
		states = [state.copy()]

		def derivative(t: float, current_state: np.ndarray) -> np.ndarray:
			return state_derivative(
				t,
				current_state,
				self.projectile,
				self.gravity_m_s2,
				include_drag,
				wind_m_s,
			)

		t = 0.0
		while t < self.time_max_s:
			next_state = rk4_step(derivative, t, state, self.time_step_s)
			t = t + self.time_step_s

			times.append(t)
			states.append(next_state.copy())

			state = next_state

			# Se corta cuando el proyectil cae por debajo del suelo (y < 0).
			if state[1] < 0.0 and t > 0.0:
				break

		data = np.array(states)
		time_s = np.array(times)
		position = data[:, 0:2]
		velocity = data[:, 2:4]

		# Calculamos la aceleración en cada punto usando la misma ecuación de movimiento.
		acceleration = np.zeros_like(velocity)
		for idx, (t_val, st) in enumerate(zip(time_s, data)):
			acc = derivative(t_val, st)[2:4]
			acceleration[idx] = acc

		range_m = float(position[-1, 0])
		max_height_m = float(position[:, 1].max())

		return SimulationResult(
			time_s=time_s,
			position_m=position,
			velocity_m_s=velocity,
			acceleration_m_s2=acceleration,
			range_m=range_m,
			max_height_m=max_height_m,
		)
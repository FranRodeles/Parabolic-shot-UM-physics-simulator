"""
Métodos numéricos para integrar ecuaciones diferenciales ordinarias.
"""

from __future__ import annotations

from typing import Callable

import numpy as np


DerivativeFunc = Callable[[float, np.ndarray], np.ndarray]


def euler_step(derivative: DerivativeFunc, t: float, state: np.ndarray, dt: float) -> np.ndarray:
	"""
	Un paso del método de Euler explícito.

	- derivative es la ecuación diferencial (estado -> derivada).
	- t es el tiempo actual.
	- state es el vector [x, y, vx, vy].
	- dt es el tamaño del paso de tiempo.
	"""

	return state + dt * derivative(t, state)


def rk4_step(derivative: DerivativeFunc, t: float, state: np.ndarray, dt: float) -> np.ndarray:
	"""
	Un paso del método clásico de Runge-Kutta de orden 4.

	Se usa en lugar de Euler porque es más preciso para el mismo paso de tiempo.
	"""

	k1 = derivative(t, state)
	k2 = derivative(t + 0.5 * dt, state + 0.5 * dt * k1)
	k3 = derivative(t + 0.5 * dt, state + 0.5 * dt * k2)
	k4 = derivative(t + dt, state + dt * k3)
	return state + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

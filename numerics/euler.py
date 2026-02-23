"""
Método de Euler explícito.
"""

from typing import Callable

DerivativeFunc = Callable[[float, list[float]], list[float]]


def euler_step(derivative: DerivativeFunc, t: float, state: list[float], dt: float) -> list[float]:
	dx = derivative(t, state)
	return [state[i] + dt * dx[i] for i in range(len(state))]

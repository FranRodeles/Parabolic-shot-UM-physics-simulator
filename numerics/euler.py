"""
Método de Euler explícito.
"""

from __future__ import annotations

from typing import Callable

import math

DerivativeFunc = Callable[[float, list[float]], list[float]]


def euler_step(derivative: DerivativeFunc, t: float, state: list[float], dt: float) -> list[float]:
	"""
	Un paso del método de Euler explícito.
	"""

	dx = derivative(t, state)
	return [state[i] + dt * dx[i] for i in range(len(state))]

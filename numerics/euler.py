from __future__ import annotations

from typing import Callable

import numpy as np

DerivativeFunc = Callable[[float, np.ndarray], np.ndarray]


def euler_step(derivative: DerivativeFunc, t: float, state: np.ndarray, dt: float) -> np.ndarray:
	return state + dt * derivative(t, state)


def rk4_step(derivative: DerivativeFunc, t: float, state: np.ndarray, dt: float) -> np.ndarray:
	k1 = derivative(t, state)
	k2 = derivative(t + 0.5 * dt, state + 0.5 * dt * k1)
	k3 = derivative(t + 0.5 * dt, state + 0.5 * dt * k2)
	k4 = derivative(t + dt, state + dt * k3)
	return state + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
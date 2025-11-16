import math
import numpy as np
from dataclasses import dataclass

from rocket import Rocket
from physics import Physics, Atmosphere

@dataclass
class EOM:
    """Base class for equations of motion"""
    rocket: Rocket
    atmos: Atmosphere
    phys: Physics

    def right_sides (self, t: float, state: np.ndarray) -> np.ndarray:

        v, gamma, h = state

        q = self.atmos.dynamic_pressure(v, h)
        beta = self.rocket.get_ballistic_coefficient()
        g = (self.phys.gravitational_acceleration(h))

        LoverD = self.rocket.get_L_over_D()

        v_dot = (- q / beta) + g * math.sin(gamma)

        gamma_dot = 1 / v * (
                - q / beta * LoverD
                + math.cos(gamma) * (g - v ** 2 / (self.phys.RE + h))
        )

        h_dot = - v * math.sin(gamma)

        return np.array([v_dot, gamma_dot, h_dot], dtype=float)
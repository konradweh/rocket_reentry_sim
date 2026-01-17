import math
import numpy as np
from dataclasses import dataclass

from vehicle import Vehicle
from physics import Physics, Atmosphere

@dataclass
class EOM:
    """Base class for equations of motion"""
    rocket: Vehicle
    atmos: Atmosphere
    phys: Physics

    @staticmethod
    def control_gain(gamma: float) -> float:
        """control law to avoid skip trajectories based on flight path angle gamma (radians)"""
        gamma_deg = math.degrees(gamma)

        if gamma_deg <= -5.0:
            return 1.0
        elif gamma_deg >= 0.0:
            return 0.0
        else:
            return -gamma_deg / 5.0  # linear interpolation between 0 and 1

    def right_sides (self, t: float, state: np.ndarray) -> np.ndarray:

        v, gamma, h = state

        q = self.atmos.dynamic_pressure(v, h)
        beta = self.rocket.get_ballistic_coefficient()
        g = (self.phys.gravitational_acceleration(h))

        # choose here to avoid or not avoid skip trajectories
        LoverD = self.control_gain(gamma) * self.rocket.get_L_over_D()  # effective L/D to avoid skip trajectories
        #LoverD = self.rocket.get_L_over_D()

        v_dot = (- q / beta) + g * math.sin(gamma)

        gamma_dot = 1 / v * (
                - q / beta * LoverD
                + math.cos(gamma) * (g - v ** 2 / (self.phys.RE + h))
        )

        h_dot = - v * math.sin(gamma)

        return np.array([v_dot, gamma_dot, h_dot], dtype=float)
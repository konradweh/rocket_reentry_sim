import math
from dataclasses import dataclass
from rocket import Rocket


@dataclass
class Atmosphere:
    """Class for calculating atmospheric properties based on altitude"""
    rho0: float = 1.2        # density at sea level (kg/m^3)
    k: float = -1.244268e-4  # exponential decay constant (1/m)

    def atmospheric_density(self, h: float) -> float:
        """calculates the atmospheric density (kg/m^3) depending on altitude h (m) using an exponential model"""
        return self.rho0 * math.exp(self.k * max(h, 0.0))   # clamp h to be non-negative

    def dynamic_pressure(self, v: float, h: float) -> float:
        """calculates the dynamic pressure (Pa) at altitude h (m) for velocity v (m/s)"""
        return self.atmospheric_density(h) * v ** 2 / 2

@dataclass
class Physics:
    """Class for various physics calculations related to rocket flight"""
    rocket: Rocket

    G: float = 6.67430e-11     # gravitational acceleration (m/s^2)
    RE: float = 6371000.0      # Earth's radius (m)
    ME: float = 5.9722e24      # Earth's mass (kg)

    def gravitational_acceleration(self, h: float) -> float:
        """calculates the gravitational acceleration (m/s^2) at altitude h (m)"""
        return self.G * self.ME / (self.RE + h) ** 2
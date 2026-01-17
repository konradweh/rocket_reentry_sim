import math
from dataclasses import dataclass

from vehicle import Vehicle
from physics import Physics, Atmosphere

@dataclass
class Thermo:
    """Thermal models for reentry: Sutton–Graves, radiative equilibrium, etc"""
    rocket: Vehicle
    atmos: Atmosphere
    phys: Physics

    k_sg: float = 1.74e-4       # Sutton–Graves constant for Earth reentry (SI units)
    sigma: float = 5.670374e-8  # Stefan-Boltzmann constant (W/m^2/K^4)
    emissivity: float = 0.8     # Emissivity of the vehicle surface

    def sutton_graves_heat_flux(self, h: float, u: float) -> float:
        """Calculates the Sutton–Graves convective heat flux q (W/m^2) at the nose of the vehicle"""
        rho = self.atmos.atmospheric_density(h)
        R = self.rocket.nose_radius
        heat_flux = self.k_sg * math.sqrt(rho / R) * (u ** 3)

        return heat_flux

    def adiabatic_wall_temperature_radiative(self, h: float, u: float, T_atmos = 273.15) -> float:
        """Calculates the adiabatic wall temperature (K) assuming radiative equilibrium with a constant background temperature of 0 °C"""
        T_wall = (self.sutton_graves_heat_flux(h, u) / (self.sigma * self.emissivity) + T_atmos ** 4) ** 0.25

        return T_wall
import math

g = 9.81  # gravitational acceleration (m/s^2)
RE = 6371000.0 # Earth's radius (m)

rho0 = 1.2  # density at sea level (kg/m^3)
k = -1.244268e-4  # exponential decay constant (1/m)

def rho(h):
    """
    calculates the atmospheric density depending on altitude h using an exponential model
    :param h: altitude (m)
    :return: density at altitude h (kg/m^3)
    """
    return rho0 * math.exp(-k * h)

def dynamic_pressure(v, h):
    """
    calculates the dynamic pressure at altitude h for velocity v
    :param v: velocity (m/s)
    :param h: altitude (m)
    :return: dynamic pressure (Pa)
    """
    return rho(h) * v ** 2 / 2
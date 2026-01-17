import math
import numpy as np
from scipy.integrate import solve_ivp

from vehicle import Vehicle
from physics import Atmosphere, Physics
from eom import EOM
from thermo import Thermo

def event_ground(t:float, state: np.ndarray):
    v, gamma, h = state
    return h   # becomes 0 at ground level

event_ground.terminal = True      # stops integration
event_ground.direction = -1       # only trigger when h is decreasing

def run_simulation_from_rocket(rocket: Vehicle,
                               t_max: float = 10000.0,
                               max_step: float = 0.5,
                               rtol: float = 1e-8,
                               atol: float = 1e-9):
    """Runs the atmospheric entry simulation using solve_ivp and returns the solution object"""

    atmos = Atmosphere()
    phys = Physics(rocket=rocket)
    thermo = Thermo(rocket=rocket, atmos=atmos, phys=phys)
    eom = EOM(rocket=rocket, atmos=atmos, phys=phys)

    v0 = rocket.initial_velocity
    gamma0 = math.radians(rocket.initial_angle)
    h0 = rocket.initial_altitude

    y0 = np.array([v0, gamma0, h0], dtype=float)

    solution = solve_ivp(
        fun=eom.right_sides,   # RHS: (t, state)
        t_span=(0, t_max),    # integration interval
        y0=y0,                 # initial state
        events=event_ground,   # event to stop at ground level
        max_step=max_step,
        rtol=rtol,
        atol=atol
    )

    return solution, thermo, rocket


def run_simulation(input_file: str,
                   t_max: float = 10000.0,
                   max_step: float = 0.5,
                   rtol: float = 1e-8,
                   atol: float = 1e-9):
    """Runs the atmospheric entry simulation using an input JSON file."""

    rocket = Vehicle.import_data(input_file)
    return run_simulation_from_rocket(
        rocket,
        t_max=t_max,
        max_step=max_step,
        rtol=rtol,
        atol=atol,
    )


def compute_thermal_histories(sol, thermo):
    """computes the thermal histories (heat flux and wall temperature) over time from the solution object"""
    t = sol.t
    v = sol.y[0]
    h = sol.y[2]

    q = np.array([thermo.sutton_graves_heat_flux(h_i, v_i) for h_i, v_i in zip(h, v)])
    T_wall = np.array([thermo.adiabatic_wall_temperature_radiative(h_i, v_i) for h_i, v_i in zip(h, v)])

    return t, q, T_wall
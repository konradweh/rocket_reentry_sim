import numpy as np
from scipy.integrate import solve_ivp

from rocket import Rocket
from physics import Atmosphere, Physics
from eom import EOM


def run_simulation(t_max: float = 1000.0,
                   max_step: float = 0.1,
                   rtol: float = 1e-8,
                   atol: float = 1e-9):
    """    Runs the atmospheric entry simulation using solve_ivp and returns the solution object"""

    rocket = Rocket.import_data("input.json")
    atmos = Atmosphere()
    phys = Physics(rocket=rocket)

    eom = EOM(rocket=rocket, atmos=atmos, phys=phys)

    v0 = rocket.initial_velocity
    gamma0 = rocket.initial_angle
    h0 = rocket.initial_altitude

    y0 = np.array([v0, gamma0, h0], dtype=float)

    solution = solve_ivp(
        fun=eom.right_sides,  # RHS: (t, state)
        t_span=(0, t_max),    # Integrationsintervall
        y0=y0,                # Anfangszustand
        max_step=max_step,
        rtol=rtol,
        atol=atol
    )

    return solution
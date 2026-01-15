import numpy as np
from numpy import ndarray
import json

from rocket import Rocket
from simulate import run_simulation, compute_thermal_histories, run_simulation_from_rocket
from physics import Atmosphere, Physics
from eom import EOM


def run_model_and_heat_load(input_file: str):
    """runs a simulation of a verhicle and returns time and integrated heat load [MJ/m²]
    zurück."""
    sol, thermo, rocket = run_simulation(input_file)

    t = sol.t
    v = sol.y[0]
    t_thermo, q, T_wall = compute_thermal_histories(sol, thermo)

    q_MW = q / 1e6

    return t, v, q_MW, T_wall


def run_model_for_acceleration(input_file: str):
    """runs a simulation of a verhicle and returns time and integrated heat load [MJ/m²]
    zurück."""
    sol, thermo, rocket = run_simulation(input_file)

    t = sol.t

    v_dot, v_dot_max = compute_v_dot(rocket, sol)

    return t, v_dot


def compute_v_dot(rocket, sol) -> tuple[ndarray, float]:
    """computes the acceleration history over time from the solution object"""
    t = sol.t
    v = sol.y[0]
    gamma = sol.y[1]
    h = sol.y[2]

    atmos = Atmosphere()
    phys = Physics(rocket=rocket)
    eom = EOM(rocket=rocket, atmos=atmos, phys=phys)

    v_dot = np.zeros_like(t)

    for i in range(len(t)):
        rhs = eom.right_sides(t[i], np.array([v[i], gamma[i], h[i]]))
        v_dot[i] = rhs[0]

    v_dot_max = np.max(np.abs(v_dot))

    return v_dot, v_dot_max


def sweep_parameter(parameter: str, sweep_array: ndarray, base_input_file: str):
    """
    Sweep either 'initial_angle' (deg) or 'ballistic_coefficient' (kg/m²)
    and compute:
      - q_max:   peak heat flux [MW/m²]
      - q_int:   integral heat load [MJ/m²]
      - n_max:   maximum deceleration [g]
    for each value in sweep_array.
    """

    with open(base_input_file, "r", encoding="utf-8") as f:
        base_config = json.load(f)

    if parameter not in ("initial_angle", "ballistic_coefficient"):
        raise ValueError("parameter must be 'initial_angle' or 'ballistic_coefficient'")

    q_max_list = []
    q_int_list = []
    n_max_list = []

    for value in sweep_array:
        config = dict(base_config)
        config[parameter] = value

        rocket = Rocket(**config)

        sol, thermo, rocket = run_simulation_from_rocket(rocket)

        t = sol.t
        v = sol.y[0]
        gamma = sol.y[1]
        h = sol.y[2]

        _, q, T_wall = compute_thermal_histories(sol, thermo)

        q_max = np.max(q) / 1e6                # [MW/m²]
        q_integral = np.trapezoid(q, t) / 1e6  # [MJ/m²]

        phys = thermo.phys
        atmos = thermo.atmos
        eom = EOM(rocket=rocket, atmos=atmos, phys=phys)

        v_dot = np.empty_like(v)
        for i, (ti, vi, gi, hi) in enumerate(zip(t, v, gamma, h)):
            rhs = eom.right_sides(ti, np.array([vi, gi, hi]))
            v_dot[i] = rhs[0]

        v_dot_max = np.max(np.abs(v_dot))

        q_max_list.append(q_max)
        q_int_list.append(q_integral)
        n_max_list.append(v_dot_max)

    return (
        parameter,
        np.array(q_max_list, dtype=float),
        np.array(q_int_list, dtype=float),
        np.array(n_max_list, dtype=float),
    )
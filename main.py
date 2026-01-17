import numpy as np

from running_utils import compute_v_dot, sweep_parameter
from simulate import run_simulation, compute_thermal_histories
from plotting_utils import (
    plot_trajectory,
    plot_parameter_over_time,
    plot_combined,
    plot_heat_flux_comparison,
    plot_wall_temp_comparison,
    plot_sweep,
    plot_both_trajectories,
    plot_v_comparison,
    plot_vdot_comparison,
)
from trajectory import plot_movement


# ============================================================
# Configuration / toggles
# ============================================================

possible_files = [
    "inputs/input_liftingBody.json",
    "inputs/input_ballisticCapsule.json"
]

# to select which input file to use, chosse from possible files and change here:
INPUT_FILE = "inputs/input_ballisticCapsule.json"

# Toggle individual plots
PLOT_ALTITUDE_OVER_VELOCITY = False
PLOT_VELOCITY_OVER_TIME = False
PLOT_HEAT_FLUX_OVER_TIME = False
PLOT_WALL_TEMP_OVER_TIME = False
PLOT_ACCELERATION_OVER_TIME = False

PLOT_COMPARISONS = False         # comparison plots (ballistic vs lifting etc.)
PLOT_MOVEMENT_ANIMATION = False  # trajectory over earth
PLOT_COMBINED_FIGURE = True      # all-in-one figure like the script

# Parameter sweep (either beta or gamma)
RUN_SWEEP = False


# ============================================================
# 1) Run simulation
# ============================================================

# Run a single trajectory simulation and get:
# - sol: ODE solution object (t and state history)
# - thermo: thermal model parameters/settings
# - vehicle: vehicle model object (areas, coefficients, etc.)
sol, thermo, vehicle = run_simulation(INPUT_FILE)

t = sol.t
v = sol.y[0]      # velocity [m/s]
gamma = sol.y[1]  # flight path angle [deg]
h = sol.y[2]      # altitude [m]


# ============================================================
# 2) Quick summary prints
# ============================================================

print(f"duration: {t[-1]:.3f} s")
print(f"terminal velocity: {v[-1]:.3f} m/s")


# ============================================================
# 3) Compute thermal histories
# ============================================================

# compute_thermal_histories returns:
# - t: time [s] (not needed)
# - q: heat flux [W/m^2]
# - T_wall: adiabatic wall temperature [K]
_, q, T_wall = compute_thermal_histories(sol, thermo)

# Maximal heat flux [MW/m^2]
q_max = np.max(q)
print(f"maximal heat flux: {q_max / 1e6:.3f} MW/m²")

# Integrated heat load per unit area [J/m^2]
q_integral = np.trapezoid(q, t)
print(f"integral heat load: {q_integral / 1e6:.3f} MJ/m²")


# ============================================================
# 4) Compute acceleration (v-dot) and peak load
# ============================================================

# v_dot: acceleration history [m/s^2]
# v_dot_max: maximum acceleration magnitude [m/s^2]
v_dot, v_dot_max = compute_v_dot(vehicle, sol)
print(f"maximal acceleration: {v_dot_max:.3f} m/s²")


# ============================================================
# 5) Energy / fraction absorbed by wall
# ============================================================

# Total heat absorbed by wall (integrated heat load * reference area) [J]
Q_wall = q_integral * vehicle.reference_area

# Calculate the vehicle's mass from given parameters
m = vehicle.get_ballistic_coefficient() * vehicle.drag_coefficient * vehicle.reference_area

# Initial kinetic energy [J]
E_kin = 0.5 * m * v[0] ** 2

# Fraction of initial kinetic energy that ends up as wall heat load [%]
eta = (Q_wall / E_kin) * 100
print(f"fraction absorbed by wall (eta): {eta:.3f} %")


# ============================================================
# 6) Plotting (controlled by toggles)
# ============================================================

if PLOT_ALTITUDE_OVER_VELOCITY:
    plot_trajectory(v, h, "Trajectory")

if PLOT_VELOCITY_OVER_TIME:
    v_km_s = v / 1000  # m/s -> km/s
    plot_parameter_over_time(t, v_km_s, "velocity", "velocity (km/s)")

if PLOT_HEAT_FLUX_OVER_TIME:
    plot_parameter_over_time(t, (q / 1e6), "Sutton–Graves heat flux", "heat flux (MW/m²)")

if PLOT_WALL_TEMP_OVER_TIME:
    plot_parameter_over_time(t, T_wall, "adiabatic wall temperature", "temperature (K)")

if PLOT_ACCELERATION_OVER_TIME:
    plot_parameter_over_time(t, v_dot, "acceleration", "acceleration (m/s²)")

if PLOT_MOVEMENT_ANIMATION:
    plot_movement(sol)

if PLOT_COMBINED_FIGURE:
    plot_combined(t, v, h, (q / 1e6), T_wall, 'ballisticCapsule' if 'ballisticCapsule' in INPUT_FILE else 'liftingBody')

if PLOT_COMPARISONS:
    # Compare ballistic capsule and lifting body
    plot_both_trajectories(possible_files)
    plot_heat_flux_comparison()
    plot_wall_temp_comparison()
    plot_v_comparison()
    plot_vdot_comparison()


# ============================================================
# 7) Parameter sweep
# ============================================================

if RUN_SWEEP:
    # Example sweep arrays (uncomment / adjust as needed)
    gamma_values = np.arange(0.1, 21, 0.1)  # degrees
    # beta_values = np.arange(5, 1001, 5)   # kg/m²

    # If sweep array is changed, adjust here as well
    parameter, q_max, q_int, n_max = sweep_parameter(
        parameter="initial_angle",
        sweep_array=gamma_values,
        base_input_file="INPUT_FILE",
    )

    plot_sweep(parameter, gamma_values, q_max, q_int, n_max, True, 10)
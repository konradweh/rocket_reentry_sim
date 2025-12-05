import numpy as np

from running_utils import compute_v_dot, sweep_parameter
from simulate import run_simulation, compute_thermal_histories
from plotting_utils import plot_trajectory, plot_parameter_over_time, format_with_prefix, plot_combined, \
    plot_heat_flux_comparison, plot_wall_temp_comparison, plot_sweep
from trajectory import plot_movement

sol, thermo, rocket = run_simulation("input_ballisticCapsule.json")

t = sol.t
v = sol.y[0]
gamma = sol.y[1]
h = sol.y[2]

print(f"duration: {sol.t[-1]:.3f} s")
print(f"terminal velocity: {sol.y[0, -1]:.3f} m/s")

#plot_trajectory(v, h)

v_km = v / 1000
#plot_parameter_over_time(t, v_km, "velocity", "velocity (km/s)")


_, q, T_wall = compute_thermal_histories(sol, thermo)

q_MW = q / 1e6
#plot_parameter_over_time(t, q_MW, "Sutton–Graves heat flux", "heat flux (MW/m^2)")
#plot_parameter_over_time(t, T_wall, "adiabatic wall temperature", "temperature (K)")

q_max_MW = np.max(q_MW)
print(f"maximal heat load: {q_max_MW:.3f} MW")

q_integral = np.trapezoid(q, t)               # heat load per unit area [J/m^2]
q_integral_formatted = q_integral / 1e6
print(f"intergral heat load: {q_integral_formatted:.3f} MJ/m²")


v_dot, v_dot_max = compute_v_dot(rocket, sol)
#plot_parameter_over_time(t, v_dot, "acceleration", "acceleration (m/s²)")
print(f"maximal acceleration: {v_dot_max:.3f} m/s²")


Q_wall = q_integral * rocket.reference_area   # total heat load [J]

m = rocket.get_ballistic_coefficient() * rocket.drag_coefficient * rocket.reference_area
E_kin = 0.5 * m * v[0] ** 2                   # initial kinetic energy [J]

eta = Q_wall / E_kin * 100                    # percentage of kinetic energy absorbed by the wall
print(f"fraction absorbed by wall (eta) = {eta:.3f} %")


#plot_movement(sol)


#plot_combined(t, v, h, q_MW, T_wall)


#plot_heat_flux_comparison()
#plot_wall_temp_comparison()


gamma_values = np.arange(0.1, 21, 0.1)  # in degrees
beta_values = np.arange(5, 1001, 5)  # in kg/m²

parameter, q_max, q_int, n_max = sweep_parameter(
    parameter="ballistic_coefficient",
    sweep_array=beta_values,
    base_input_file="input_ballisticCapsule.json",
)

plot_sweep(parameter, beta_values, q_max, q_int, n_max, True, 400)
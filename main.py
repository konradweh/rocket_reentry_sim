import numpy as np

from simulate import run_simulation, compute_thermal_histories
from utils import plot_trajectory, plot_parameter_over_time, format_with_prefix

sol, thermo = run_simulation()

t = sol.t
v = sol.y[0]
gamma = sol.y[1]
h = sol.y[2]

print("duration:", sol.t[-1])
print("y_end:", sol.y[:, -1])

plot_trajectory(v, h)

v_km = v / 1000
plot_parameter_over_time(t, v_km, "velocity", "velocity (km/s)")

t, q, T_wall = compute_thermal_histories(sol, thermo)

q_MW = q / 1000
plot_parameter_over_time(t, q_MW, "Sutton–Graves heat flux", "heat flux (W/m^2)")
plot_parameter_over_time(t, T_wall, "adiabatic wall temperature", "temperature (K)")

q_integral = np.trapezoid(q, t)
print("Intergral heat load:", format_with_prefix(q_integral, "J/m^2"))
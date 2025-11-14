from simulate import run_simulation
from utils import plot_trajectory

sol = run_simulation(t_max=1000)

t = sol.t
v = sol.y[0]
gamma = sol.y[1]
h = sol.y[2]

plot_trajectory(v, h)
from simulate import run_simulation
from utils import plot_trajectory

sol = run_simulation()

t = sol.t
v = sol.y[0]
gamma = sol.y[1]
h = sol.y[2]

plot_trajectory(v, h)

print("status:", sol.status)
print("message:", sol.message)
print("t_end:", sol.t[-1])
print("y_end:", sol.y[:, -1])
print("t_events:", sol.t_events)
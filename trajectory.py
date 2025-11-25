import numpy as np
from matplotlib import pyplot as plt

from physics import Physics

def plot_movement(sol):
    t = sol.t
    v = sol.y[0]
    gamma = sol.y[1]
    h = sol.y[2]

    RE = Physics.RE
    r = RE + h

    theta = np.zeros_like(t)        # initialise array for angle
    theta[0] = np.pi / 2            # start at 90° (zenith)

    for i in range(1, len(t)):
        dt = t[i] - t[i - 1]

        theta_dot_i = - v[i] * np.cos(gamma[i]) / r[i]
        theta_dot_im1 = - v[i - 1] * np.cos(gamma[i - 1]) / r[i - 1]

        theta[i] = theta[i - 1] + 0.5 * (theta_dot_i + theta_dot_im1) * dt

    x_traj = r * np.cos(theta)       # convert to Cartesian coordinates
    y_traj = r * np.sin(theta)

    phi = np.linspace(0, np.pi, 500)  # 0 bis 180° = top half of Earth
    x_earth = RE * np.cos(phi)
    y_earth = RE * np.sin(phi)

    plt.figure(figsize=(8, 8))

    plt.fill(x_earth / 1000, y_earth / 1000, alpha=0.2)  # km
    plt.plot(x_earth / 1000, y_earth / 1000, linewidth=2, label="Earth")

    plt.plot(x_traj / 1000, y_traj / 1000, label="Reentry trajectory")

    plt.gca().set_aspect("equal", "box")
    plt.xlabel("x (km)")
    plt.ylabel("y (km)")
    plt.title("Reentry trajectory relative to Earth")
    plt.legend()
    plt.grid(True)
    plt.xlim(-50, 450)
    plt.ylim(6300, 6500)

    plt.show()
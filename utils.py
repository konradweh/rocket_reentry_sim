import matplotlib.pyplot as plt
import numpy as np


def plot_trajectory(x: np.ndarray, y: np.ndarray, title="trajectory"):
    altitude_in_km = y / 1000
    velocity_in_km_s = x / 1000

    plt.figure(figsize=(10, 5))
    plt.plot(velocity_in_km_s, altitude_in_km)
    plt.title(title)
    plt.xlabel("velocity (km/s)")
    plt.ylabel("altitude (km)")
    plt.grid(True)
    plt.show()
import matplotlib.pyplot as plt

def plot_trajectory(x: float, y: float, title="trajectory"):
    plt.figure(figsize=(10, 5))
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel("velocity (m/s)")
    plt.ylabel("altitude (m)")
    plt.grid(True)
    plt.show()
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

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


def plot_parameter_over_time(time: np.ndarray, parameter: np.ndarray, parameter_name: str, ylabel: str):
    plt.figure(figsize=(10, 5))
    plt.plot(time, parameter)
    plt.title(f"{parameter_name} over time")
    plt.xlabel("time (s)")
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()


def format_with_prefix(value: float, unit: str, decimals=3):
    """Formats a value with an appropriate SI prefix"""
    prefixes = [
        (1e-24, "y"),   # yocto
        (1e-21, "z"),   # zepto
        (1e-18, "a"),   # atto
        (1e-15, "f"),   # femto
        (1e-12, "p"),   # pico
        (1e-9,  "n"),   # nano
        (1e-6,  "µ"),   # micro
        (1e-3,  "m"),   # milli
        (1e0,   ""),    # base
        (1e3,   "k"),   # kilo
        (1e6,   "M"),   # mega
        (1e9,   "G"),   # giga
        (1e12,  "T"),   # tera
        (1e15,  "P"),   # peta
        (1e18,  "E"),   # exa
    ]

    abs_val = abs(value)

    # find the best prefix, i.e., the largest factor less than or equal to abs_val
    best_factor, prefix = max((f, p) for f, p in prefixes if abs_val >= f)

    scaled = value / best_factor
    return f"{scaled:.{decimals}f} {prefix}{unit}"


def plot_combined(t, v, h, q_MW, T_wall):
    # vorberechnen
    altitude_km = h / 1000
    velocity_km_s = v / 1000

    fig = plt.figure(figsize=(14, 6), constrained_layout=True)
    gs = gridspec.GridSpec(3, 2, figure=fig, width_ratios=[2.5, 1])

    # --------------------------------------
    # LEFT: big trajectory plot
    # --------------------------------------
    ax_big = fig.add_subplot(gs[:, 0])  # alle Zeilen, linke Spalte
    ax_big.plot(velocity_km_s, altitude_km)
    ax_big.set_title("Trajectory")
    ax_big.set_xlabel("velocity (km/s)")
    ax_big.set_ylabel("altitude (km)")

    # --------------------------------------
    # RIGHT: small plots (stacked)
    # --------------------------------------
    # 1. velocity over time
    ax1 = fig.add_subplot(gs[0, 1])
    ax1.plot(t, velocity_km_s)
    ax1.set_title("velocity over time")
    ax1.set_ylabel("velocity (km/s)")
    ax1.tick_params(axis="x", which="both", bottom=True, labelbottom=False)

    # 2. heat flux
    ax2 = fig.add_subplot(gs[1, 1])
    ax2.plot(t, q_MW)
    ax2.set_title("Sutton–Graves heat flux")
    ax2.set_ylabel("heat flux (MW/m²)")
    ax2.tick_params(axis="x", which="both", bottom=True, labelbottom=False)

    # 3. adiabatic wall temperature
    ax3 = fig.add_subplot(gs[2, 1])
    ax3.plot(t, T_wall)
    ax3.set_title("adiabatic wall temperature")
    ax3.set_xlabel("time (s)")
    ax3.set_ylabel("temperature (K)")

    plt.show()
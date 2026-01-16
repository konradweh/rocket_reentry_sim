import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
from datetime import datetime
from pathlib import Path
import json

from running_utils import run_model_and_heat_load, run_model_for_acceleration
from simulate import run_simulation

def plot_trajectory(x: np.ndarray, y: np.ndarray, label: str = None):
    altitude_in_km = y / 1000
    velocity_in_km_s = x / 1000
    plt.plot(velocity_in_km_s, altitude_in_km, label=label)


def plot_both_trajectories(sweepingparams, title="trajectory comparison"):
    plt.figure(figsize=(10, 5))

    name_map = {
        "input_ballisticCapsule.json": "ballistic capsule",
        "input_liftingBody.json": "lifting body",
    }

    for param in sweepingparams:
        sol, thermo, rocket = run_simulation(str(param))
        v = sol.y[0]
        h = sol.y[2]

        param_name = name_map.get(str(param), str(param))
        plot_trajectory(v, h, label=param_name)

    plt.title(title)
    plt.xlabel("velocity (km/s)")
    plt.ylabel("altitude (km)")
    plt.legend()
    plt.grid(True, alpha=0.3)

    save_figure(plt, title)
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


def build_case_info_text(input_file: str, label: str) -> str:
    """Build a small info text box for a given input JSON."""
    with open(input_file, "r") as f:
        data = json.load(f)

    beta = data["ballistic_coefficient"]
    L_over_D = data["L_over_D"]
    gamma0 = data["initial_angle"]
    h0_km = data["initial_altitude"] / 1000.0

    text = (
        f"{label}:\n"
        rf"$\beta = {beta:.0f}\,\mathrm{{kg/m^2}}$" "\n"
        rf"$L/D = {L_over_D:.2f}$" "\n"
        rf"$\gamma_0 = {gamma0:.1f}^\circ$" "\n"
        rf"$h_0 = {h0_km:.0f}\,\mathrm{{km}}$"
    )
    return text


def plot_v_comparison():
    """compares heat flux for different trajectory cases"""

    cases = [
        ("input_ballisticCapsule.json", "ballistic capsule"),
        ("input_liftingBody.json", "lifting body"),
    ]

    fig, ax = plt.subplots(figsize=(8, 5))

    for input_file, label in cases:
        t, v, _, _ = run_model_and_heat_load(input_file)
        ax.plot(t, v, label=label)

    ax.set_title("velocity comparison")
    ax.set_xlabel("time (s)")
    ax.set_ylabel("velocity (m/s)")
    ax.legend()
    fig.tight_layout()

    text_ballistic = build_case_info_text("input_ballisticCapsule.json", "ballistic capsule")
    text_lifting = build_case_info_text("input_liftingBody.json", "lifting body")

    ax.text(
        0.98, 0.98, text_ballistic,
        transform=ax.transAxes,
        ha="right", va="top",
        fontsize=9,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
    )

    ax.text(
        0.98, 0.55, text_lifting,
        transform=ax.transAxes,
        ha="right", va="top",
        fontsize=9,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
    )

    save_figure(fig, 'velocity_comparison')
    plt.show()


def plot_vdot_comparison():
    """compares heat flux for different trajectory cases"""

    cases = [
        ("input_ballisticCapsule.json", "ballistic capsule"),
        ("input_liftingBody.json", "lifting body"),
    ]

    fig, ax = plt.subplots(figsize=(8, 5))

    for input_file, label in cases:
        t, v_dot = run_model_for_acceleration(input_file)
        ax.plot(t, v_dot, label=label)

    ax.set_title("acceleration comparison")
    ax.set_xlabel("time (s)")
    ax.set_ylabel("acceleration (m/s^2)")
    ax.legend()
    fig.tight_layout()

    text_ballistic = build_case_info_text("input_ballisticCapsule.json", "ballistic capsule")
    text_lifting = build_case_info_text("input_liftingBody.json", "lifting body")

    ax.text(
        0.98, 0.98, text_ballistic,
        transform=ax.transAxes,
        ha="right", va="top",
        fontsize=9,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
    )

    ax.text(
        0.98, 0.55, text_lifting,
        transform=ax.transAxes,
        ha="right", va="top",
        fontsize=9,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
    )

    save_figure(fig, 'acceleration_comparison')
    plt.show()


def plot_heat_flux_comparison():
    """compares heat flux for different trajectory cases"""

    cases = [
        ("input_ballisticCapsule.json", "ballistic capsule"),
        ("input_liftingBody.json", "lifting body"),
    ]

    fig, ax = plt.subplots(figsize=(8, 5))

    for input_file, label in cases:
        t, _, q, _ = run_model_and_heat_load(input_file)
        ax.plot(t, q, label=label)

    ax.set_title("heat flux comparison")
    ax.set_xlabel("time (s)")
    ax.set_ylabel("heat flux (MW/m²)")
    ax.legend()
    fig.tight_layout()

    text_ballistic = build_case_info_text("input_ballisticCapsule.json", "ballistic capsule")
    text_lifting = build_case_info_text("input_liftingBody.json", "lifting body")

    ax.text(
        0.98, 0.98, text_ballistic,
        transform=ax.transAxes,
        ha="right", va="top",
        fontsize=9,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
    )

    ax.text(
        0.98, 0.55, text_lifting,
        transform=ax.transAxes,
        ha="right", va="top",
        fontsize=9,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
    )

    save_figure(fig, 'heat_flux_comparison')
    plt.show()


def plot_wall_temp_comparison():
    """compares wall temperature for different trajectory cases"""

    cases = [
        ("input_ballisticCapsule.json", "ballistic capsule"),
        ("input_liftingBody.json", "lifting body"),
    ]

    fig, ax = plt.subplots(figsize=(8, 5))

    for input_file, label in cases:
        t, _, _, T_wall = run_model_and_heat_load(input_file)
        ax.plot(t, T_wall, label=label)

    ax.set_title("wall temperature comparison")
    ax.set_xlabel("time (s)")
    ax.set_ylabel("wall temperature (K)")
    ax.legend()
    fig.tight_layout()

    text_ballistic = build_case_info_text("input_ballisticCapsule.json", "ballistic capsule")
    text_lifting = build_case_info_text("input_liftingBody.json", "lifting body")

    ax.text(
        0.98, 0.98, text_ballistic,
        transform=ax.transAxes,
        ha="right", va="top",
        fontsize=9,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
    )

    ax.text(
        0.98, 0.55, text_lifting,
        transform=ax.transAxes,
        ha="right", va="top",
        fontsize=9,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
    )

    save_figure(fig, 'wall_temp_comparison')
    plt.show()


def save_figure(fig, name: str):
    output_dir = Path(r"C:\Users\kw\Documents\Uni\Grundlagen der Raumfahrt\rocket_reentry_sim\plots")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # z.B. 20251203_153045
    filename = f"{name}_{timestamp}.pdf"
    filepath = output_dir / filename

    fig.savefig(filepath, format="pdf")


def plot_sweep(parameter: str, x: np.ndarray, q_max: list[float], q_int: list[float], v_dot_max: list[float],
               v_line=False, v_line_x=400):
    if parameter == "initial_angle":
        x_label = "initial angle γ₀ (deg)"
    elif parameter == "ballistic_coefficient":
        x_label = "ballistic coefficient β (kg/m²)"
    else:
        x_label = parameter

    fig, (ax_top, ax_bottom) = plt.subplots(
        2, 1,
        figsize=(8, 8),
        sharex=True,
        gridspec_kw={'height_ratios': [1.2, 1]}
    )

    color1 = "#004B23"  # dark green
    color2 = "#6A0DAD"  # dark yellow
    color3 = "#003F5C"  # dark blue

    ax_top.plot(x, q_max, ".-", color=color1, label="peak heat flux")
    ax_top.set_ylabel("peak heat flux (MW/m²)", color=color1)
    ax_top.tick_params(axis="y", labelcolor=color1)

    ax_top_2 = ax_top.twinx()
    ax_top_2.plot(x, q_int, ".-", color=color2, label="integral heat load")
    ax_top_2.set_ylabel("integral heat load (MJ/m²)", color=color2)
    ax_top_2.tick_params(axis="y", labelcolor=color2)

    if v_line:
        ax_top.axvline(v_line_x, color="gray", linestyle="--", linewidth=1)
        ax_top_2.axvline(v_line_x, color="gray", linestyle="--", linewidth=1)
        ax_bottom.axvline(v_line_x, color="gray", linestyle="--", linewidth=1)

    ax_bottom.plot(x, v_dot_max, ".-", color=color3)
    ax_bottom.set_xlabel(x_label)
    ax_bottom.set_ylabel("max acceleration (m/s²)", color=color3)
    ax_bottom.tick_params(axis="y", labelcolor=color3)

    fig.tight_layout()
    save_figure(fig, f'sweep_{parameter}')
    plt.show()
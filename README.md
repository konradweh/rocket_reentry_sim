# Atmospheric Reentry Simulation

This repository contains a physics-based simulation of atmospheric reentry for space vehicles such as
ballistic capsules and lifting bodies.  
The model computes the vehicle trajectory, deceleration, and thermal loads during entry into Earth's
atmosphere and allows for systematic parameter studies.

The project was developed in the context of the course *Grundlagen der Raumfahrt* and is intended
as an educational and exploratory tool for atmospheric entry dynamics.

---

## Physical Model Overview

The simulation is based on a simplified **3-degree-of-freedom (3-DOF)** point-mass model,
assuming motion in the vertical plane and neglecting attitude dynamics.

### Implemented physics:

- Equations of motion in flight-path coordinates (velocity, flight-path angle, altitude)
- Variable gravity with altitude
- Exponential atmospheric density model
- Aerodynamic drag and lift with constant coefficients
- Ballistic coefficient formulation
- Sutton–Graves correlation for convective stagnation-point heat flux
- Radiative equilibrium wall temperature (Stefan–Boltzmann)
- Event-based termination at ground impact

The model is intentionally kept simple to highlight fundamental reentry mechanisms and trade-offs
between heating, deceleration, and trajectory shaping.

---

## Features

- Ballistic and lifting reentry simulations
- Comparison of different vehicle configurations
- Velocity, acceleration, altitude, and trajectory plots
- Heat flux and wall temperature histories
- Integral heat load computation
- Parameter sweeps:
  - Initial flight-path angle
  - Ballistic coefficient
- Visualization tools for direct comparison of entry profiles

---

## Example Applications

- Comparison of ballistic capsules vs. lifting bodies
- Analysis of peak heat flux vs. total heat load
- Investigation of skip trajectories and lift-based control
- Sensitivity studies for entry angle and vehicle design

---

## Installation

- python -m venv venv
- source venv/bin/activate   # Linux / macOS
- venv\Scripts\activate      # Windows
- pip install -r requirements.txt

---

## Project Structure

```text
.
├── main.py             # Entry point for simulations
├── atmosphere.py
├── vehicle.py
├── equations.py
├── simulation.py
├── utils.py
├── configs/            # JSON configuration files for vehicles and scenarios
├── plots/              # Generated plots
└── requirements.txt

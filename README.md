# Atmospheric Reentry Simulation

This project simulates the atmospheric reentry of a spacecraft (e.g. ballistic capsule or lifting body).
It computes the vehicle trajectory, deceleration, and thermal loads during entry and provides
multiple plotting and comparison options.

## Features

- 3-DOF atmospheric entry equations of motion
- Variable gravity with altitude
- Exponential atmosphere model
- Aerodynamic drag and lift (constant coefficients)
- Sutton–Graves convective heat flux model
- Radiative equilibrium wall temperature
- Event-based termination at ground impact
- Parameter sweeps (entry angle, ballistic coefficient)
- Multiple plotting and comparison tools

## Setup

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
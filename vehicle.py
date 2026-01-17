import json
from dataclasses import dataclass

@dataclass
class Vehicle:
    """Geometric and aerodynamic properties of a reentry vehicle."""
    mass: float                  # [kg]
    reference_area: float        # [m^2]
    drag_coefficient: float      # [-]
    lift_coefficient: float      # [-]
    ballistic_coefficient: float # [kg/m^2] (must satisfy β = m / (Cd*A))
    L_over_D: float              # [-] (constant approximation)
    initial_angle: float         # [deg or rad – model dependent]
    initial_altitude: float      # [m]
    initial_velocity: float      # [m/s]
    nose_radius: float           # [m]
    emission_coefficient: float  # [-]

    @classmethod
    def import_data(cls, file_path: str) -> "Vehicle":
        """imports rocket data from a JSON file and returns a Rocket instance"""
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(**data)

    def compute_ballistic_coefficient(self) -> float:
        """compute the ballistic coefficient (kg/m^2) of the rocket"""
        return self.mass / (self.drag_coefficient * self.reference_area)

    def get_ballistic_coefficient(self) -> float:
        """returns the ballistic coefficient (kg/m^2) of the rocket from input-file"""
        return self.ballistic_coefficient

    def aerodynamic_drag(self, q: float) -> float:
        """calculates the aerodynamic drag force (N) on the rocket for dynamic pressure q (Pa)"""
        return q * self.drag_coefficient * self.reference_area

    def aerodynamic_lift(self, q: float) -> float:
        """calculates the lift force (N) on the rocket for dynamic pressure q (Pa)"""
        return q * self.lift_coefficient * self.reference_area

    def compute_L_over_D(self, q: float) -> float:
        """Compute L/D from c_L and c_D."""
        if self.aerodynamic_drag(q) == 0.0:
            return 0.0
        return self.aerodynamic_lift(q) / self.aerodynamic_drag(q)

    def get_L_over_D(self) -> float:
        """Get L/D from input-file."""
        return self.L_over_D
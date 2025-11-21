import json
from dataclasses import dataclass

@dataclass
class Rocket:
    """Class for various rocket-related calculations"""
    mass: float
    reference_area: float
    drag_coefficient: float
    lift_coefficient: float
    ballistic_coefficient: float
    L_over_D: float
    initial_angle: float
    initial_altitude: float
    initial_velocity: float
    nose_radius: float
    emission_coefficient: float

    @classmethod
    def import_data(cls, file_path: str) -> "Rocket":
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
        if self.aerodynamic_drag() == 0.0:
            return 0.0  # mathematisch sicherer fallback
        return self.aerodynamic_lift(q) / self.aerodynamic_drag(q)

    def get_L_over_D(self) -> float:
        """Get L/D from input-file."""
        return self.L_over_D
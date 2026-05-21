"""Projectile motion — range, max height, time of flight for a projectile."""
import math
from ._base import non_negative, positive, require, to_float

META = {
    "slug": "projectile-motion",
    "name": "Projectile Motion Calculator",
    "category": "physics",
    "description": "Calculate range, max height, and flight time for a projectile launched with given speed and angle.",
    "formula": "R = v²·sin(2θ)/g;  H = v²·sin²(θ)/(2g);  T = 2v·sin(θ)/g",
    "fields": [
        {"name": "initial_velocity", "label": "Initial Velocity (m/s)", "type": "number", "min": 0, "required": True, "placeholder": "30"},
        {"name": "angle_degrees", "label": "Launch Angle (°)", "type": "number", "required": True, "placeholder": "45"},
        {"name": "gravity", "label": "Gravity (m/s², default 9.81)", "type": "number", "min": 0, "required": False, "placeholder": "9.81"},
    ],
    "outputs": [
        {"key": "range_m", "label": "Horizontal Range (m)", "format": "number"},
        {"key": "max_height_m", "label": "Maximum Height (m)", "format": "number"},
        {"key": "time_of_flight_s", "label": "Time of Flight (s)", "format": "number"},
        {"key": "horizontal_velocity_mps", "label": "Horizontal Velocity (m/s)", "format": "number"},
        {"key": "vertical_velocity_mps", "label": "Initial Vertical Velocity (m/s)", "format": "number"},
    ],
    "faq": [
        {"q": "What angle gives max range?", "a": "45° on flat ground in a vacuum. Air resistance pushes the optimal angle lower (~43° for a baseball, ~30° for a shotput)."},
        {"q": "Limitations?", "a": "Assumes no air resistance, level ground, and constant gravity. Real projectiles deviate considerably at high speeds."},
    ],
}

def calculate(inputs):
    v, angle = require(inputs, "initial_velocity", "angle_degrees")
    g = to_float(inputs["gravity"] if inputs.get("gravity") not in (None, "") else 9.81, "gravity")
    non_negative(v, "initial_velocity"); positive(g, "gravity")
    theta = math.radians(angle)
    vx = v * math.cos(theta); vy = v * math.sin(theta)
    R = (v*v * math.sin(2*theta)) / g
    H = (v*v * math.sin(theta)**2) / (2*g)
    T = (2 * v * math.sin(theta)) / g
    return {
        "range_m": round(R, 4),
        "max_height_m": round(H, 4),
        "time_of_flight_s": round(T, 4),
        "horizontal_velocity_mps": round(vx, 4),
        "vertical_velocity_mps": round(vy, 4),
    }

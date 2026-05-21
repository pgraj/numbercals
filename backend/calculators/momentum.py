"""Momentum (p = m × v) — Newton's 2nd law in the form F = dp/dt."""
from ._base import non_negative, require

META = {
    "slug": "momentum",
    "name": "Momentum Calculator",
    "category": "physics",
    "description": "Calculate the linear momentum of a moving object.",
    "formula": "p = m × v",
    "fields": [
        {"name": "mass", "label": "Mass (kg)", "type": "number", "min": 0, "required": True, "placeholder": "1500"},
        {"name": "velocity", "label": "Velocity (m/s)", "type": "number", "required": True, "placeholder": "20"},
    ],
    "outputs": [{"key": "momentum", "label": "Momentum (kg·m/s)", "format": "number"}],
    "faq": [
        {"q": "Why does momentum matter?", "a": "Conservation of momentum is one of the most fundamental laws of physics. In a closed system, total momentum is preserved through collisions — the basis for everything from car crash physics to rocket propulsion."},
    ],
}

def calculate(inputs):
    m, v = require(inputs, "mass", "velocity")
    non_negative(m, "mass")
    return {"momentum": round(m * v, 4)}

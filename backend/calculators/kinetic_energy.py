"""Kinetic Energy Calculator. KE = ½mv²"""
from typing import Any, Dict
from ._base import non_negative, require

META = {
    "slug": "kinetic-energy",
    "name": "Kinetic Energy Calculator",
    "category": "physics",
    "description": "Calculate the kinetic energy of a moving object.",
    "formula": "KE = ½ · m · v²",
    "fields": [
        {"name": "mass", "label": "Mass (kg)", "type": "number", "min": 0, "required": True, "placeholder": "1500"},
        {"name": "velocity", "label": "Velocity (m/s)", "type": "number", "required": True, "placeholder": "20"},
    ],
    "outputs": [{"key": "kinetic_energy_joules", "label": "Kinetic Energy (J)", "format": "number"}],
    "faq": [{"q": "Why squared?", "a": "Energy scales with v² — doubling speed quadruples kinetic energy. This is why car crash forces grow so rapidly with speed."}],
}

def calculate(inputs):
    m, v = require(inputs, "mass", "velocity")
    non_negative(m, "mass")
    return {"kinetic_energy_joules": round(0.5 * m * v * v, 4)}

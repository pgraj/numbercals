"""Gravitational Potential Energy. PE = m·g·h"""
from typing import Any, Dict
from ._base import non_negative, require, to_float

META = {
    "slug": "potential-energy",
    "name": "Potential Energy Calculator",
    "category": "physics",
    "description": "Calculate gravitational potential energy at a given height.",
    "formula": "PE = m · g · h",
    "fields": [
        {"name": "mass", "label": "Mass (kg)", "type": "number", "min": 0, "required": True, "placeholder": "10"},
        {"name": "height", "label": "Height (m)", "type": "number", "min": 0, "required": True, "placeholder": "20"},
        {"name": "gravity", "label": "Gravity (m/s², default 9.81)", "type": "number", "min": 0, "required": False, "placeholder": "9.81"},
    ],
    "outputs": [{"key": "potential_energy_joules", "label": "PE (J)", "format": "number"}],
    "faq": [{"q": "What about g on other planets?", "a": "Override the default — Moon ≈ 1.62, Mars ≈ 3.71, Jupiter ≈ 24.79 m/s²."}],
}

def calculate(inputs):
    m, h = require(inputs, "mass", "height")
    g = to_float(inputs["gravity"] if inputs.get("gravity") not in (None, "") else 9.81, "gravity")
    non_negative(m, "mass"); non_negative(h, "height"); non_negative(g, "gravity")
    return {"potential_energy_joules": round(m * g * h, 4)}

"""Acceleration Calculator. a = (v − u) / t"""
from typing import Any, Dict
from ._base import positive, require

META = {
    "slug": "acceleration",
    "name": "Acceleration Calculator",
    "category": "physics",
    "description": "Calculate acceleration from initial velocity, final velocity, and time.",
    "formula": "a = (v − u) / t",
    "fields": [
        {"name": "initial_velocity", "label": "Initial Velocity (u, m/s)", "type": "number", "required": True, "placeholder": "0"},
        {"name": "final_velocity", "label": "Final Velocity (v, m/s)", "type": "number", "required": True, "placeholder": "27"},
        {"name": "time", "label": "Time (s)", "type": "number", "min": 0, "required": True, "placeholder": "10"},
    ],
    "outputs": [{"key": "acceleration", "label": "Acceleration (m/s²)", "format": "number"}],
    "faq": [{"q": "Can acceleration be negative?", "a": "Yes — negative acceleration (deceleration) means velocity decreases over time."}],
}

def calculate(inputs):
    u, v, t = require(inputs, "initial_velocity", "final_velocity", "time")
    positive(t, "time")
    return {"acceleration": round((v - u) / t, 4)}

"""Force Calculator. F = m × a (Newton's second law)"""
from typing import Any, Dict
from ._base import require

META = {
    "slug": "force",
    "name": "Force Calculator",
    "category": "physics",
    "description": "Calculate force from mass and acceleration using Newton's second law.",
    "formula": "F = m × a",
    "fields": [
        {"name": "mass", "label": "Mass (kg)", "type": "number", "min": 0, "required": True, "placeholder": "10"},
        {"name": "acceleration", "label": "Acceleration (m/s²)", "type": "number", "required": True, "placeholder": "9.8"},
    ],
    "outputs": [{"key": "force_newtons", "label": "Force (N)", "format": "number"}],
    "faq": [{"q": "What is 1 Newton?", "a": "The force needed to accelerate 1 kg at 1 m/s². Roughly the weight of a small apple under Earth's gravity."}],
}

def calculate(inputs):
    m, a = require(inputs, "mass", "acceleration")
    return {"force_newtons": round(m * a, 4)}

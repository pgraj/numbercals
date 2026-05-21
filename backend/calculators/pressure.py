"""Pressure Calculator. P = F / A"""
from typing import Any, Dict
from ._base import non_negative, positive, require

META = {
    "slug": "pressure",
    "name": "Pressure Calculator",
    "category": "physics",
    "description": "Calculate pressure from force and area.",
    "formula": "P = F / A",
    "fields": [
        {"name": "force", "label": "Force (N)", "type": "number", "min": 0, "required": True, "placeholder": "100"},
        {"name": "area", "label": "Area (m²)", "type": "number", "min": 0, "required": True, "placeholder": "2"},
    ],
    "outputs": [
        {"key": "pressure_pascals", "label": "Pressure (Pa)", "format": "number"},
        {"key": "pressure_kpa", "label": "Pressure (kPa)", "format": "number"},
    ],
    "faq": [{"q": "What is 1 Pascal?", "a": "1 N per m². Atmospheric pressure is ~101,325 Pa (101.3 kPa)."}],
}

def calculate(inputs):
    f, a = require(inputs, "force", "area")
    non_negative(f, "force"); positive(a, "area")
    p = f / a
    return {"pressure_pascals": round(p, 4), "pressure_kpa": round(p / 1000, 4)}

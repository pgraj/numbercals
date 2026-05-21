"""Density Calculator. ρ = m / V"""
from typing import Any, Dict
from ._base import non_negative, positive, require

META = {
    "slug": "density",
    "name": "Density Calculator",
    "category": "physics",
    "description": "Calculate density from mass and volume.",
    "formula": "ρ = m / V",
    "fields": [
        {"name": "mass", "label": "Mass (kg)", "type": "number", "min": 0, "required": True, "placeholder": "1000"},
        {"name": "volume", "label": "Volume (m³)", "type": "number", "min": 0, "required": True, "placeholder": "1"},
    ],
    "outputs": [{"key": "density", "label": "Density (kg/m³)", "format": "number"}],
    "faq": [{"q": "Density of water?", "a": "Pure water at 4°C is ~1000 kg/m³ (= 1 g/cm³) — the basis for many density comparisons."}],
}

def calculate(inputs):
    m, v = require(inputs, "mass", "volume")
    non_negative(m, "mass"); positive(v, "volume")
    return {"density": round(m / v, 6)}

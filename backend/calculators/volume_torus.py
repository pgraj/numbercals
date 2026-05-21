"""Torus (doughnut) — volume and surface area."""
import math
from ._base import positive, require

META = {
    "slug": "volume-torus",
    "name": "Torus Volume Calculator",
    "category": "geometry",
    "description": "Calculate volume and surface area of a torus (doughnut shape).",
    "formula": "V = 2π²·R·r²;  SA = 4π²·R·r",
    "fields": [
        {"name": "major_radius", "label": "Major Radius (R, centre of tube to centre of torus)", "type": "number", "min": 0, "required": True, "placeholder": "5"},
        {"name": "minor_radius", "label": "Minor Radius (r, tube radius)", "type": "number", "min": 0, "required": True, "placeholder": "2"},
    ],
    "outputs": [
        {"key": "volume", "label": "Volume", "format": "number"},
        {"key": "surface_area", "label": "Surface Area", "format": "number"},
    ],
    "faq": [{"q": "R vs r?", "a": "R is the distance from the centre of the torus to the centre of the tube. r is the radius of the tube itself. R must be ≥ r for a valid torus."}],
}

def calculate(inputs):
    R, r = require(inputs, "major_radius", "minor_radius")
    positive(R, "major_radius"); positive(r, "minor_radius")
    if R < r: raise ValueError("Major radius (R) must be ≥ minor radius (r) for a valid torus.")
    return {
        "volume": round(2*math.pi**2 * R * r*r, 6),
        "surface_area": round(4*math.pi**2 * R * r, 6),
    }

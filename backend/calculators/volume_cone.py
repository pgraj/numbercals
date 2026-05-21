"""Cone — volume, surface area, slant height."""
import math
from ._base import positive, require

META = {
    "slug": "volume-cone",
    "name": "Cone Volume Calculator",
    "category": "geometry",
    "description": "Calculate volume, surface area, and slant height of a right circular cone.",
    "formula": "V = (1/3)π·r²·h;  SA = π·r·(r + ℓ);  ℓ = √(r² + h²)",
    "fields": [
        {"name": "radius", "label": "Base Radius", "type": "number", "min": 0, "required": True, "placeholder": "3"},
        {"name": "height", "label": "Perpendicular Height", "type": "number", "min": 0, "required": True, "placeholder": "8"},
    ],
    "outputs": [
        {"key": "volume", "label": "Volume", "format": "number"},
        {"key": "slant_height", "label": "Slant Height", "format": "number"},
        {"key": "surface_area_total", "label": "Total Surface Area", "format": "number"},
        {"key": "lateral_surface_area", "label": "Lateral Surface Area", "format": "number"},
    ],
    "faq": [{"q": "Cone vs pyramid?", "a": "A cone has a circular base; a pyramid has a polygonal base. Both share the V = (1/3)·base·height pattern."}],
}

def calculate(inputs):
    r, h = require(inputs, "radius", "height")
    positive(r, "radius"); positive(h, "height")
    slant = math.sqrt(r*r + h*h)
    return {
        "volume": round((1/3)*math.pi*r*r*h, 6),
        "slant_height": round(slant, 6),
        "surface_area_total": round(math.pi*r*(r + slant), 6),
        "lateral_surface_area": round(math.pi*r*slant, 6),
    }

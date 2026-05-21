"""Cylinder — volume, surface area, lateral area."""
import math
from ._base import positive, require

META = {
    "slug": "volume-cylinder",
    "name": "Cylinder Volume Calculator",
    "category": "geometry",
    "description": "Calculate volume, total surface area, and lateral (curved) surface area of a cylinder.",
    "formula": "V = π·r²·h;  SA = 2π·r·(r+h);  Lateral = 2π·r·h",
    "fields": [
        {"name": "radius", "label": "Radius", "type": "number", "min": 0, "required": True, "placeholder": "3"},
        {"name": "height", "label": "Height", "type": "number", "min": 0, "required": True, "placeholder": "10"},
    ],
    "outputs": [
        {"key": "volume", "label": "Volume", "format": "number"},
        {"key": "surface_area_total", "label": "Total Surface Area", "format": "number"},
        {"key": "lateral_surface_area", "label": "Lateral Surface Area (sides only)", "format": "number"},
    ],
    "faq": [{"q": "Total SA vs lateral SA?", "a": "Lateral = the curved side only (e.g., the label on a can). Total = lateral + the two circular ends."}],
}

def calculate(inputs):
    r, h = require(inputs, "radius", "height")
    positive(r, "radius"); positive(h, "height")
    return {
        "volume": round(math.pi*r*r*h, 6),
        "surface_area_total": round(2*math.pi*r*(r+h), 6),
        "lateral_surface_area": round(2*math.pi*r*h, 6),
    }

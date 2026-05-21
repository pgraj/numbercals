"""Sphere — volume and surface area from radius (or radius from either)."""
import math
from ._base import positive, to_float

META = {
    "slug": "volume-sphere",
    "name": "Sphere Volume Calculator",
    "category": "geometry",
    "description": "Calculate volume and surface area of a sphere from radius, diameter, volume, or surface area.",
    "formula": "V = (4/3)π·r³;  SA = 4π·r²",
    "fields": [
        {"name": "known_value", "label": "What you know", "type": "select", "required": True, "default": "radius",
         "options": [
             {"value": "radius", "label": "Radius"},
             {"value": "diameter", "label": "Diameter"},
             {"value": "volume", "label": "Volume"},
             {"value": "surface_area", "label": "Surface Area"},
         ]},
        {"name": "value", "label": "Value", "type": "number", "min": 0, "required": True, "placeholder": "5"},
    ],
    "outputs": [
        {"key": "radius", "label": "Radius", "format": "number"},
        {"key": "diameter", "label": "Diameter", "format": "number"},
        {"key": "volume", "label": "Volume", "format": "number"},
        {"key": "surface_area", "label": "Surface Area", "format": "number"},
    ],
    "faq": [{"q": "How do I find the radius from the volume?", "a": "Pick 'Volume' and enter the value. The calculator solves r = (3V/(4π))^(1/3)."}],
}

def calculate(inputs):
    known = str(inputs.get("known_value", "radius"))
    val = to_float(inputs.get("value"), "value")
    positive(val, "value")
    if known == "radius": r = val
    elif known == "diameter": r = val / 2
    elif known == "volume": r = (3*val / (4*math.pi))**(1/3)
    elif known == "surface_area": r = math.sqrt(val / (4*math.pi))
    else: raise ValueError(f"Unknown: {known}")
    return {
        "radius": round(r, 6),
        "diameter": round(2*r, 6),
        "volume": round((4/3)*math.pi*r**3, 6),
        "surface_area": round(4*math.pi*r*r, 6),
    }

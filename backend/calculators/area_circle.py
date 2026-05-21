"""Circle — area, circumference, diameter from radius (or radius from any of them)."""
import math
from ._base import positive, to_float

META = {
    "slug": "area-circle",
    "name": "Circle Area Calculator",
    "category": "geometry",
    "description": "Calculate area, circumference, diameter, and radius of a circle. Solve from any one value.",
    "formula": "A = π·r²;  C = 2π·r;  d = 2r",
    "fields": [
        {"name": "known_value", "label": "What you know", "type": "select", "required": True, "default": "radius",
         "options": [
             {"value": "radius", "label": "Radius"},
             {"value": "diameter", "label": "Diameter"},
             {"value": "circumference", "label": "Circumference"},
             {"value": "area", "label": "Area"},
         ]},
        {"name": "value", "label": "Value", "type": "number", "min": 0, "required": True, "placeholder": "5"},
    ],
    "outputs": [
        {"key": "radius", "label": "Radius", "format": "number"},
        {"key": "diameter", "label": "Diameter", "format": "number"},
        {"key": "circumference", "label": "Circumference", "format": "number"},
        {"key": "area", "label": "Area", "format": "number"},
    ],
    "faq": [
        {"q": "How do I find the radius from the area?", "a": "Pick 'Area' from the dropdown and enter the value. The calculator computes r = √(A/π) and the rest."},
        {"q": "What's the value of π used?", "a": "Python's math.pi, accurate to ~15 decimal places."},
    ],
}

def calculate(inputs):
    known = str(inputs.get("known_value", "radius"))
    val = to_float(inputs.get("value"), "value")
    positive(val, "value")
    if known == "radius":
        r = val
    elif known == "diameter":
        r = val / 2
    elif known == "circumference":
        r = val / (2 * math.pi)
    elif known == "area":
        r = math.sqrt(val / math.pi)
    else:
        raise ValueError(f"Unknown input: {known}")
    return {
        "radius": round(r, 6),
        "diameter": round(2*r, 6),
        "circumference": round(2*math.pi*r, 6),
        "area": round(math.pi*r*r, 6),
    }

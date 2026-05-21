"""Ellipse — area, approximate circumference (Ramanujan's formula)."""
import math
from ._base import positive, require

META = {
    "slug": "area-ellipse",
    "name": "Ellipse Area Calculator",
    "category": "geometry",
    "description": "Calculate area and approximate circumference of an ellipse from its semi-major and semi-minor axes.",
    "formula": "A = π·a·b;  C ≈ π·(3(a+b) − √((3a+b)(a+3b)))",
    "fields": [
        {"name": "semi_major", "label": "Semi-major axis (a)", "type": "number", "min": 0, "required": True, "placeholder": "5"},
        {"name": "semi_minor", "label": "Semi-minor axis (b)", "type": "number", "min": 0, "required": True, "placeholder": "3"},
    ],
    "outputs": [
        {"key": "area", "label": "Area", "format": "number"},
        {"key": "circumference_approx", "label": "Circumference (Ramanujan's approx.)", "format": "number"},
        {"key": "eccentricity", "label": "Eccentricity (e)", "format": "number"},
    ],
    "faq": [{"q": "Why is the circumference approximate?", "a": "The exact circumference of an ellipse can only be expressed as a non-elementary elliptic integral. Ramanujan's second formula gives an excellent approximation (error < 0.04% for all valid ellipses)."}],
}

def calculate(inputs):
    a, b = require(inputs, "semi_major", "semi_minor")
    positive(a, "semi_major"); positive(b, "semi_minor")
    if b > a: a, b = b, a  # ensure a ≥ b
    area = math.pi * a * b
    # Ramanujan's second approximation
    h = ((a-b)/(a+b))**2
    circ = math.pi * (a+b) * (1 + (3*h)/(10 + math.sqrt(4 - 3*h)))
    e = math.sqrt(1 - (b*b)/(a*a))
    return {"area": round(area, 6), "circumference_approx": round(circ, 6), "eccentricity": round(e, 6)}

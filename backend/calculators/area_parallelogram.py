"""Parallelogram — area, perimeter."""
import math
from ._base import positive, require, to_float

META = {
    "slug": "area-parallelogram",
    "name": "Parallelogram Area Calculator",
    "category": "geometry",
    "description": "Calculate area and perimeter of a parallelogram.",
    "formula": "A = base × height;  P = 2(a + b)",
    "fields": [
        {"name": "base", "label": "Base", "type": "number", "min": 0, "required": True, "placeholder": "8"},
        {"name": "height", "label": "Perpendicular Height", "type": "number", "min": 0, "required": True, "placeholder": "5"},
        {"name": "side", "label": "Slanted Side (for perimeter, optional)", "type": "number", "min": 0, "required": False, "placeholder": "6"},
    ],
    "outputs": [
        {"key": "area", "label": "Area", "format": "number"},
        {"key": "perimeter", "label": "Perimeter (if side provided)", "format": "number"},
    ],
    "faq": [{"q": "What's perpendicular height?", "a": "The shortest distance between the two parallel bases, measured at right angles — NOT the slanted side length."}],
}

def calculate(inputs):
    b, h = require(inputs, "base", "height")
    positive(b, "base"); positive(h, "height")
    result = {"area": round(b*h, 6), "perimeter": None}
    side = inputs.get("side")
    if side not in (None, ""):
        s = to_float(side, "side")
        positive(s, "side")
        result["perimeter"] = round(2*(b+s), 6)
    return result

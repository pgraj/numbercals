"""Trapezoid (trapezium) — area, perimeter."""
from ._base import positive, require, to_float

META = {
    "slug": "area-trapezoid",
    "name": "Trapezoid Area Calculator",
    "category": "geometry",
    "description": "Calculate area and perimeter of a trapezoid (trapezium).",
    "formula": "A = ½·(a + b)·h",
    "fields": [
        {"name": "base_a", "label": "Parallel side a", "type": "number", "min": 0, "required": True, "placeholder": "10"},
        {"name": "base_b", "label": "Parallel side b", "type": "number", "min": 0, "required": True, "placeholder": "6"},
        {"name": "height", "label": "Perpendicular Height", "type": "number", "min": 0, "required": True, "placeholder": "4"},
        {"name": "side_c", "label": "Slanted side c (for perimeter, optional)", "type": "number", "min": 0, "required": False, "placeholder": "5"},
        {"name": "side_d", "label": "Slanted side d (for perimeter, optional)", "type": "number", "min": 0, "required": False, "placeholder": "5"},
    ],
    "outputs": [
        {"key": "area", "label": "Area", "format": "number"},
        {"key": "perimeter", "label": "Perimeter (if all sides given)", "format": "number"},
    ],
    "faq": [{"q": "Trapezoid vs trapezium?", "a": "Same shape, different names. 'Trapezoid' is North American English; 'trapezium' is British English (with the same meaning)."}],
}

def calculate(inputs):
    a, b, h = require(inputs, "base_a", "base_b", "height")
    positive(a, "base_a"); positive(b, "base_b"); positive(h, "height")
    result = {"area": round(0.5*(a+b)*h, 6), "perimeter": None}
    c = inputs.get("side_c"); d = inputs.get("side_d")
    if c not in (None, "") and d not in (None, ""):
        c = to_float(c, "side_c"); d = to_float(d, "side_d")
        positive(c, "side_c"); positive(d, "side_d")
        result["perimeter"] = round(a+b+c+d, 6)
    return result

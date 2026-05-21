"""Rhombus — area from diagonals, perimeter from side."""
import math
from ._base import positive, require

META = {
    "slug": "area-rhombus",
    "name": "Rhombus Area Calculator",
    "category": "geometry",
    "description": "Calculate area of a rhombus from its two diagonals, plus perimeter from the side length.",
    "formula": "A = ½·d₁·d₂;  P = 4s",
    "fields": [
        {"name": "diagonal_1", "label": "Diagonal 1", "type": "number", "min": 0, "required": True, "placeholder": "12"},
        {"name": "diagonal_2", "label": "Diagonal 2", "type": "number", "min": 0, "required": True, "placeholder": "8"},
    ],
    "outputs": [
        {"key": "area", "label": "Area", "format": "number"},
        {"key": "side_length", "label": "Side Length", "format": "number"},
        {"key": "perimeter", "label": "Perimeter", "format": "number"},
    ],
    "faq": [{"q": "Why are the diagonals enough?", "a": "A rhombus's diagonals bisect each other at right angles, so each side is √((d₁/2)² + (d₂/2)²)."}],
}

def calculate(inputs):
    d1, d2 = require(inputs, "diagonal_1", "diagonal_2")
    positive(d1, "diagonal_1"); positive(d2, "diagonal_2")
    side = math.sqrt((d1/2)**2 + (d2/2)**2)
    return {"area": round(0.5*d1*d2, 6), "side_length": round(side, 6), "perimeter": round(4*side, 6)}

"""Square — area, perimeter, diagonal."""
import math
from ._base import positive, require

META = {
    "slug": "area-square",
    "name": "Square Area Calculator",
    "category": "geometry",
    "description": "Calculate area, perimeter, and diagonal of a square from its side length.",
    "formula": "A = s²;  P = 4s;  d = s√2",
    "fields": [
        {"name": "side", "label": "Side Length", "type": "number", "min": 0, "required": True, "placeholder": "5"},
    ],
    "outputs": [
        {"key": "area", "label": "Area", "format": "number"},
        {"key": "perimeter", "label": "Perimeter", "format": "number"},
        {"key": "diagonal", "label": "Diagonal", "format": "number"},
    ],
    "faq": [
        {"q": "How is a square different from a rectangle?", "a": "A square is a rectangle where all four sides are equal length. Every square is a rectangle, but not every rectangle is a square."},
    ],
}

def calculate(inputs):
    (s,) = require(inputs, "side")
    positive(s, "side")
    return {"area": round(s*s, 6), "perimeter": round(4*s, 6), "diagonal": round(s*math.sqrt(2), 6)}

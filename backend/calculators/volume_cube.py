"""Cube — volume, surface area, diagonal."""
import math
from ._base import positive, require

META = {
    "slug": "volume-cube",
    "name": "Cube Volume Calculator",
    "category": "geometry",
    "description": "Calculate volume, surface area, and space diagonal of a cube.",
    "formula": "V = s³;  SA = 6s²;  d = s√3",
    "fields": [
        {"name": "side", "label": "Side Length", "type": "number", "min": 0, "required": True, "placeholder": "5"},
    ],
    "outputs": [
        {"key": "volume", "label": "Volume", "format": "number"},
        {"key": "surface_area", "label": "Surface Area", "format": "number"},
        {"key": "space_diagonal", "label": "Space Diagonal", "format": "number"},
    ],
    "faq": [{"q": "What's space diagonal?", "a": "The longest straight line you can draw inside a cube — corner to opposite corner through the centre."}],
}

def calculate(inputs):
    (s,) = require(inputs, "side")
    positive(s, "side")
    return {"volume": round(s**3, 6), "surface_area": round(6*s*s, 6), "space_diagonal": round(s*math.sqrt(3), 6)}

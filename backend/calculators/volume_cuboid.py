"""Cuboid (rectangular prism) — volume, surface area, diagonal."""
import math
from ._base import positive, require

META = {
    "slug": "volume-cuboid",
    "name": "Cuboid Volume Calculator",
    "category": "geometry",
    "description": "Calculate volume, surface area, and space diagonal of a cuboid (rectangular box).",
    "formula": "V = l·w·h;  SA = 2(lw + lh + wh);  d = √(l²+w²+h²)",
    "fields": [
        {"name": "length", "label": "Length", "type": "number", "min": 0, "required": True, "placeholder": "10"},
        {"name": "width", "label": "Width", "type": "number", "min": 0, "required": True, "placeholder": "6"},
        {"name": "height", "label": "Height", "type": "number", "min": 0, "required": True, "placeholder": "4"},
    ],
    "outputs": [
        {"key": "volume", "label": "Volume", "format": "number"},
        {"key": "surface_area", "label": "Surface Area", "format": "number"},
        {"key": "space_diagonal", "label": "Space Diagonal", "format": "number"},
    ],
    "faq": [{"q": "Cuboid vs box?", "a": "Same shape. 'Cuboid' is the formal geometric name; a shoebox or a cargo container is also a cuboid."}],
}

def calculate(inputs):
    l, w, h = require(inputs, "length", "width", "height")
    positive(l, "length"); positive(w, "width"); positive(h, "height")
    return {
        "volume": round(l*w*h, 6),
        "surface_area": round(2*(l*w + l*h + w*h), 6),
        "space_diagonal": round(math.sqrt(l*l+w*w+h*h), 6),
    }

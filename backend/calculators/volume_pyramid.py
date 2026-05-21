"""Square pyramid — volume and surface area."""
import math
from ._base import positive, require

META = {
    "slug": "volume-pyramid",
    "name": "Square Pyramid Volume Calculator",
    "category": "geometry",
    "description": "Calculate volume, surface area, and slant height of a square-based pyramid.",
    "formula": "V = (1/3)·b²·h;  SA = b² + 2·b·ℓ;  ℓ = √(h² + (b/2)²)",
    "fields": [
        {"name": "base_side", "label": "Base Side Length", "type": "number", "min": 0, "required": True, "placeholder": "6"},
        {"name": "height", "label": "Perpendicular Height", "type": "number", "min": 0, "required": True, "placeholder": "8"},
    ],
    "outputs": [
        {"key": "volume", "label": "Volume", "format": "number"},
        {"key": "slant_height", "label": "Slant Height (face)", "format": "number"},
        {"key": "surface_area", "label": "Total Surface Area", "format": "number"},
    ],
    "faq": [{"q": "What about non-square pyramids?", "a": "For a regular polygon base, V = (1/3)·(base area)·h. This calculator handles the most common case: a square base."}],
}

def calculate(inputs):
    b, h = require(inputs, "base_side", "height")
    positive(b, "base_side"); positive(h, "height")
    slant = math.sqrt(h*h + (b/2)**2)
    return {
        "volume": round((1/3)*b*b*h, 6),
        "slant_height": round(slant, 6),
        "surface_area": round(b*b + 2*b*slant, 6),
    }

"""Rectangle — area, perimeter, diagonal."""
import math
from ._base import positive, require

META = {
    "slug": "area-rectangle",
    "name": "Rectangle Area Calculator",
    "category": "geometry",
    "description": "Calculate area, perimeter, and diagonal of a rectangle.",
    "formula": "A = l·w;  P = 2(l+w);  d = √(l²+w²)",
    "fields": [
        {"name": "length", "label": "Length", "type": "number", "min": 0, "required": True, "placeholder": "8"},
        {"name": "width", "label": "Width", "type": "number", "min": 0, "required": True, "placeholder": "5"},
    ],
    "outputs": [
        {"key": "area", "label": "Area", "format": "number"},
        {"key": "perimeter", "label": "Perimeter", "format": "number"},
        {"key": "diagonal", "label": "Diagonal", "format": "number"},
    ],
    "faq": [{"q": "What unit is area in?", "a": "Whatever unit you used for length, squared. e.g. m → m²."}],
}

def calculate(inputs):
    l, w = require(inputs, "length", "width")
    positive(l, "length"); positive(w, "width")
    return {"area": round(l*w, 6), "perimeter": round(2*(l+w), 6), "diagonal": round(math.sqrt(l*l+w*w), 6)}

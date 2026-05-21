"""Triangle — area from base/height or Heron's formula."""
import math
from ._base import positive, require, to_float

META = {
    "slug": "area-triangle",
    "name": "Triangle Area Calculator",
    "category": "geometry",
    "description": "Calculate triangle area from base × height, or from three sides using Heron's formula.",
    "formula": "A = ½·b·h  OR  A = √(s(s−a)(s−b)(s−c))",
    "fields": [
        {"name": "method", "label": "Method", "type": "select", "required": True, "default": "base_height",
         "options": [{"value": "base_height", "label": "Base × Height"}, {"value": "three_sides", "label": "Three Sides (Heron's)"}]},
        {"name": "base", "label": "Base (or side a)", "type": "number", "min": 0, "required": True, "placeholder": "10"},
        {"name": "height", "label": "Height (for base × height)", "type": "number", "min": 0, "required": False, "placeholder": "6"},
        {"name": "side_b", "label": "Side b (Heron's only)", "type": "number", "min": 0, "required": False, "placeholder": "7"},
        {"name": "side_c", "label": "Side c (Heron's only)", "type": "number", "min": 0, "required": False, "placeholder": "8"},
    ],
    "outputs": [
        {"key": "area", "label": "Area", "format": "number"},
        {"key": "perimeter", "label": "Perimeter (Heron's only)", "format": "number"},
    ],
    "faq": [{"q": "Heron's formula vs base × height?", "a": "Use base × height when you know one side and the perpendicular distance to the opposite vertex. Use Heron's when you only know the three side lengths."}],
}

def calculate(inputs):
    method = str(inputs.get("method", "base_height"))
    if method == "base_height":
        b, h = require(inputs, "base", "height")
        positive(b, "base"); positive(h, "height")
        return {"area": round(0.5*b*h, 6), "perimeter": None}
    if method == "three_sides":
        a = to_float(inputs.get("base"), "base"); b = to_float(inputs.get("side_b"), "side_b"); c = to_float(inputs.get("side_c"), "side_c")
        positive(a, "base"); positive(b, "side_b"); positive(c, "side_c")
        if a+b<=c or a+c<=b or b+c<=a:
            raise ValueError("Triangle inequality violated — these sides cannot form a triangle.")
        s = (a+b+c)/2
        return {"area": round(math.sqrt(s*(s-a)*(s-b)*(s-c)), 6), "perimeter": round(a+b+c, 6)}
    raise ValueError(f"Unknown method: {method}")

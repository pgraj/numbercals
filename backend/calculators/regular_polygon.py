"""Regular polygon — area and perimeter from number of sides and side length."""
import math
from ._base import positive, require, to_int

META = {
    "slug": "regular-polygon",
    "name": "Regular Polygon Calculator",
    "category": "geometry",
    "description": "Calculate area, perimeter, and interior angle of a regular polygon.",
    "formula": "A = (n·s²) / (4·tan(π/n));  P = n·s;  Interior angle = (n−2)·180°/n",
    "fields": [
        {"name": "num_sides", "label": "Number of sides (n)", "type": "number", "min": 3, "required": True, "placeholder": "6"},
        {"name": "side_length", "label": "Side length (s)", "type": "number", "min": 0, "required": True, "placeholder": "5"},
    ],
    "outputs": [
        {"key": "area", "label": "Area", "format": "number"},
        {"key": "perimeter", "label": "Perimeter", "format": "number"},
        {"key": "interior_angle_degrees", "label": "Interior Angle (°)", "format": "number"},
        {"key": "apothem", "label": "Apothem (centre to edge midpoint)", "format": "number"},
    ],
    "faq": [{"q": "What's the apothem?", "a": "The perpendicular distance from the centre of the polygon to the midpoint of any side. For a hexagon with side 5, apothem ≈ 4.33."}],
}

def calculate(inputs):
    n = to_int(inputs.get("num_sides"), "num_sides")
    (s,) = require(inputs, "side_length")
    if n < 3: raise ValueError("A polygon must have at least 3 sides.")
    positive(s, "side_length")
    area = (n * s*s) / (4 * math.tan(math.pi / n))
    apothem = s / (2 * math.tan(math.pi / n))
    return {
        "area": round(area, 6),
        "perimeter": round(n*s, 6),
        "interior_angle_degrees": round((n-2)*180/n, 4),
        "apothem": round(apothem, 6),
    }

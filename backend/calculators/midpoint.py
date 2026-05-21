"""Midpoint between two points (2D)."""
from ._base import require

META = {
    "slug": "midpoint",
    "name": "Midpoint Calculator",
    "category": "math",
    "description": "Find the midpoint of the line segment between two 2D points.",
    "formula": "M = ((x₁+x₂)/2, (y₁+y₂)/2)",
    "fields": [
        {"name": "x1", "label": "x₁", "type": "number", "required": True, "placeholder": "2"},
        {"name": "y1", "label": "y₁", "type": "number", "required": True, "placeholder": "3"},
        {"name": "x2", "label": "x₂", "type": "number", "required": True, "placeholder": "8"},
        {"name": "y2", "label": "y₂", "type": "number", "required": True, "placeholder": "11"},
    ],
    "outputs": [
        {"key": "midpoint_x", "label": "Midpoint x", "format": "number"},
        {"key": "midpoint_y", "label": "Midpoint y", "format": "number"},
    ],
    "faq": [{"q": "What's the midpoint used for?", "a": "Centre of a line segment, finding the centre of a circle from two endpoints of a diameter, perpendicular bisectors."}],
}

def calculate(inputs):
    x1, y1, x2, y2 = require(inputs, "x1", "y1", "x2", "y2")
    return {"midpoint_x": round((x1+x2)/2, 6), "midpoint_y": round((y1+y2)/2, 6)}

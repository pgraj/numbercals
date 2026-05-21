"""2D distance between two points."""
import math
from ._base import require

META = {
    "slug": "distance-formula",
    "name": "Distance Formula Calculator (2D)",
    "category": "math",
    "description": "Calculate the straight-line distance between two points in a 2D plane.",
    "formula": "d = √((x₂−x₁)² + (y₂−y₁)²)",
    "fields": [
        {"name": "x1", "label": "x₁", "type": "number", "required": True, "placeholder": "1"},
        {"name": "y1", "label": "y₁", "type": "number", "required": True, "placeholder": "2"},
        {"name": "x2", "label": "x₂", "type": "number", "required": True, "placeholder": "4"},
        {"name": "y2", "label": "y₂", "type": "number", "required": True, "placeholder": "6"},
    ],
    "outputs": [
        {"key": "distance", "label": "Distance", "format": "number"},
        {"key": "dx", "label": "Δx (x₂ − x₁)", "format": "number"},
        {"key": "dy", "label": "Δy (y₂ − y₁)", "format": "number"},
    ],
    "faq": [{"q": "How does this relate to Pythagoras?", "a": "It IS Pythagoras — the distance is the hypotenuse of a right triangle with legs Δx and Δy."}],
}

def calculate(inputs):
    x1, y1, x2, y2 = require(inputs, "x1", "y1", "x2", "y2")
    dx, dy = x2-x1, y2-y1
    return {"distance": round(math.sqrt(dx*dx + dy*dy), 6), "dx": round(dx, 6), "dy": round(dy, 6)}

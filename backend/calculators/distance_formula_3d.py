"""3D distance between two points."""
import math
from ._base import require

META = {
    "slug": "distance-formula-3d",
    "name": "Distance Formula Calculator (3D)",
    "category": "math",
    "description": "Calculate the straight-line distance between two points in 3D space.",
    "formula": "d = √((x₂−x₁)² + (y₂−y₁)² + (z₂−z₁)²)",
    "fields": [
        {"name": "x1", "label": "x₁", "type": "number", "required": True, "placeholder": "0"},
        {"name": "y1", "label": "y₁", "type": "number", "required": True, "placeholder": "0"},
        {"name": "z1", "label": "z₁", "type": "number", "required": True, "placeholder": "0"},
        {"name": "x2", "label": "x₂", "type": "number", "required": True, "placeholder": "3"},
        {"name": "y2", "label": "y₂", "type": "number", "required": True, "placeholder": "4"},
        {"name": "z2", "label": "z₂", "type": "number", "required": True, "placeholder": "12"},
    ],
    "outputs": [{"key": "distance", "label": "Distance", "format": "number"}],
    "faq": [{"q": "Where would I use 3D distance?", "a": "3D modelling, robotics, physics simulations, video games, GPS-with-altitude, drone trajectory planning."}],
}

def calculate(inputs):
    x1, y1, z1, x2, y2, z2 = require(inputs, "x1", "y1", "z1", "x2", "y2", "z2")
    return {"distance": round(math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2), 6)}

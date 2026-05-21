"""Slope and equation of a line through two points."""
import math
from ._base import require

META = {
    "slug": "slope",
    "name": "Slope Calculator",
    "category": "math",
    "description": "Calculate the slope, y-intercept, and equation of the line through two points.",
    "formula": "m = (y₂ − y₁) / (x₂ − x₁);  y = mx + b",
    "fields": [
        {"name": "x1", "label": "x₁", "type": "number", "required": True, "placeholder": "1"},
        {"name": "y1", "label": "y₁", "type": "number", "required": True, "placeholder": "2"},
        {"name": "x2", "label": "x₂", "type": "number", "required": True, "placeholder": "4"},
        {"name": "y2", "label": "y₂", "type": "number", "required": True, "placeholder": "11"},
    ],
    "outputs": [
        {"key": "slope", "label": "Slope (m)", "format": "number"},
        {"key": "y_intercept", "label": "y-intercept (b)", "format": "number"},
        {"key": "angle_degrees", "label": "Angle with x-axis (°)", "format": "number"},
        {"key": "equation", "label": "Line Equation", "format": "text"},
    ],
    "faq": [
        {"q": "What's a vertical line?", "a": "If x₁ = x₂, slope is undefined (the line is vertical). The calculator returns an error in that case."},
        {"q": "What's the angle?", "a": "The angle the line makes with the positive x-axis, measured counter-clockwise. A slope of 1 = 45°."},
    ],
}

def calculate(inputs):
    x1, y1, x2, y2 = require(inputs, "x1", "y1", "x2", "y2")
    if x1 == x2:
        raise ValueError("Slope is undefined for a vertical line (x₁ = x₂).")
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    angle = math.degrees(math.atan(m))
    sign = "+" if b >= 0 else "-"
    eq = f"y = {round(m, 4)}x {sign} {abs(round(b, 4))}"
    return {
        "slope": round(m, 6),
        "y_intercept": round(b, 6),
        "angle_degrees": round(angle, 4),
        "equation": eq,
    }

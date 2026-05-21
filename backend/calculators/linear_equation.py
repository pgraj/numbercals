"""Linear Equation Solver. ax + b = 0 → x = -b/a"""
from typing import Any, Dict
from ._base import require

META = {
    "slug": "linear-equation",
    "name": "Linear Equation Solver",
    "category": "math",
    "description": "Solve ax + b = 0 for x.",
    "formula": "x = −b / a",
    "fields": [
        {"name": "a", "label": "a (coefficient of x)", "type": "number", "required": True, "placeholder": "2"},
        {"name": "b", "label": "b (constant)", "type": "number", "required": True, "placeholder": "-6"},
    ],
    "outputs": [{"key": "x", "label": "x", "format": "number"}],
    "faq": [{"q": "What if a = 0?", "a": "Then it's not linear. If b also = 0, every x is a solution; if b ≠ 0, no solution exists."}],
}

def calculate(inputs):
    a, b = require(inputs, "a", "b")
    if a == 0:
        if b == 0: raise ValueError("Infinite solutions (0 = 0).")
        raise ValueError("No solution (this is not a valid linear equation when a = 0 and b ≠ 0).")
    return {"x": round(-b / a, 6)}

"""Quadratic Equation Solver. ax² + bx + c = 0"""
import cmath
from typing import Any, Dict
from ._base import require

META = {
    "slug": "quadratic",
    "name": "Quadratic Equation Solver",
    "category": "math",
    "description": "Solve ax² + bx + c = 0 for both real and complex roots.",
    "formula": "x = (−b ± √(b² − 4ac)) / 2a",
    "fields": [
        {"name": "a", "label": "a", "type": "number", "required": True, "placeholder": "1"},
        {"name": "b", "label": "b", "type": "number", "required": True, "placeholder": "-3"},
        {"name": "c", "label": "c", "type": "number", "required": True, "placeholder": "2"},
    ],
    "outputs": [
        {"key": "discriminant", "label": "Discriminant", "format": "number"},
        {"key": "root1", "label": "Root 1", "format": "text"},
        {"key": "root2", "label": "Root 2", "format": "text"},
        {"key": "nature", "label": "Nature of Roots", "format": "text"},
    ],
    "faq": [{"q": "What does the discriminant tell me?", "a": "b²−4ac. Positive: two real roots. Zero: one real (repeated) root. Negative: two complex conjugate roots."}],
}

def _fmt(x: complex) -> str:
    if abs(x.imag) < 1e-12:
        return str(round(x.real, 6))
    return f"{round(x.real, 6)} {'+' if x.imag >= 0 else '-'} {abs(round(x.imag, 6))}i"

def calculate(inputs):
    a, b, c = require(inputs, "a", "b", "c")
    if a == 0: raise ValueError("'a' cannot be 0 (this would be a linear equation, not quadratic).")
    disc = b * b - 4 * a * c
    sqrt_d = cmath.sqrt(disc)
    r1 = (-b + sqrt_d) / (2 * a); r2 = (-b - sqrt_d) / (2 * a)
    if disc > 0: nature = "Two distinct real roots"
    elif disc == 0: nature = "One repeated real root"
    else: nature = "Two complex conjugate roots"
    return {"discriminant": disc, "root1": _fmt(r1), "root2": _fmt(r2), "nature": nature}

"""Ratio Calculator — simplify a:b and solve a:b = c:?"""
from math import gcd
from typing import Any, Dict
from ._base import positive, to_float, to_int

META = {
    "slug": "ratio",
    "name": "Ratio Calculator",
    "category": "math",
    "description": "Simplify a ratio and solve missing terms in proportional ratios.",
    "formula": "a:b = c:d  =>  d = b·c / a",
    "fields": [
        {"name": "a", "label": "A", "type": "number", "required": True, "placeholder": "12"},
        {"name": "b", "label": "B", "type": "number", "required": True, "placeholder": "18"},
        {"name": "c", "label": "C (optional, for proportion)", "type": "number", "required": False, "placeholder": "30"},
    ],
    "outputs": [
        {"key": "simplified", "label": "Simplified Ratio", "format": "text"},
        {"key": "missing_d", "label": "Missing D (when C given)", "format": "number"},
    ],
    "faq": [{"q": "What's the difference between ratio and proportion?", "a": "A ratio compares two quantities. A proportion states that two ratios are equal."}],
}

def calculate(inputs):
    a_raw = inputs.get("a"); b_raw = inputs.get("b")
    a = to_int(a_raw, "a"); b = to_int(b_raw, "b")
    if b == 0:
        raise ValueError("B cannot be zero.")
    g = gcd(abs(a), abs(b)) or 1
    simplified = f"{a // g}:{b // g}"
    result = {"simplified": simplified, "missing_d": None}
    if inputs.get("c") not in (None, ""):
        c = to_float(inputs.get("c"), "c")
        if a == 0: raise ValueError("Cannot solve proportion with A = 0.")
        result["missing_d"] = round(b * c / a, 6)
    return result

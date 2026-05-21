"""Percentage Calculator — three common modes."""
from typing import Any, Dict
from ._base import positive, require

META = {
    "slug": "percentage",
    "name": "Percentage Calculator",
    "category": "math",
    "description": "Solve the three core percentage problems: what is X% of Y, X is what % of Y, and percentage increase/decrease.",
    "formula": "value × percent / 100",
    "fields": [
        {"name": "mode", "label": "Mode", "type": "select", "required": True, "default": "of",
         "options": [
             {"value": "of", "label": "What is X% of Y?"},
             {"value": "is_what_percent", "label": "X is what % of Y?"},
             {"value": "change", "label": "% change from X to Y?"},
         ]},
        {"name": "x", "label": "X", "type": "number", "required": True, "placeholder": "20"},
        {"name": "y", "label": "Y", "type": "number", "required": True, "placeholder": "150"},
    ],
    "outputs": [{"key": "result", "label": "Result", "format": "number"}],
    "faq": [{"q": "How do I reverse a percentage?", "a": "If A is 80% of B, then B = A / 0.80. Use mode 'X is what % of Y' to verify."}],
}

def calculate(inputs):
    mode = str(inputs.get("mode", "of"))
    x, y = require(inputs, "x", "y")
    if mode == "of":
        return {"result": round(x * y / 100, 4)}
    if mode == "is_what_percent":
        positive(y, "y")
        return {"result": round(x / y * 100, 4)}
    if mode == "change":
        positive(x, "x")
        return {"result": round((y - x) / x * 100, 4)}
    raise ValueError(f"Unknown mode: {mode}")

"""Fraction Calculator — add, subtract, multiply, divide two fractions; return simplified result."""
from math import gcd
from typing import Any, Dict
from ._base import to_int

META = {
    "slug": "fraction",
    "name": "Fraction Calculator",
    "category": "math",
    "description": "Add, subtract, multiply, or divide two fractions and get a simplified result.",
    "formula": "Operates on a/b op c/d, returns p/q in lowest terms.",
    "fields": [
        {"name": "a", "label": "Numerator 1", "type": "number", "required": True, "placeholder": "1"},
        {"name": "b", "label": "Denominator 1", "type": "number", "required": True, "placeholder": "2"},
        {"name": "op", "label": "Operation", "type": "select", "required": True, "default": "+",
         "options": [{"value": "+", "label": "+"}, {"value": "-", "label": "−"}, {"value": "*", "label": "×"}, {"value": "/", "label": "÷"}]},
        {"name": "c", "label": "Numerator 2", "type": "number", "required": True, "placeholder": "1"},
        {"name": "d", "label": "Denominator 2", "type": "number", "required": True, "placeholder": "3"},
    ],
    "outputs": [
        {"key": "result_fraction", "label": "Result (fraction)", "format": "text"},
        {"key": "result_decimal", "label": "Result (decimal)", "format": "number"},
    ],
    "faq": [{"q": "What does 'simplified' mean?", "a": "Both numerator and denominator share no common factor greater than 1 — e.g. 6/8 simplifies to 3/4."}],
}

def calculate(inputs):
    a = to_int(inputs.get("a"), "a"); b = to_int(inputs.get("b"), "b")
    c = to_int(inputs.get("c"), "c"); d = to_int(inputs.get("d"), "d")
    op = str(inputs.get("op", "+"))
    if b == 0 or d == 0:
        raise ValueError("Denominators must be non-zero.")
    if op == "+":
        num, den = a * d + c * b, b * d
    elif op == "-":
        num, den = a * d - c * b, b * d
    elif op == "*":
        num, den = a * c, b * d
    elif op == "/":
        if c == 0: raise ValueError("Cannot divide by zero fraction.")
        num, den = a * d, b * c
    else:
        raise ValueError(f"Unknown operation: {op}")
    g = gcd(abs(num), abs(den)) or 1
    num //= g; den //= g
    if den < 0:
        num, den = -num, -den
    return {"result_fraction": f"{num}/{den}", "result_decimal": round(num / den, 6)}

"""Pythagoras' Theorem — solve for hypotenuse or a leg of a right triangle."""
import math
from ._base import to_float

META = {
    "slug": "pythagoras",
    "name": "Pythagoras' Theorem Calculator",
    "category": "math",
    "description": "Solve a² + b² = c² for any side of a right triangle.",
    "formula": "a² + b² = c²",
    "fields": [
        {"name": "solve_for", "label": "Solve for", "type": "select", "required": True, "default": "c",
         "options": [
             {"value": "c", "label": "Hypotenuse (c) — given a and b"},
             {"value": "a", "label": "Leg a — given b and c"},
             {"value": "b", "label": "Leg b — given a and c"},
         ]},
        {"name": "a", "label": "Side a", "type": "number", "min": 0, "required": False, "placeholder": "3"},
        {"name": "b", "label": "Side b", "type": "number", "min": 0, "required": False, "placeholder": "4"},
        {"name": "c", "label": "Hypotenuse c", "type": "number", "min": 0, "required": False, "placeholder": "5"},
    ],
    "outputs": [
        {"key": "result", "label": "Result", "format": "number"},
        {"key": "solved_for", "label": "Solved For", "format": "text"},
    ],
    "faq": [
        {"q": "What's a right triangle?", "a": "A triangle with one 90° angle. The side opposite the right angle is the hypotenuse — always the longest side."},
        {"q": "Famous Pythagorean triples?", "a": "(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25). Integer-sided right triangles."},
    ],
}

def calculate(inputs):
    solve = str(inputs.get("solve_for", "c"))
    if solve == "c":
        a = to_float(inputs.get("a"), "a"); b = to_float(inputs.get("b"), "b")
        if a < 0 or b < 0: raise ValueError("Sides must be non-negative.")
        return {"result": round(math.sqrt(a*a + b*b), 6), "solved_for": "Hypotenuse c"}
    if solve == "a":
        b = to_float(inputs.get("b"), "b"); c = to_float(inputs.get("c"), "c")
        if b < 0 or c < 0: raise ValueError("Sides must be non-negative.")
        if c <= b: raise ValueError("Hypotenuse must be longer than the given leg.")
        return {"result": round(math.sqrt(c*c - b*b), 6), "solved_for": "Leg a"}
    if solve == "b":
        a = to_float(inputs.get("a"), "a"); c = to_float(inputs.get("c"), "c")
        if a < 0 or c < 0: raise ValueError("Sides must be non-negative.")
        if c <= a: raise ValueError("Hypotenuse must be longer than the given leg.")
        return {"result": round(math.sqrt(c*c - a*a), 6), "solved_for": "Leg b"}
    raise ValueError(f"Unknown solve_for: {solve}")

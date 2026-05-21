"""Combination Calculator. nCr = n! / (r!(n−r)!)"""
import math
from typing import Any, Dict
from ._base import to_int

META = {
    "slug": "combination",
    "name": "Combination Calculator",
    "category": "math",
    "description": "Calculate the number of unordered selections (combinations) of r items from n.",
    "formula": "nCr = n! / (r! · (n − r)!)",
    "fields": [
        {"name": "n", "label": "n (total items)", "type": "number", "min": 0, "required": True, "placeholder": "10"},
        {"name": "r", "label": "r (items chosen)", "type": "number", "min": 0, "required": True, "placeholder": "3"},
    ],
    "outputs": [{"key": "combinations", "label": "Combinations (nCr)", "format": "number"}],
    "faq": [{"q": "When do I use combinations?", "a": "When order doesn't matter — e.g. picking 5 cards from a deck (poker hands) or choosing committee members."}],
}

def calculate(inputs):
    n = to_int(inputs.get("n"), "n"); r = to_int(inputs.get("r"), "r")
    if n < 0 or r < 0: raise ValueError("n and r must be non-negative.")
    if r > n: raise ValueError("r cannot exceed n.")
    return {"combinations": math.comb(n, r)}

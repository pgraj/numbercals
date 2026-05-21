"""Permutation Calculator. nPr = n! / (n−r)!"""
import math
from typing import Any, Dict
from ._base import to_int

META = {
    "slug": "permutation",
    "name": "Permutation Calculator",
    "category": "math",
    "description": "Calculate the number of ordered arrangements (permutations) of r items from n.",
    "formula": "nPr = n! / (n − r)!",
    "fields": [
        {"name": "n", "label": "n (total items)", "type": "number", "min": 0, "required": True, "placeholder": "10"},
        {"name": "r", "label": "r (items chosen)", "type": "number", "min": 0, "required": True, "placeholder": "3"},
    ],
    "outputs": [{"key": "permutations", "label": "Permutations (nPr)", "format": "number"}],
    "faq": [{"q": "Permutation vs combination?", "a": "Permutations count order (ABC ≠ BCA); combinations don't (ABC = BCA)."}],
}

def calculate(inputs):
    n = to_int(inputs.get("n"), "n"); r = to_int(inputs.get("r"), "r")
    if n < 0 or r < 0: raise ValueError("n and r must be non-negative.")
    if r > n: raise ValueError("r cannot exceed n.")
    return {"permutations": math.perm(n, r)}

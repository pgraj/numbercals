"""LCM Calculator. Accepts comma-separated integers."""
import math
from functools import reduce
from typing import Any, Dict

META = {
    "slug": "lcm",
    "name": "LCM Calculator",
    "category": "math",
    "description": "Find the least common multiple of two or more integers.",
    "formula": "LCM(a, b) = |a·b| / GCD(a, b)",
    "fields": [{"name": "numbers", "label": "Integers (comma- or space-separated)", "type": "text", "required": True, "placeholder": "12, 18, 24"}],
    "outputs": [{"key": "lcm", "label": "LCM", "format": "number"}],
    "faq": [{"q": "What is LCM used for?", "a": "Adding fractions (common denominator), scheduling repeating events, music theory."}],
}

def parse_ints(text):
    if not text: raise ValueError("Please enter at least two integers.")
    items = str(text).replace(",", " ").split()
    nums = []
    for t in items:
        try:
            f = float(t)
            if f != int(f): raise ValueError
            nums.append(int(f))
        except ValueError: raise ValueError(f"'{t}' is not an integer.")
    if len(nums) < 2: raise ValueError("Please enter at least two integers.")
    return nums

def calculate(inputs):
    nums = parse_ints(inputs.get("numbers"))
    return {"lcm": reduce(math.lcm, nums)}

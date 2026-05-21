"""GCD (Greatest Common Divisor) Calculator."""
import math
from functools import reduce
from typing import Any, Dict
from .lcm import parse_ints

META = {
    "slug": "gcd",
    "name": "GCD Calculator",
    "category": "math",
    "description": "Find the greatest common divisor of two or more integers.",
    "formula": "Euclidean algorithm",
    "fields": [{"name": "numbers", "label": "Integers (comma- or space-separated)", "type": "text", "required": True, "placeholder": "48, 36, 24"}],
    "outputs": [{"key": "gcd", "label": "GCD", "format": "number"}],
    "faq": [{"q": "GCD vs LCM?", "a": "GCD is the largest integer that divides all the numbers. LCM is the smallest integer divisible by all."}],
}

def calculate(inputs):
    nums = parse_ints(inputs.get("numbers"))
    return {"gcd": reduce(math.gcd, nums)}

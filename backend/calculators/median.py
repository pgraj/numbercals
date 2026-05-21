"""Median Calculator."""
from typing import Any, Dict
from .average import parse_numbers

META = {
    "slug": "median",
    "name": "Median Calculator",
    "category": "math",
    "description": "Find the middle value of a list of numbers.",
    "formula": "For sorted list of n values: if n odd, middle; if even, average of two middle.",
    "fields": [{"name": "numbers", "label": "Numbers", "type": "text", "required": True, "placeholder": "3, 1, 4, 1, 5, 9, 2, 6"}],
    "outputs": [{"key": "median", "label": "Median", "format": "number"}],
    "faq": [{"q": "When is median better than mean?", "a": "When the data has outliers or is skewed — e.g. household income, where a few billionaires would skew the mean."}],
}

def calculate(inputs):
    nums = sorted(parse_numbers(inputs.get("numbers")))
    n = len(nums)
    mid = n // 2
    med = nums[mid] if n % 2 else (nums[mid - 1] + nums[mid]) / 2
    return {"median": round(med, 6)}

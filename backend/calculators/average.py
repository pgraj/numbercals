"""Average (Mean) Calculator. Accepts comma- or space-separated numbers."""
from typing import Any, Dict

META = {
    "slug": "average",
    "name": "Average Calculator",
    "category": "math",
    "description": "Compute the arithmetic mean of a list of numbers.",
    "formula": "mean = Σx / n",
    "fields": [{"name": "numbers", "label": "Numbers (comma- or space-separated)", "type": "text", "required": True, "placeholder": "5, 10, 15, 20, 25"}],
    "outputs": [
        {"key": "mean", "label": "Average (Mean)", "format": "number"},
        {"key": "count", "label": "Count", "format": "number"},
        {"key": "sum", "label": "Sum", "format": "number"},
    ],
    "faq": [{"q": "Mean vs median?", "a": "Mean is the arithmetic average; median is the middle value. Median is more robust to outliers."}],
}

def parse_numbers(text: Any) -> list:
    if text is None or text == "":
        raise ValueError("Please enter at least one number.")
    if isinstance(text, list):
        items = text
    else:
        items = str(text).replace(",", " ").split()
    nums = []
    for t in items:
        try: nums.append(float(t))
        except ValueError: raise ValueError(f"Could not parse '{t}' as a number.")
    if not nums:
        raise ValueError("Please enter at least one number.")
    return nums

def calculate(inputs):
    nums = parse_numbers(inputs.get("numbers"))
    s = sum(nums)
    return {"mean": round(s / len(nums), 6), "count": len(nums), "sum": round(s, 6)}

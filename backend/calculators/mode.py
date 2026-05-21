"""Mode Calculator."""
from collections import Counter
from typing import Any, Dict
from .average import parse_numbers

META = {
    "slug": "mode",
    "name": "Mode Calculator",
    "category": "math",
    "description": "Find the most frequently occurring value(s) in a dataset.",
    "formula": "The value(s) with highest frequency.",
    "fields": [{"name": "numbers", "label": "Numbers", "type": "text", "required": True, "placeholder": "1, 2, 2, 3, 3, 3, 4"}],
    "outputs": [
        {"key": "modes", "label": "Mode(s)", "format": "text"},
        {"key": "frequency", "label": "Frequency", "format": "number"},
    ],
    "faq": [{"q": "Can a dataset have multiple modes?", "a": "Yes — if two or more values tie for highest frequency. This is called bimodal or multimodal."}],
}

def calculate(inputs):
    nums = parse_numbers(inputs.get("numbers"))
    counts = Counter(nums)
    if not counts: raise ValueError("No data.")
    top_freq = max(counts.values())
    modes = sorted([v for v, c in counts.items() if c == top_freq])
    return {"modes": ", ".join(str(m) for m in modes), "frequency": top_freq}

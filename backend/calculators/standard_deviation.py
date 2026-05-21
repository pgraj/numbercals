"""Standard Deviation Calculator. Reports both population and sample SD."""
import math
from typing import Any, Dict
from .average import parse_numbers

META = {
    "slug": "standard-deviation",
    "name": "Standard Deviation Calculator",
    "category": "math",
    "description": "Calculate population and sample standard deviation and variance.",
    "formula": "σ = √(Σ(xᵢ − μ)² / n);   s = √(Σ(xᵢ − x̄)² / (n−1))",
    "fields": [{"name": "numbers", "label": "Numbers", "type": "text", "required": True, "placeholder": "2, 4, 4, 4, 5, 5, 7, 9"}],
    "outputs": [
        {"key": "mean", "label": "Mean", "format": "number"},
        {"key": "population_sd", "label": "Population SD (σ)", "format": "number"},
        {"key": "sample_sd", "label": "Sample SD (s)", "format": "number"},
        {"key": "population_variance", "label": "Population Variance (σ²)", "format": "number"},
        {"key": "sample_variance", "label": "Sample Variance (s²)", "format": "number"},
    ],
    "faq": [{"q": "Population vs sample SD?", "a": "Use population when you have all data points; use sample (n−1 in denominator) when estimating from a subset."}],
}

def calculate(inputs):
    nums = parse_numbers(inputs.get("numbers"))
    n = len(nums); mean = sum(nums) / n
    sq = sum((x - mean) ** 2 for x in nums)
    pop_var = sq / n
    samp_var = sq / (n - 1) if n > 1 else 0
    return {
        "mean": round(mean, 6),
        "population_sd": round(math.sqrt(pop_var), 6),
        "sample_sd": round(math.sqrt(samp_var), 6),
        "population_variance": round(pop_var, 6),
        "sample_variance": round(samp_var, 6),
    }

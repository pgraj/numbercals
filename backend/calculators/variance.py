"""Variance Calculator. Wraps standard_deviation."""
from typing import Any, Dict
from . import standard_deviation as sd_mod

META = {
    "slug": "variance",
    "name": "Variance Calculator",
    "category": "math",
    "description": "Calculate the variance of a dataset.",
    "formula": "Var = Σ(xᵢ − mean)² / n  (or /(n−1) for sample)",
    "fields": [{"name": "numbers", "label": "Numbers", "type": "text", "required": True, "placeholder": "2, 4, 4, 4, 5, 5, 7, 9"}],
    "outputs": [
        {"key": "population_variance", "label": "Population Variance", "format": "number"},
        {"key": "sample_variance", "label": "Sample Variance", "format": "number"},
    ],
    "faq": [{"q": "Variance vs SD?", "a": "SD is the square root of variance; SD is in the same units as the data, variance in squared units."}],
}

def calculate(inputs):
    r = sd_mod.calculate(inputs)
    return {"population_variance": r["population_variance"], "sample_variance": r["sample_variance"]}

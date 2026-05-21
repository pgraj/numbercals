"""Probability Calculator. P(event) = favorable / total"""
from typing import Any, Dict
from ._base import non_negative, require

META = {
    "slug": "probability",
    "name": "Probability Calculator",
    "category": "math",
    "description": "Calculate single-event probability and the complement.",
    "formula": "P(A) = favorable / total",
    "fields": [
        {"name": "favorable", "label": "Favorable Outcomes", "type": "number", "min": 0, "required": True, "placeholder": "1"},
        {"name": "total", "label": "Total Possible Outcomes", "type": "number", "min": 1, "required": True, "placeholder": "6"},
    ],
    "outputs": [
        {"key": "probability", "label": "Probability", "format": "number"},
        {"key": "probability_percent", "label": "Probability (%)", "format": "percent"},
        {"key": "complement_percent", "label": "Probability NOT (%)", "format": "percent"},
        {"key": "odds", "label": "Odds (favorable:unfavorable)", "format": "text"},
    ],
    "faq": [{"q": "Probability vs odds?", "a": "Probability = favorable/total. Odds = favorable:unfavorable. P=0.25 → odds 1:3."}],
}

def calculate(inputs):
    fav, total = require(inputs, "favorable", "total")
    non_negative(fav, "favorable")
    if total <= 0: raise ValueError("'total' must be greater than 0.")
    if fav > total: raise ValueError("'favorable' cannot exceed 'total'.")
    p = fav / total
    unfav = total - fav
    return {
        "probability": round(p, 6),
        "probability_percent": round(p * 100, 4),
        "complement_percent": round((1 - p) * 100, 4),
        "odds": f"{int(fav)}:{int(unfav)}",
    }

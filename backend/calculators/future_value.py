"""Future Value Calculator. FV = PV × (1 + r)^n"""
from typing import Any, Dict
from ._base import non_negative, require

META = {
    "slug": "future-value",
    "name": "Future Value Calculator",
    "category": "finance",
    "description": "Project the future value of a lump-sum investment.",
    "formula": "FV = PV × (1 + r)^n",
    "fields": [
        {"name": "present_value", "label": "Present Value", "type": "number", "min": 0, "required": True, "placeholder": "10000"},
        {"name": "annual_rate", "label": "Annual Rate (%)", "type": "number", "min": 0, "required": True, "placeholder": "7"},
        {"name": "years", "label": "Years", "type": "number", "min": 0, "required": True, "placeholder": "10"},
    ],
    "outputs": [
        {"key": "future_value", "label": "Future Value", "format": "currency"},
        {"key": "interest_earned", "label": "Interest Earned", "format": "currency"},
    ],
    "faq": [{"q": "Why does FV grow non-linearly?", "a": "Because each period's interest itself earns interest in the next — the compounding effect."}],
}

def calculate(inputs):
    pv, r, n = require(inputs, "present_value", "annual_rate", "years")
    non_negative(pv, "present_value"); non_negative(r, "annual_rate"); non_negative(n, "years")
    fv = pv * ((1 + r/100) ** n)
    return {"future_value": round(fv, 2), "interest_earned": round(fv - pv, 2)}

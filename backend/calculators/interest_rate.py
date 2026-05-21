"""Interest Rate Calculator — solve for rate given P, FV, n. r = (FV/P)^(1/n) − 1"""
from typing import Any, Dict
from ._base import positive, require

META = {
    "slug": "interest-rate",
    "name": "Interest Rate Calculator",
    "category": "finance",
    "description": "Solve for the annual interest rate given starting amount, ending amount, and time.",
    "formula": "r = (FV / PV)^(1/n) − 1",
    "fields": [
        {"name": "present_value", "label": "Present Value", "type": "number", "min": 0, "required": True, "placeholder": "10000"},
        {"name": "future_value", "label": "Future Value", "type": "number", "min": 0, "required": True, "placeholder": "15000"},
        {"name": "years", "label": "Years", "type": "number", "min": 0, "required": True, "placeholder": "5"},
    ],
    "outputs": [
        {"key": "annual_rate_percent", "label": "Implied Annual Rate (%)", "format": "percent"},
    ],
    "faq": [{"q": "How is this different from CAGR?", "a": "It's the same calculation — both solve for the constant rate that takes PV to FV over n years."}],
}

def calculate(inputs):
    pv, fv, n = require(inputs, "present_value", "future_value", "years")
    positive(pv, "present_value"); positive(n, "years")
    r = ((fv / pv) ** (1 / n) - 1) * 100
    return {"annual_rate_percent": round(r, 4)}

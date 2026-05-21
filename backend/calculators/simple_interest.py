"""Simple Interest Calculator.

Formula: SI = (P × R × T) / 100
Where:
  P = Principal amount
  R = Annual rate of interest (%)
  T = Time in years
"""
from typing import Any, Dict

from ._base import non_negative, require

META = {
    "slug": "simple-interest",
    "name": "Simple Interest Calculator",
    "category": "finance",
    "description": "Calculate simple interest earned on a principal amount over time.",
    "formula": "SI = (P × R × T) / 100",
    "fields": [
        {"name": "principal", "label": "Principal Amount", "type": "number", "min": 0, "required": True, "placeholder": "10000"},
        {"name": "rate", "label": "Annual Interest Rate (%)", "type": "number", "min": 0, "required": True, "placeholder": "5"},
        {"name": "time", "label": "Time (years)", "type": "number", "min": 0, "required": True, "placeholder": "3"},
    ],
    "outputs": [
        {"key": "interest", "label": "Simple Interest", "format": "currency"},
        {"key": "total_amount", "label": "Total Amount (P + SI)", "format": "currency"},
    ],
    "faq": [
        {"q": "What is simple interest?", "a": "Simple interest is interest calculated only on the original principal, not on accumulated interest from prior periods."},
        {"q": "When is simple interest used?", "a": "It's used for short-term loans, some auto loans, and most personal loans where interest does not compound."},
    ],
}


def calculate(inputs: Dict[str, Any]) -> Dict[str, Any]:
    p, r, t = require(inputs, "principal", "rate", "time")
    non_negative(p, "principal")
    non_negative(r, "rate")
    non_negative(t, "time")

    interest = (p * r * t) / 100
    total = p + interest
    return {
        "interest": round(interest, 2),
        "total_amount": round(total, 2),
    }

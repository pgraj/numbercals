"""Compound Interest Calculator.

Formula: A = P × (1 + r/n)^(n×t)
  P = principal
  r = annual rate (decimal, e.g. 5% -> 0.05)
  n = compounding periods per year
  t = time in years
Interest = A - P
"""
from typing import Any, Dict

from ._base import non_negative, positive, require, to_int

META = {
    "slug": "compound-interest",
    "name": "Compound Interest Calculator",
    "category": "finance",
    "description": "Calculate compound interest on an investment with configurable compounding frequency.",
    "formula": "A = P × (1 + r/n)^(n·t)",
    "fields": [
        {"name": "principal", "label": "Principal Amount", "type": "number", "min": 0, "required": True, "placeholder": "10000"},
        {"name": "rate", "label": "Annual Interest Rate (%)", "type": "number", "min": 0, "required": True, "placeholder": "8"},
        {"name": "time", "label": "Time (years)", "type": "number", "min": 0, "required": True, "placeholder": "5"},
        {"name": "compounds_per_year", "label": "Compounding Frequency (per year)", "type": "select",
         "options": [
             {"value": 1, "label": "Annually (1)"},
             {"value": 2, "label": "Semi-annually (2)"},
             {"value": 4, "label": "Quarterly (4)"},
             {"value": 12, "label": "Monthly (12)"},
             {"value": 365, "label": "Daily (365)"},
         ],
         "required": True, "default": 12},
    ],
    "outputs": [
        {"key": "final_amount", "label": "Final Amount (A)", "format": "currency"},
        {"key": "interest_earned", "label": "Total Interest Earned", "format": "currency"},
    ],
    "faq": [
        {"q": "How is compound interest different from simple interest?", "a": "Compound interest is calculated on principal plus previously accumulated interest, so it grows faster over time."},
        {"q": "Which compounding frequency gives the best return?", "a": "More frequent compounding (e.g. daily) yields slightly more than annual, but the difference shrinks as frequency increases."},
    ],
}


def calculate(inputs: Dict[str, Any]) -> Dict[str, Any]:
    p, r, t = require(inputs, "principal", "rate", "time")
    n = to_int(inputs.get("compounds_per_year", 1), "compounds_per_year")
    non_negative(p, "principal")
    non_negative(r, "rate")
    non_negative(t, "time")
    positive(n, "compounds_per_year")

    rate_decimal = r / 100
    final_amount = p * ((1 + rate_decimal / n) ** (n * t))
    interest = final_amount - p
    return {
        "final_amount": round(final_amount, 2),
        "interest_earned": round(interest, 2),
    }

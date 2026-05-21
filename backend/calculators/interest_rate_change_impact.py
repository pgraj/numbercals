"""Interest Rate Change Impact Calculator.

Compares EMI/monthly payment at two interest rates — the impact of rate hikes/cuts.
"""
from typing import Any, Dict
from ._base import non_negative, positive, require, to_int

META = {
    "slug": "interest-rate-change-impact",
    "name": "Interest Rate Change Impact Calculator",
    "category": "finance",
    "description": "Calculate how a change in interest rate affects your monthly mortgage/loan payment and total cost over the life of the loan.",
    "formula": "ΔEMI = EMI(new_rate) − EMI(old_rate)",
    "fields": [
        {"name": "loan_amount", "label": "Loan Amount", "type": "number", "min": 0, "required": True, "placeholder": "500000"},
        {"name": "current_rate", "label": "Current Interest Rate (%)", "type": "number", "min": 0, "required": True, "placeholder": "6.25"},
        {"name": "new_rate", "label": "New Interest Rate (%)", "type": "number", "min": 0, "required": True, "placeholder": "7"},
        {"name": "term_years", "label": "Loan Term (years)", "type": "number", "min": 1, "required": True, "placeholder": "25"},
    ],
    "outputs": [
        {"key": "current_emi", "label": "Current Monthly Payment", "format": "currency"},
        {"key": "new_emi", "label": "New Monthly Payment", "format": "currency"},
        {"key": "monthly_difference", "label": "Monthly Difference", "format": "currency"},
        {"key": "annual_difference", "label": "Annual Difference", "format": "currency"},
        {"key": "lifetime_difference", "label": "Lifetime Difference", "format": "currency"},
        {"key": "direction", "label": "Impact", "format": "text"},
    ],
    "faq": [
        {"q": "How sensitive is a mortgage to rates?", "a": "Very. On a 25-year $500K loan, each 0.25% rate change is roughly $75–80/month — about $22,500 over the life of the loan."},
    ],
}


def _emi(p, rate, years):
    n = years * 12
    r = (rate / 100) / 12
    if r == 0: return p / n if n else 0
    return p * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)


def calculate(inputs):
    loan, current_r, new_r = require(inputs, "loan_amount", "current_rate", "new_rate")
    term = to_int(inputs.get("term_years"), "term_years")
    non_negative(loan, "loan_amount"); non_negative(current_r, "current_rate"); non_negative(new_r, "new_rate")
    positive(term, "term_years")

    cur = _emi(loan, current_r, term)
    new = _emi(loan, new_r, term)
    diff = new - cur
    return {
        "current_emi": round(cur, 2),
        "new_emi": round(new, 2),
        "monthly_difference": round(diff, 2),
        "annual_difference": round(diff * 12, 2),
        "lifetime_difference": round(diff * term * 12, 2),
        "direction": "Rate INCREASE — higher payments." if diff > 0 else "Rate DECREASE — lower payments." if diff < 0 else "No change.",
    }

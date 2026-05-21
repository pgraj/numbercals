"""Amortization Schedule Calculator. Returns first-year schedule + summary."""
from typing import Any, Dict, List
from ._base import non_negative, positive, require, to_int

META = {
    "slug": "amortization",
    "name": "Amortization Calculator",
    "category": "finance",
    "description": "Generate a loan amortization schedule showing principal, interest, and balance per month.",
    "formula": "Monthly Payment = P · r(1+r)^n / [(1+r)^n − 1]",
    "fields": [
        {"name": "principal", "label": "Loan Amount", "type": "number", "min": 0, "required": True, "placeholder": "300000"},
        {"name": "annual_rate", "label": "Annual Interest Rate (%)", "type": "number", "min": 0, "required": True, "placeholder": "6.5"},
        {"name": "term_years", "label": "Loan Term (years)", "type": "number", "min": 1, "required": True, "placeholder": "30"},
    ],
    "outputs": [
        {"key": "monthly_payment", "label": "Monthly Payment", "format": "currency"},
        {"key": "total_interest", "label": "Total Interest", "format": "currency"},
        {"key": "schedule_first_year", "label": "First Year Schedule", "format": "table"},
    ],
    "faq": [{"q": "What is amortization?", "a": "The process of paying off a loan via regular payments where each payment covers interest first, then principal — gradually shifting toward more principal over time."}],
}

def calculate(inputs):
    p, r_annual = require(inputs, "principal", "annual_rate")
    years = to_int(inputs.get("term_years"), "term_years")
    non_negative(p, "principal"); non_negative(r_annual, "annual_rate"); positive(years, "term_years")
    r = (r_annual / 12) / 100
    n = years * 12
    pmt = p / n if r == 0 else p * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)
    balance = p
    schedule: List[Dict[str, Any]] = []
    total_interest = 0.0
    for month in range(1, min(12, n) + 1):
        interest = balance * r
        principal_paid = pmt - interest
        balance -= principal_paid
        total_interest += interest
        schedule.append({
            "month": month,
            "payment": round(pmt, 2),
            "principal": round(principal_paid, 2),
            "interest": round(interest, 2),
            "balance": round(max(balance, 0), 2),
        })
    total_interest_full = pmt * n - p
    return {
        "monthly_payment": round(pmt, 2),
        "total_interest": round(total_interest_full, 2),
        "schedule_first_year": schedule,
    }

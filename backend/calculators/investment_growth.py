"""Investment Growth Calculator (lump sum + regular monthly contributions)."""
from typing import Any, Dict
from ._base import non_negative, require, to_float

META = {
    "slug": "investment-growth",
    "name": "Investment Growth Calculator",
    "category": "finance",
    "description": "Project growth of an initial investment with optional monthly contributions.",
    "formula": "FV = PV(1+r)^n + PMT × [((1+r)^n − 1) / r]",
    "fields": [
        {"name": "initial_amount", "label": "Initial Amount", "type": "number", "min": 0, "required": True, "placeholder": "10000"},
        {"name": "monthly_contribution", "label": "Monthly Contribution", "type": "number", "min": 0, "required": False, "placeholder": "500"},
        {"name": "annual_rate", "label": "Expected Annual Return (%)", "type": "number", "min": 0, "required": True, "placeholder": "8"},
        {"name": "years", "label": "Years", "type": "number", "min": 0, "required": True, "placeholder": "20"},
    ],
    "outputs": [
        {"key": "future_value", "label": "Future Value", "format": "currency"},
        {"key": "total_contributed", "label": "Total Contributed", "format": "currency"},
        {"key": "interest_earned", "label": "Growth from Returns", "format": "currency"},
    ],
    "faq": [
        {"q": "What return should I assume?", "a": "Long-term diversified equity portfolios have historically returned ~7–10% nominal. Use conservative assumptions for planning."},
    ],
}

def calculate(inputs):
    pv, r, years = require(inputs, "initial_amount", "annual_rate", "years")
    pmt = to_float(inputs["monthly_contribution"] if inputs.get("monthly_contribution") not in (None, "") else 0, "monthly_contribution")
    non_negative(pv, "initial_amount"); non_negative(r, "annual_rate"); non_negative(years, "years"); non_negative(pmt, "monthly_contribution")
    monthly_r = (r / 100) / 12
    n = int(years * 12)
    fv_lump = pv * ((1 + monthly_r) ** n) if n else pv
    if monthly_r == 0:
        fv_pmt = pmt * n
    else:
        fv_pmt = pmt * (((1 + monthly_r) ** n - 1) / monthly_r)
    total_fv = fv_lump + fv_pmt
    contributed = pv + pmt * n
    return {
        "future_value": round(total_fv, 2),
        "total_contributed": round(contributed, 2),
        "interest_earned": round(total_fv - contributed, 2),
    }

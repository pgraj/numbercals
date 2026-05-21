"""SIP (Systematic Investment Plan) Calculator.

FV = P × [((1+r)^n − 1) / r] × (1+r)
where r = monthly rate, n = number of months, P = monthly investment.
"""
from typing import Any, Dict
from ._base import non_negative, require

META = {
    "slug": "sip",
    "name": "SIP Calculator",
    "category": "finance",
    "description": "Calculate future value of a Systematic Investment Plan with monthly contributions.",
    "formula": "FV = P × [((1+r)^n − 1) / r] × (1+r)",
    "fields": [
        {"name": "monthly_investment", "label": "Monthly Investment", "type": "number", "min": 0, "required": True, "placeholder": "5000"},
        {"name": "annual_rate", "label": "Expected Annual Return (%)", "type": "number", "min": 0, "required": True, "placeholder": "12"},
        {"name": "years", "label": "Years", "type": "number", "min": 0, "required": True, "placeholder": "15"},
    ],
    "outputs": [
        {"key": "future_value", "label": "Estimated Future Value", "format": "currency"},
        {"key": "total_invested", "label": "Total Invested", "format": "currency"},
        {"key": "wealth_gained", "label": "Wealth Gained", "format": "currency"},
    ],
    "faq": [{"q": "Why is SIP recommended?", "a": "It enforces discipline, averages out market volatility via rupee/dollar cost averaging, and compounds over time."}],
}

def calculate(inputs):
    p, r_annual, years = require(inputs, "monthly_investment", "annual_rate", "years")
    non_negative(p, "monthly_investment"); non_negative(r_annual, "annual_rate"); non_negative(years, "years")
    r = (r_annual / 100) / 12
    n = int(years * 12)
    if r == 0:
        fv = p * n
    else:
        fv = p * (((1 + r) ** n - 1) / r) * (1 + r)
    total_invested = p * n
    return {
        "future_value": round(fv, 2),
        "total_invested": round(total_invested, 2),
        "wealth_gained": round(fv - total_invested, 2),
    }

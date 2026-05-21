"""Salary Increase Impact Calculator.

Compares nominal salary growth vs real (inflation-adjusted) growth.
Real raise % = ((1 + nominal) / (1 + inflation)) - 1

Useful for "did I get a real raise?" — a 3% raise at 3% inflation is a flat real raise.
"""
from typing import Any, Dict
from ._base import non_negative, positive, require, to_int

META = {
    "slug": "salary-increase-impact",
    "name": "Salary Increase Impact Calculator",
    "category": "finance",
    "description": "Compare nominal vs real salary growth after inflation. See whether your raise is actually a raise.",
    "formula": "Real Raise % = ((1 + nominal) / (1 + inflation)) − 1",
    "fields": [
        {"name": "current_salary", "label": "Current Salary", "type": "number", "min": 0, "required": True, "placeholder": "100000"},
        {"name": "annual_raise_percent", "label": "Annual Raise (% nominal)", "type": "number", "required": True, "placeholder": "5"},
        {"name": "inflation_rate", "label": "Annual Inflation (%)", "type": "number", "required": True, "placeholder": "3"},
        {"name": "years", "label": "Years", "type": "number", "min": 1, "required": True, "placeholder": "10"},
    ],
    "outputs": [
        {"key": "future_nominal_salary", "label": "Future Nominal Salary", "format": "currency"},
        {"key": "future_real_salary", "label": "Future Real Salary (today's $)", "format": "currency"},
        {"key": "real_raise_per_year_percent", "label": "Real Raise per Year (%)", "format": "percent"},
        {"key": "real_growth_percent", "label": "Total Real Growth Over Period (%)", "format": "percent"},
        {"key": "assessment", "label": "Assessment", "format": "text"},
    ],
    "faq": [
        {"q": "What if my raise equals inflation?", "a": "You broke even — purchasing power unchanged. Your standard of living didn't improve, even though the headline number went up."},
    ],
}


def calculate(inputs):
    salary, raise_pct, inflation = require(inputs, "current_salary", "annual_raise_percent", "inflation_rate")
    years = to_int(inputs.get("years"), "years")
    positive(salary, "current_salary"); positive(years, "years")

    nominal_factor = (1 + raise_pct / 100) ** years
    inflation_factor = (1 + inflation / 100) ** years

    future_nominal = salary * nominal_factor
    future_real = future_nominal / inflation_factor

    real_raise_per_year = ((1 + raise_pct / 100) / (1 + inflation / 100) - 1) * 100
    real_growth_total = (future_real / salary - 1) * 100

    if real_raise_per_year > 1.5:
        assess = "Strong — your purchasing power is meaningfully growing."
    elif real_raise_per_year > 0:
        assess = "Modest real gain — slightly ahead of inflation."
    elif real_raise_per_year > -0.5:
        assess = "Treading water — roughly keeping pace with inflation."
    else:
        assess = "Falling behind — your real income is shrinking."

    return {
        "future_nominal_salary": round(future_nominal, 2),
        "future_real_salary": round(future_real, 2),
        "real_raise_per_year_percent": round(real_raise_per_year, 3),
        "real_growth_percent": round(real_growth_total, 2),
        "assessment": assess,
    }

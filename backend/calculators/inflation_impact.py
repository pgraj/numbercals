"""Inflation Impact Calculator.

Shows the future purchasing power of a present-day amount given an
inflation rate, and vice versa.

Real Value = Nominal / (1 + inflation)^n
"""
from typing import Any, Dict
from ._base import non_negative, require

META = {
    "slug": "inflation-impact",
    "name": "Inflation Impact Calculator",
    "category": "finance",
    "description": "Calculate the real (inflation-adjusted) value of money in the future, and the loss of purchasing power.",
    "formula": "Real Value = Nominal / (1 + inflation)^n",
    "fields": [
        {"name": "amount_today", "label": "Amount Today", "type": "number", "min": 0, "required": True, "placeholder": "100000"},
        {"name": "inflation_rate", "label": "Annual Inflation Rate (%)", "type": "number", "required": True, "placeholder": "3"},
        {"name": "years", "label": "Years Ahead", "type": "number", "min": 1, "required": True, "placeholder": "10"},
    ],
    "outputs": [
        {"key": "future_purchasing_power", "label": "Future Purchasing Power", "format": "currency"},
        {"key": "loss_of_purchasing_power", "label": "Loss of Purchasing Power", "format": "currency"},
        {"key": "loss_percent", "label": "Loss (%)", "format": "percent"},
        {"key": "nominal_equivalent_needed", "label": "Nominal $ needed to keep same purchasing power", "format": "currency"},
    ],
    "faq": [
        {"q": "Why does $1,000,000 not feel like a lot anymore?", "a": "Inflation. At 3% annual inflation, the purchasing power of money halves about every 23 years."},
        {"q": "Why does this matter for retirement planning?", "a": "If you plan to retire on $80k/year today's money, you need to plan for ~$144k/year in 20 years at 3% inflation just to maintain the same lifestyle."},
    ],
}


def calculate(inputs):
    amount, inflation, years = require(inputs, "amount_today", "inflation_rate", "years")
    non_negative(amount, "amount_today")
    if years <= 0: raise ValueError("'years' must be greater than 0.")
    factor = (1 + inflation / 100) ** years
    future_power = amount / factor
    loss = amount - future_power
    return {
        "future_purchasing_power": round(future_power, 2),
        "loss_of_purchasing_power": round(loss, 2),
        "loss_percent": round((loss / amount * 100) if amount else 0, 2),
        "nominal_equivalent_needed": round(amount * factor, 2),
    }

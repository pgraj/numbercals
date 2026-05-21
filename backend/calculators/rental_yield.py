"""Rental Yield Calculator.

Gross Yield (%) = (Annual Rent / Property Price) × 100
Net Yield (%)   = ((Annual Rent − Annual Expenses) / Property Price) × 100

Annual Rent is computed from weekly rent × 52 (common for AU/UK markets).
"""
from typing import Any, Dict

from ._base import non_negative, positive, require, to_float

META = {
    "slug": "rental-yield",
    "name": "Rental Yield Calculator",
    "category": "property",
    "description": "Calculate gross and net rental yield on an investment property.",
    "formula": "Gross Yield = Annual Rent / Property Price × 100",
    "fields": [
        {"name": "property_price", "label": "Property Price", "type": "number", "min": 0, "required": True, "placeholder": "750000"},
        {"name": "weekly_rent", "label": "Weekly Rent", "type": "number", "min": 0, "required": True, "placeholder": "650"},
        {"name": "annual_expenses", "label": "Annual Expenses (rates, insurance, mgmt, maintenance)", "type": "number", "min": 0, "required": False, "placeholder": "8000"},
    ],
    "outputs": [
        {"key": "annual_rent", "label": "Annual Rent", "format": "currency"},
        {"key": "gross_yield_percent", "label": "Gross Yield (%)", "format": "percent"},
        {"key": "net_yield_percent", "label": "Net Yield (%)", "format": "percent"},
        {"key": "monthly_cashflow_before_mortgage", "label": "Monthly Cashflow (before mortgage)", "format": "currency"},
    ],
    "faq": [
        {"q": "Gross vs net yield?", "a": "Gross yield ignores expenses — it's just rent ÷ price. Net yield subtracts holding costs (rates, insurance, management, maintenance) and gives a much more realistic picture of returns."},
        {"q": "What's a 'good' yield?", "a": "Depends on the market. Australian capital-city houses often yield 2–4% gross; regional areas can be 5–7%. Higher yield usually means lower capital growth — a trade-off, not a free lunch."},
    ],
}


def calculate(inputs: Dict[str, Any]) -> Dict[str, Any]:
    price, weekly = require(inputs, "property_price", "weekly_rent")
    expenses = to_float(inputs["annual_expenses"] if inputs.get("annual_expenses") not in (None, "") else 0, "annual_expenses")
    positive(price, "property_price")
    non_negative(weekly, "weekly_rent")
    non_negative(expenses, "annual_expenses")

    annual_rent = weekly * 52
    gross = annual_rent / price * 100
    net = (annual_rent - expenses) / price * 100
    monthly_cf = (annual_rent - expenses) / 12

    return {
        "annual_rent": round(annual_rent, 2),
        "gross_yield_percent": round(gross, 2),
        "net_yield_percent": round(net, 2),
        "monthly_cashflow_before_mortgage": round(monthly_cf, 2),
    }

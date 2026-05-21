"""Profit Margin Calculator.

Gross Margin (%) = ((Revenue − Cost) / Revenue) × 100
"""
from typing import Any, Dict
from ._base import positive, require

META = {
    "slug": "profit-margin",
    "name": "Profit Margin Calculator",
    "category": "business",
    "description": "Calculate gross profit and profit margin from revenue and cost.",
    "formula": "Margin (%) = ((Revenue − Cost) / Revenue) × 100",
    "fields": [
        {"name": "revenue", "label": "Revenue", "type": "number", "min": 0, "required": True, "placeholder": "100000"},
        {"name": "cost", "label": "Cost", "type": "number", "min": 0, "required": True, "placeholder": "60000"},
    ],
    "outputs": [
        {"key": "gross_profit", "label": "Gross Profit", "format": "currency"},
        {"key": "margin_percent", "label": "Profit Margin (%)", "format": "percent"},
    ],
    "faq": [
        {"q": "Profit margin vs markup?", "a": "Margin is profit as a % of revenue; markup is profit as a % of cost. Same dollar amount, different denominators."},
    ],
}

def calculate(inputs: Dict[str, Any]) -> Dict[str, Any]:
    rev, cost = require(inputs, "revenue", "cost")
    positive(rev, "revenue")
    profit = rev - cost
    return {"gross_profit": round(profit, 2), "margin_percent": round((profit / rev) * 100, 2)}

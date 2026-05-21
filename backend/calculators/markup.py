"""Markup Calculator. Markup% = (Selling − Cost) / Cost × 100"""
from typing import Any, Dict
from ._base import non_negative, positive, require

META = {
    "slug": "markup",
    "name": "Markup Calculator",
    "category": "business",
    "description": "Calculate markup percentage and selling price from cost.",
    "formula": "Markup (%) = ((Selling − Cost) / Cost) × 100",
    "fields": [
        {"name": "cost", "label": "Cost", "type": "number", "min": 0, "required": True, "placeholder": "50"},
        {"name": "selling_price", "label": "Selling Price", "type": "number", "min": 0, "required": True, "placeholder": "75"},
    ],
    "outputs": [
        {"key": "markup_percent", "label": "Markup (%)", "format": "percent"},
        {"key": "profit", "label": "Profit per unit", "format": "currency"},
    ],
    "faq": [{"q": "Markup vs margin?", "a": "Markup is profit as a % of cost; margin is profit as a % of selling price. Same profit, different denominators."}],
}

def calculate(inputs):
    cost, selling = require(inputs, "cost", "selling_price")
    positive(cost, "cost"); non_negative(selling, "selling_price")
    profit = selling - cost
    return {"markup_percent": round(profit / cost * 100, 2), "profit": round(profit, 2)}

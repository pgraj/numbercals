"""Revenue Calculator. Revenue = Price × Quantity"""
from typing import Any, Dict
from ._base import non_negative, require

META = {
    "slug": "revenue",
    "name": "Revenue Calculator",
    "category": "business",
    "description": "Calculate revenue from price and quantity sold.",
    "formula": "Revenue = Price × Quantity",
    "fields": [
        {"name": "price", "label": "Price per Unit", "type": "number", "min": 0, "required": True, "placeholder": "29.99"},
        {"name": "quantity", "label": "Units Sold", "type": "number", "min": 0, "required": True, "placeholder": "500"},
    ],
    "outputs": [{"key": "revenue", "label": "Revenue", "format": "currency"}],
    "faq": [{"q": "Revenue vs profit?", "a": "Revenue is total sales (top line). Profit subtracts costs (bottom line). High revenue does not mean profitable."}],
}

def calculate(inputs):
    p, q = require(inputs, "price", "quantity")
    non_negative(p, "price"); non_negative(q, "quantity")
    return {"revenue": round(p * q, 2)}

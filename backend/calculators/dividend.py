"""Dividend Yield Calculator. Yield% = Annual Dividend / Price × 100"""
from typing import Any, Dict
from ._base import positive, require

META = {
    "slug": "dividend",
    "name": "Dividend Yield Calculator",
    "category": "finance",
    "description": "Calculate dividend yield and annual income from a stock holding.",
    "formula": "Yield (%) = Annual Dividend per Share / Price per Share × 100",
    "fields": [
        {"name": "annual_dividend_per_share", "label": "Annual Dividend per Share", "type": "number", "min": 0, "required": True, "placeholder": "2.50"},
        {"name": "share_price", "label": "Share Price", "type": "number", "min": 0, "required": True, "placeholder": "50"},
        {"name": "shares_held", "label": "Shares Held (optional)", "type": "number", "min": 0, "required": False, "placeholder": "100"},
    ],
    "outputs": [
        {"key": "yield_percent", "label": "Dividend Yield (%)", "format": "percent"},
        {"key": "annual_income", "label": "Estimated Annual Income", "format": "currency"},
    ],
    "faq": [{"q": "Is a high yield always good?", "a": "Not always — abnormally high yields can signal a falling share price or unsustainable payout. Always check payout ratio and earnings stability."}],
}

def calculate(inputs):
    div, price = require(inputs, "annual_dividend_per_share", "share_price")
    positive(price, "share_price")
    shares = float(inputs.get("shares_held") or 0)
    y = div / price * 100
    return {"yield_percent": round(y, 2), "annual_income": round(div * shares, 2)}

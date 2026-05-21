"""Revenue Impact Calculator.

Models the impact of changing price AND/OR volume on revenue, with
independent percentage changes for each.

New Revenue = (Price × (1 + ΔP%)) × (Volume × (1 + ΔV%))
"""
from typing import Any, Dict
from ._base import positive, require, to_float

META = {
    "slug": "revenue-impact",
    "name": "Revenue Impact Calculator",
    "category": "business",
    "description": "See the combined impact of price and volume changes on revenue.",
    "formula": "New Revenue = (Price × (1 + ΔP)) × (Volume × (1 + ΔV))",
    "fields": [
        {"name": "current_price", "label": "Current Price per Unit", "type": "number", "min": 0, "required": True, "placeholder": "100"},
        {"name": "current_volume", "label": "Current Volume (units)", "type": "number", "min": 0, "required": True, "placeholder": "1000"},
        {"name": "price_change_percent", "label": "Price Change (%)", "type": "number", "required": False, "placeholder": "5"},
        {"name": "volume_change_percent", "label": "Volume Change (%)", "type": "number", "required": False, "placeholder": "-2"},
    ],
    "outputs": [
        {"key": "current_revenue", "label": "Current Revenue", "format": "currency"},
        {"key": "new_revenue", "label": "Projected New Revenue", "format": "currency"},
        {"key": "revenue_change", "label": "Revenue Change", "format": "currency"},
        {"key": "revenue_change_percent", "label": "Revenue Change (%)", "format": "percent"},
    ],
    "faq": [
        {"q": "Does this model account for elasticity?", "a": "No — this is a deterministic calculator: you specify both the price change AND the volume change. For elasticity-driven volume response, use the Price Change Impact Calculator."},
    ],
}


def calculate(inputs):
    price, volume = require(inputs, "current_price", "current_volume")
    dp = to_float(inputs["price_change_percent"] if inputs.get("price_change_percent") not in (None, "") else 0, "price_change_percent")
    dv = to_float(inputs["volume_change_percent"] if inputs.get("volume_change_percent") not in (None, "") else 0, "volume_change_percent")
    positive(price, "current_price")

    current = price * volume
    new_price = price * (1 + dp / 100)
    new_volume = volume * (1 + dv / 100)
    new_rev = new_price * new_volume
    change = new_rev - current
    pct = (change / current * 100) if current else 0
    return {
        "current_revenue": round(current, 2),
        "new_revenue": round(new_rev, 2),
        "revenue_change": round(change, 2),
        "revenue_change_percent": round(pct, 2),
    }

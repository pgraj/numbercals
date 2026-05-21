"""Price Change Impact Calculator with Elasticity.

Uses constant-elasticity demand: %ΔQ = −elasticity × %ΔP

A negative elasticity of −1 means a 10% price rise drops demand by 10%.
"""
from typing import Any, Dict
from ._base import positive, require, to_float

META = {
    "slug": "price-change-impact",
    "name": "Price Change Impact Calculator (with Elasticity)",
    "category": "business",
    "description": "Project the impact of a price change on volume, revenue, and profit using price elasticity of demand.",
    "formula": "%ΔQ = −elasticity × %ΔP",
    "fields": [
        {"name": "current_price", "label": "Current Price", "type": "number", "min": 0, "required": True, "placeholder": "100"},
        {"name": "current_volume", "label": "Current Volume", "type": "number", "min": 0, "required": True, "placeholder": "1000"},
        {"name": "unit_cost", "label": "Variable Cost per Unit", "type": "number", "min": 0, "required": True, "placeholder": "40"},
        {"name": "price_change_percent", "label": "Price Change (%)", "type": "number", "required": True, "placeholder": "10"},
        {"name": "elasticity", "label": "Price Elasticity (typical: −0.5 to −2.5)", "type": "number", "required": False, "placeholder": "-1.5"},
    ],
    "outputs": [
        {"key": "current_revenue", "label": "Current Revenue", "format": "currency"},
        {"key": "new_volume", "label": "Projected New Volume", "format": "number"},
        {"key": "new_revenue", "label": "Projected New Revenue", "format": "currency"},
        {"key": "current_profit", "label": "Current Gross Profit", "format": "currency"},
        {"key": "new_profit", "label": "Projected Gross Profit", "format": "currency"},
        {"key": "profit_change_percent", "label": "Profit Change (%)", "format": "percent"},
        {"key": "verdict", "label": "Verdict", "format": "text"},
    ],
    "faq": [
        {"q": "How do I find elasticity for my product?", "a": "Run a price test (A/B), look at industry studies, or use rough benchmarks: luxury goods often −2 to −3, necessities −0.3 to −0.8, addictive goods near 0."},
        {"q": "Why does a price rise sometimes lower profit?", "a": "If demand is elastic (|e| > 1), the volume drop offsets the price gain. Calculator shows this directly."},
    ],
}


def calculate(inputs):
    price, volume, cost, dp = require(inputs, "current_price", "current_volume", "unit_cost", "price_change_percent")
    elasticity = to_float(inputs["elasticity"] if inputs.get("elasticity") not in (None, "") else -1.5, "elasticity")
    positive(price, "current_price")

    new_price = price * (1 + dp / 100)
    # Elasticity of demand is negative by convention; we use abs() so users can
    # enter it either way (1.5 or -1.5) and get the right sign on volume.
    dv_pct = -abs(elasticity) * dp
    new_volume = max(volume * (1 + dv_pct / 100), 0)
    current_rev = price * volume
    new_rev = new_price * new_volume
    current_profit = (price - cost) * volume
    new_profit = (new_price - cost) * new_volume
    profit_change_pct = ((new_profit - current_profit) / current_profit * 100) if current_profit else 0

    if profit_change_pct > 1:
        verdict = f"Profit IMPROVES by {round(profit_change_pct, 1)}% — price change is favorable."
    elif profit_change_pct < -1:
        verdict = f"Profit DROPS by {round(-profit_change_pct, 1)}% — reconsider this price change."
    else:
        verdict = "Profit roughly unchanged — break-even price move."

    return {
        "current_revenue": round(current_rev, 2),
        "new_volume": round(new_volume, 2),
        "new_revenue": round(new_rev, 2),
        "current_profit": round(current_profit, 2),
        "new_profit": round(new_profit, 2),
        "profit_change_percent": round(profit_change_pct, 2),
        "verdict": verdict,
    }

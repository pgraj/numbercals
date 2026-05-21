"""LTV Growth Simulator.

Models the impact of reducing churn or improving ARPU on customer LTV.

LTV = ARPU × Gross Margin / Churn Rate
"""
from typing import Any, Dict
from ._base import positive, require

META = {
    "slug": "ltv-growth-simulator",
    "name": "LTV Growth Simulator",
    "category": "business",
    "description": "Simulate the impact of churn reduction and ARPU improvement on customer Lifetime Value.",
    "formula": "LTV = ARPU × Margin / Churn Rate",
    "fields": [
        {"name": "current_arpu", "label": "Current ARPU (monthly)", "type": "number", "min": 0, "required": True, "placeholder": "100"},
        {"name": "current_churn_percent", "label": "Current Monthly Churn (%)", "type": "number", "min": 0, "required": True, "placeholder": "3"},
        {"name": "gross_margin_percent", "label": "Gross Margin (%)", "type": "number", "min": 0, "required": True, "placeholder": "80"},
        {"name": "new_arpu", "label": "Projected ARPU", "type": "number", "min": 0, "required": True, "placeholder": "120"},
        {"name": "new_churn_percent", "label": "Projected Monthly Churn (%)", "type": "number", "min": 0, "required": True, "placeholder": "2"},
    ],
    "outputs": [
        {"key": "current_ltv", "label": "Current LTV", "format": "currency"},
        {"key": "new_ltv", "label": "New LTV", "format": "currency"},
        {"key": "ltv_increase", "label": "LTV Increase", "format": "currency"},
        {"key": "ltv_increase_percent", "label": "LTV Growth (%)", "format": "percent"},
        {"key": "verdict", "label": "Verdict", "format": "text"},
    ],
    "faq": [
        {"q": "Why is churn so impactful?", "a": "LTV is inversely proportional to churn. Cutting churn from 5% to 2.5% doubles LTV — same as doubling ARPU."},
    ],
}


def calculate(inputs):
    arpu, churn, margin, new_arpu, new_churn = require(
        inputs, "current_arpu", "current_churn_percent", "gross_margin_percent", "new_arpu", "new_churn_percent"
    )
    positive(churn, "current_churn_percent"); positive(new_churn, "new_churn_percent"); positive(margin, "gross_margin_percent")

    current_ltv = arpu * (margin / 100) / (churn / 100)
    new_ltv = new_arpu * (margin / 100) / (new_churn / 100)
    diff = new_ltv - current_ltv
    pct = (diff / current_ltv * 100) if current_ltv else 0

    if pct > 50: verdict = "Major LTV improvement — significant business value."
    elif pct > 20: verdict = "Strong improvement — invest in the levers driving this."
    elif pct > 0: verdict = "Modest improvement."
    else: verdict = "No improvement or regression — revisit assumptions."

    return {
        "current_ltv": round(current_ltv, 2),
        "new_ltv": round(new_ltv, 2),
        "ltv_increase": round(diff, 2),
        "ltv_increase_percent": round(pct, 2),
        "verdict": verdict,
    }

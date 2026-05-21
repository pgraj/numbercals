"""Marketing Spend Impact Calculator.

Projects revenue and profit impact of additional marketing spend at a given ROAS.

Incremental Revenue = Additional Spend × ROAS
Net Profit Impact   = Incremental Revenue × Gross Margin − Additional Spend
"""
from typing import Any, Dict
from ._base import non_negative, positive, require, to_float

META = {
    "slug": "marketing-spend-impact",
    "name": "Marketing Spend Impact Calculator",
    "category": "business",
    "description": "Project the revenue and profit impact of additional marketing spend at an expected ROAS.",
    "formula": "Incremental Revenue = Spend × ROAS;  Profit = Revenue × Margin − Spend",
    "fields": [
        {"name": "additional_spend", "label": "Additional Marketing Spend", "type": "number", "min": 0, "required": True, "placeholder": "50000"},
        {"name": "expected_roas", "label": "Expected ROAS (revenue per $ spent)", "type": "number", "min": 0, "required": True, "placeholder": "4"},
        {"name": "gross_margin_percent", "label": "Gross Margin (%)", "type": "number", "min": 0, "required": True, "placeholder": "60"},
    ],
    "outputs": [
        {"key": "incremental_revenue", "label": "Incremental Revenue", "format": "currency"},
        {"key": "incremental_gross_profit", "label": "Incremental Gross Profit", "format": "currency"},
        {"key": "net_profit_impact", "label": "Net Profit Impact (after spend)", "format": "currency"},
        {"key": "marketing_roi_percent", "label": "Marketing ROI (%)", "format": "percent"},
        {"key": "verdict", "label": "Verdict", "format": "text"},
    ],
    "faq": [
        {"q": "What ROAS should I assume?", "a": "Past performance is the best guide. Industry benchmarks: 3× is OK, 4× is solid, 5×+ is strong. For B2B or high-CAC categories, lower can still be profitable if LTV is large."},
        {"q": "Why does the calculator subtract the spend twice?", "a": "It doesn't — gross profit (revenue × margin) already includes the cost of goods; we subtract spend once at the end to convert gross profit to net profit impact."},
    ],
}


def calculate(inputs):
    spend, roas, margin = require(inputs, "additional_spend", "expected_roas", "gross_margin_percent")
    non_negative(spend, "additional_spend"); non_negative(roas, "expected_roas"); positive(margin, "gross_margin_percent")
    if margin > 100: raise ValueError("'gross_margin_percent' cannot exceed 100.")

    inc_rev = spend * roas
    gross_profit = inc_rev * (margin / 100)
    net_impact = gross_profit - spend
    roi = (net_impact / spend * 100) if spend else 0

    if roi > 50: verdict = "Strongly profitable — scale up if pipeline allows."
    elif roi > 0: verdict = "Profitable — but tight; check assumptions."
    elif roi > -25: verdict = "Marginal loss — likely not worth it unless strategic."
    else: verdict = "Unprofitable — don't proceed with these assumptions."

    return {
        "incremental_revenue": round(inc_rev, 2),
        "incremental_gross_profit": round(gross_profit, 2),
        "net_profit_impact": round(net_impact, 2),
        "marketing_roi_percent": round(roi, 2),
        "verdict": verdict,
    }

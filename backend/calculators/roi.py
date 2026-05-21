"""ROI (Return on Investment) Calculator.

Formula: ROI (%) = (Net Gain / Cost of Investment) × 100
Where Net Gain = Final Value − Cost of Investment
"""
from typing import Any, Dict

from ._base import positive, require

META = {
    "slug": "roi",
    "name": "ROI Calculator",
    "category": "finance",
    "description": "Calculate Return on Investment as a percentage of cost.",
    "formula": "ROI = ((Final Value − Cost) / Cost) × 100",
    "fields": [
        {"name": "initial_investment", "label": "Initial Investment (Cost)", "type": "number", "min": 0, "required": True, "placeholder": "10000"},
        {"name": "final_value", "label": "Final Value", "type": "number", "required": True, "placeholder": "13500"},
    ],
    "outputs": [
        {"key": "net_gain", "label": "Net Gain / Loss", "format": "currency"},
        {"key": "roi_percent", "label": "ROI (%)", "format": "percent"},
    ],
    "faq": [
        {"q": "What is a good ROI?", "a": "It depends on the asset class and timeframe. Equities historically average ~7–10% annually after inflation; a 'good' ROI must beat the risk-free rate plus a premium for the risk taken."},
        {"q": "Does ROI account for time?", "a": "No — ROI is a single-period return. For annualised returns over multiple years, use CAGR."},
    ],
}


def calculate(inputs: Dict[str, Any]) -> Dict[str, Any]:
    cost, final = require(inputs, "initial_investment", "final_value")
    positive(cost, "initial_investment")

    net_gain = final - cost
    roi = (net_gain / cost) * 100
    return {
        "net_gain": round(net_gain, 2),
        "roi_percent": round(roi, 2),
    }

"""CAGR (Compound Annual Growth Rate) Calculator.

Formula: CAGR = (End / Start)^(1/years) − 1
"""
from typing import Any, Dict
from ._base import positive, require

META = {
    "slug": "cagr",
    "name": "CAGR Calculator",
    "category": "finance",
    "description": "Calculate the compound annual growth rate of an investment over multiple years.",
    "formula": "CAGR = (End / Start)^(1/years) − 1",
    "fields": [
        {"name": "start_value", "label": "Starting Value", "type": "number", "min": 0, "required": True, "placeholder": "10000"},
        {"name": "end_value", "label": "Ending Value", "type": "number", "min": 0, "required": True, "placeholder": "16500"},
        {"name": "years", "label": "Number of Years", "type": "number", "min": 1, "required": True, "placeholder": "5"},
    ],
    "outputs": [
        {"key": "cagr_percent", "label": "CAGR (%)", "format": "percent"},
        {"key": "total_growth_percent", "label": "Total Growth (%)", "format": "percent"},
    ],
    "faq": [
        {"q": "How is CAGR different from average annual return?", "a": "CAGR is a smoothed geometric rate that accounts for compounding; the arithmetic average ignores compounding and over-states volatility-driven returns."},
    ],
}

def calculate(inputs: Dict[str, Any]) -> Dict[str, Any]:
    start, end, years = require(inputs, "start_value", "end_value", "years")
    positive(start, "start_value")
    positive(years, "years")
    cagr = ((end / start) ** (1 / years) - 1) * 100
    total = ((end - start) / start) * 100
    return {"cagr_percent": round(cagr, 4), "total_growth_percent": round(total, 2)}

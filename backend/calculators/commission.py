"""Commission Calculator. Commission = Sales × Rate / 100"""
from typing import Any, Dict
from ._base import non_negative, require

META = {
    "slug": "commission",
    "name": "Commission Calculator",
    "category": "business",
    "description": "Calculate commission earned on sales at a given rate.",
    "formula": "Commission = Sales × Rate / 100",
    "fields": [
        {"name": "sales", "label": "Total Sales", "type": "number", "min": 0, "required": True, "placeholder": "100000"},
        {"name": "rate", "label": "Commission Rate (%)", "type": "number", "min": 0, "required": True, "placeholder": "5"},
    ],
    "outputs": [
        {"key": "commission", "label": "Commission", "format": "currency"},
        {"key": "net_to_company", "label": "Net to Company (after commission)", "format": "currency"},
    ],
    "faq": [{"q": "Tiered commissions?", "a": "This calculator handles flat rates. For tiered structures, run it once per tier and sum the results."}],
}

def calculate(inputs):
    sales, rate = require(inputs, "sales", "rate")
    non_negative(sales, "sales"); non_negative(rate, "rate")
    com = sales * rate / 100
    return {"commission": round(com, 2), "net_to_company": round(sales - com, 2)}

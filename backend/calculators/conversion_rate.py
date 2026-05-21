"""Conversion Rate Calculator. CR% = conversions / visitors × 100"""
from typing import Any, Dict
from ._base import non_negative, positive, require

META = {
    "slug": "conversion-rate",
    "name": "Conversion Rate Calculator",
    "category": "business",
    "description": "Calculate conversion rate from visitors and conversions.",
    "formula": "Conversion Rate (%) = (Conversions / Visitors) × 100",
    "fields": [
        {"name": "visitors", "label": "Total Visitors", "type": "number", "min": 0, "required": True, "placeholder": "10000"},
        {"name": "conversions", "label": "Conversions", "type": "number", "min": 0, "required": True, "placeholder": "250"},
    ],
    "outputs": [{"key": "conversion_rate_percent", "label": "Conversion Rate (%)", "format": "percent"}],
    "faq": [{"q": "What's a good conversion rate?", "a": "Varies wildly by industry and intent. E-commerce site average ~2–3%; lead-gen landing pages can hit 10–25%."}],
}

def calculate(inputs):
    visitors, conv = require(inputs, "visitors", "conversions")
    positive(visitors, "visitors"); non_negative(conv, "conversions")
    if conv > visitors: raise ValueError("Conversions cannot exceed visitors.")
    return {"conversion_rate_percent": round(conv / visitors * 100, 4)}

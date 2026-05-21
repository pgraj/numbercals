"""Discount Calculator.

Final Price = Original × (1 − Discount% / 100)
"""
from typing import Any, Dict
from ._base import non_negative, require

META = {
    "slug": "discount",
    "name": "Discount Calculator",
    "category": "finance",
    "description": "Calculate sale price and savings after applying a percentage discount.",
    "formula": "Final = Original × (1 − Discount%/100)",
    "fields": [
        {"name": "original_price", "label": "Original Price", "type": "number", "min": 0, "required": True, "placeholder": "200"},
        {"name": "discount_percent", "label": "Discount (%)", "type": "number", "min": 0, "required": True, "placeholder": "25"},
    ],
    "outputs": [
        {"key": "final_price", "label": "Final Price", "format": "currency"},
        {"key": "amount_saved", "label": "You Save", "format": "currency"},
    ],
    "faq": [
        {"q": "How do I calculate a discount in my head?", "a": "Find 10% by moving the decimal one place left, then scale. e.g. 25% off $80 → 10% is $8, so 20% is $16, plus half of $8 = $4 → total off $20."},
    ],
}

def calculate(inputs: Dict[str, Any]) -> Dict[str, Any]:
    price, disc = require(inputs, "original_price", "discount_percent")
    non_negative(price, "original_price"); non_negative(disc, "discount_percent")
    if disc > 100:
        raise ValueError("'discount_percent' cannot exceed 100.")
    saved = price * disc / 100
    return {"final_price": round(price - saved, 2), "amount_saved": round(saved, 2)}

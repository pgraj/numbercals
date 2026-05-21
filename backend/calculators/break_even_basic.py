"""Break-even Calculator (basic).

Break-even units = Fixed Costs / (Price per unit − Variable Cost per unit)
"""
from typing import Any, Dict
from ._base import non_negative, positive, require

META = {
    "slug": "break-even",
    "name": "Break-even Calculator",
    "category": "business",
    "description": "Calculate the number of units required to cover all fixed and variable costs.",
    "formula": "Break-even Units = Fixed Costs / (Price − Variable Cost)",
    "fields": [
        {"name": "fixed_costs", "label": "Total Fixed Costs", "type": "number", "min": 0, "required": True, "placeholder": "50000"},
        {"name": "price_per_unit", "label": "Price per Unit", "type": "number", "min": 0, "required": True, "placeholder": "100"},
        {"name": "variable_cost_per_unit", "label": "Variable Cost per Unit", "type": "number", "min": 0, "required": True, "placeholder": "40"},
    ],
    "outputs": [
        {"key": "break_even_units", "label": "Break-even Units", "format": "number"},
        {"key": "break_even_revenue", "label": "Break-even Revenue", "format": "currency"},
        {"key": "contribution_margin", "label": "Contribution Margin per Unit", "format": "currency"},
    ],
    "faq": [
        {"q": "What is contribution margin?", "a": "The amount each unit sold contributes toward covering fixed costs, calculated as Price minus Variable Cost."},
    ],
}

def calculate(inputs: Dict[str, Any]) -> Dict[str, Any]:
    fc, price, vc = require(inputs, "fixed_costs", "price_per_unit", "variable_cost_per_unit")
    non_negative(fc, "fixed_costs"); non_negative(price, "price_per_unit"); non_negative(vc, "variable_cost_per_unit")
    contribution = price - vc
    if contribution <= 0:
        raise ValueError("Price per unit must be greater than variable cost per unit.")
    units = fc / contribution
    return {
        "break_even_units": round(units, 2),
        "break_even_revenue": round(units * price, 2),
        "contribution_margin": round(contribution, 2),
    }

"""Electrical Power Calculator. P = V × I"""
from typing import Any, Dict
from ._base import require

META = {
    "slug": "power-electrical",
    "name": "Electrical Power Calculator",
    "category": "physics",
    "description": "Calculate electrical power from voltage and current.",
    "formula": "P = V × I",
    "fields": [
        {"name": "voltage", "label": "Voltage (V)", "type": "number", "required": True, "placeholder": "230"},
        {"name": "current", "label": "Current (A)", "type": "number", "required": True, "placeholder": "5"},
    ],
    "outputs": [
        {"key": "power_watts", "label": "Power (W)", "format": "number"},
        {"key": "power_kw", "label": "Power (kW)", "format": "number"},
    ],
    "faq": [{"q": "What about AC power factor?", "a": "For AC circuits, real power = V·I·cos(φ). This calculator gives apparent power; for real power, multiply by your power factor."}],
}

def calculate(inputs):
    v, i = require(inputs, "voltage", "current")
    p = v * i
    return {"power_watts": round(p, 4), "power_kw": round(p / 1000, 4)}

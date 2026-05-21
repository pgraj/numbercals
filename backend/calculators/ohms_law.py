"""Ohm's Law Calculator. V = I × R — solve for any one."""
from typing import Any, Dict
from ._base import to_float

META = {
    "slug": "ohms-law",
    "name": "Ohm's Law Calculator",
    "category": "physics",
    "description": "Solve for voltage, current, or resistance given any two of the three.",
    "formula": "V = I × R",
    "fields": [
        {"name": "voltage", "label": "Voltage (V) — leave blank to solve for", "type": "number", "required": False, "placeholder": ""},
        {"name": "current", "label": "Current (A)", "type": "number", "required": False, "placeholder": ""},
        {"name": "resistance", "label": "Resistance (Ω)", "type": "number", "required": False, "placeholder": ""},
    ],
    "outputs": [
        {"key": "voltage", "label": "Voltage (V)", "format": "number"},
        {"key": "current", "label": "Current (A)", "format": "number"},
        {"key": "resistance", "label": "Resistance (Ω)", "format": "number"},
    ],
    "faq": [{"q": "How do I use this?", "a": "Enter any two values, leave the third blank. The calculator solves for the missing one."}],
}

def _has(v): return v not in (None, "", "null")

def calculate(inputs):
    v_in = inputs.get("voltage"); i_in = inputs.get("current"); r_in = inputs.get("resistance")
    v = to_float(v_in, "voltage") if _has(v_in) else None
    i = to_float(i_in, "current") if _has(i_in) else None
    r = to_float(r_in, "resistance") if _has(r_in) else None
    given = sum(x is not None for x in (v, i, r))
    if given < 2:
        raise ValueError("Provide at least two of: voltage, current, resistance.")
    if v is None:
        v = i * r
    elif i is None:
        if r == 0: raise ValueError("Resistance must be non-zero to solve for current.")
        i = v / r
    elif r is None:
        if i == 0: raise ValueError("Current must be non-zero to solve for resistance.")
        r = v / i
    return {"voltage": round(v, 4), "current": round(i, 4), "resistance": round(r, 4)}

"""Ideal Weight Calculator. Uses Devine, Robinson, Miller, Hamwi formulas (height in inches)."""
from typing import Any, Dict
from ._base import positive, require

META = {
    "slug": "ideal-weight",
    "name": "Ideal Weight Calculator",
    "category": "health",
    "description": "Calculate ideal body weight using four established formulas (Devine, Robinson, Miller, Hamwi).",
    "formula": "Multiple — see output for each formula's result.",
    "fields": [
        {"name": "height_cm", "label": "Height (cm)", "type": "number", "min": 1, "required": True, "placeholder": "175"},
        {"name": "sex", "label": "Sex", "type": "select", "options": [{"value": "male", "label": "Male"}, {"value": "female", "label": "Female"}], "required": True, "default": "male"},
    ],
    "outputs": [
        {"key": "devine_kg", "label": "Devine Formula (kg)", "format": "number"},
        {"key": "robinson_kg", "label": "Robinson Formula (kg)", "format": "number"},
        {"key": "miller_kg", "label": "Miller Formula (kg)", "format": "number"},
        {"key": "hamwi_kg", "label": "Hamwi Formula (kg)", "format": "number"},
    ],
    "faq": [{"q": "Which formula should I use?", "a": "There's no single 'correct' formula — use the average across the four as a reasonable target range."}],
}

def calculate(inputs):
    (h,) = require(inputs, "height_cm")
    positive(h, "height_cm")
    sex = str(inputs.get("sex", "male")).lower()
    inches_over_5ft = (h / 2.54) - 60
    if sex == "male":
        devine = 50 + 2.3 * inches_over_5ft
        robinson = 52 + 1.9 * inches_over_5ft
        miller = 56.2 + 1.41 * inches_over_5ft
        hamwi = 48 + 2.7 * inches_over_5ft
    else:
        devine = 45.5 + 2.3 * inches_over_5ft
        robinson = 49 + 1.7 * inches_over_5ft
        miller = 53.1 + 1.36 * inches_over_5ft
        hamwi = 45.5 + 2.2 * inches_over_5ft
    return {
        "devine_kg": round(devine, 1),
        "robinson_kg": round(robinson, 1),
        "miller_kg": round(miller, 1),
        "hamwi_kg": round(hamwi, 1),
    }

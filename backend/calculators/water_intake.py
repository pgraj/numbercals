"""Water Intake Calculator. Rule of thumb: 35 ml per kg body weight + activity bonus."""
from typing import Any, Dict
from ._base import positive, require, to_float

META = {
    "slug": "water-intake",
    "name": "Water Intake Calculator",
    "category": "health",
    "description": "Estimate daily water intake based on body weight and exercise duration.",
    "formula": "ml/day = weight × 35 + (exercise_minutes × 12)",
    "fields": [
        {"name": "weight_kg", "label": "Weight (kg)", "type": "number", "min": 1, "required": True, "placeholder": "70"},
        {"name": "exercise_minutes", "label": "Exercise (minutes/day)", "type": "number", "min": 0, "required": False, "placeholder": "30"},
    ],
    "outputs": [
        {"key": "ml_per_day", "label": "Daily Water (ml)", "format": "number"},
        {"key": "litres_per_day", "label": "Daily Water (L)", "format": "number"},
        {"key": "glasses_250ml", "label": "Glasses (250 ml)", "format": "number"},
    ],
    "faq": [{"q": "Is 8 glasses a day universal?", "a": "No — needs vary by body size, climate, and activity. Use thirst and pale-yellow urine as practical signals."}],
}

def calculate(inputs):
    (w,) = require(inputs, "weight_kg")
    positive(w, "weight_kg")
    ex = to_float(inputs["exercise_minutes"] if inputs.get("exercise_minutes") not in (None, "") else 0, "exercise_minutes")
    ml = w * 35 + ex * 12
    return {
        "ml_per_day": round(ml, 0),
        "litres_per_day": round(ml / 1000, 2),
        "glasses_250ml": round(ml / 250, 1),
    }

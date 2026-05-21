"""TDEE Calculator. TDEE = BMR × activity multiplier."""
from typing import Any, Dict
from ._base import require
from . import bmr as bmr_mod

ACTIVITY_LEVELS = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9,
}

META = {
    "slug": "tdee",
    "name": "TDEE Calculator",
    "category": "health",
    "description": "Calculate Total Daily Energy Expenditure based on BMR and activity level.",
    "formula": "TDEE = BMR × Activity Factor",
    "fields": [
        {"name": "weight_kg", "label": "Weight (kg)", "type": "number", "min": 1, "required": True, "placeholder": "70"},
        {"name": "height_cm", "label": "Height (cm)", "type": "number", "min": 1, "required": True, "placeholder": "175"},
        {"name": "age", "label": "Age", "type": "number", "min": 1, "required": True, "placeholder": "30"},
        {"name": "sex", "label": "Sex", "type": "select", "options": [{"value": "male", "label": "Male"}, {"value": "female", "label": "Female"}], "required": True, "default": "male"},
        {"name": "activity", "label": "Activity Level", "type": "select", "required": True, "default": "moderate",
         "options": [
             {"value": "sedentary", "label": "Sedentary (little exercise)"},
             {"value": "light", "label": "Light (1–3 days/week)"},
             {"value": "moderate", "label": "Moderate (3–5 days/week)"},
             {"value": "active", "label": "Active (6–7 days/week)"},
             {"value": "very_active", "label": "Very Active (athlete/physical job)"},
         ]},
    ],
    "outputs": [
        {"key": "bmr", "label": "BMR", "format": "number"},
        {"key": "tdee", "label": "TDEE (maintenance calories)", "format": "number"},
    ],
    "faq": [{"q": "How accurate is TDEE?", "a": "It's an estimate within ~10%. Track actual intake vs weight change over 2–3 weeks to calibrate."}],
}

def calculate(inputs):
    bmr_result = bmr_mod.calculate(inputs)
    activity = str(inputs.get("activity", "moderate")).lower()
    if activity not in ACTIVITY_LEVELS:
        raise ValueError(f"Invalid activity level: {activity}")
    tdee = bmr_result["bmr"] * ACTIVITY_LEVELS[activity]
    return {"bmr": bmr_result["bmr"], "tdee": round(tdee, 0)}

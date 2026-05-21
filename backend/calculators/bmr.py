"""BMR Calculator (Mifflin-St Jeor equation).

Men:   BMR = 10·w + 6.25·h − 5·age + 5
Women: BMR = 10·w + 6.25·h − 5·age − 161
"""
from typing import Any, Dict
from ._base import positive, require

META = {
    "slug": "bmr",
    "name": "BMR Calculator",
    "category": "health",
    "description": "Calculate Basal Metabolic Rate using the Mifflin-St Jeor equation.",
    "formula": "BMR = 10·weight + 6.25·height − 5·age + s (s=+5 male, −161 female)",
    "fields": [
        {"name": "weight_kg", "label": "Weight (kg)", "type": "number", "min": 1, "required": True, "placeholder": "70"},
        {"name": "height_cm", "label": "Height (cm)", "type": "number", "min": 1, "required": True, "placeholder": "175"},
        {"name": "age", "label": "Age (years)", "type": "number", "min": 1, "required": True, "placeholder": "30"},
        {"name": "sex", "label": "Sex", "type": "select", "options": [{"value": "male", "label": "Male"}, {"value": "female", "label": "Female"}], "required": True, "default": "male"},
    ],
    "outputs": [{"key": "bmr", "label": "BMR (kcal/day)", "format": "number"}],
    "faq": [{"q": "What is BMR?", "a": "The number of calories your body needs at complete rest to maintain basic functions (breathing, circulation, cell production)."}],
}

def calculate(inputs):
    w, h, age = require(inputs, "weight_kg", "height_cm", "age")
    positive(w, "weight_kg"); positive(h, "height_cm"); positive(age, "age")
    sex = str(inputs.get("sex", "male")).lower()
    base = 10 * w + 6.25 * h - 5 * age
    bmr = base + 5 if sex == "male" else base - 161
    return {"bmr": round(bmr, 0)}

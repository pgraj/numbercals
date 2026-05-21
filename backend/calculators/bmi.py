"""BMI Calculator. BMI = weight(kg) / height(m)^2"""
from typing import Any, Dict
from ._base import positive, require

META = {
    "slug": "bmi",
    "name": "BMI Calculator",
    "category": "health",
    "description": "Calculate Body Mass Index from weight and height. Get your category (underweight/normal/overweight/obese).",
    "formula": "BMI = weight(kg) / height(m)²",
    "fields": [
        {"name": "weight_kg", "label": "Weight (kg)", "type": "number", "min": 1, "required": True, "placeholder": "70"},
        {"name": "height_cm", "label": "Height (cm)", "type": "number", "min": 1, "required": True, "placeholder": "175"},
    ],
    "outputs": [
        {"key": "bmi", "label": "BMI", "format": "number"},
        {"key": "category", "label": "Category", "format": "text"},
    ],
    "faq": [{"q": "Is BMI accurate for everyone?", "a": "No. BMI doesn't distinguish muscle from fat, so athletes and very muscular people can be classed 'overweight' incorrectly. For body composition, use body fat % or waist-to-height ratio."}],
}

def _category(bmi: float) -> str:
    if bmi < 18.5: return "Underweight"
    if bmi < 25: return "Normal weight"
    if bmi < 30: return "Overweight"
    return "Obese"

def calculate(inputs):
    w, h_cm = require(inputs, "weight_kg", "height_cm")
    positive(w, "weight_kg"); positive(h_cm, "height_cm")
    h = h_cm / 100
    bmi = w / (h * h)
    return {"bmi": round(bmi, 2), "category": _category(bmi)}

"""Calorie Calculator — adjusts TDEE for weight goal."""
from typing import Any, Dict
from . import tdee as tdee_mod

GOAL_ADJUSTMENT = {
    "lose_aggressive": -750,
    "lose": -500,
    "lose_mild": -250,
    "maintain": 0,
    "gain_mild": 250,
    "gain": 500,
}

META = {
    "slug": "calorie",
    "name": "Calorie Calculator",
    "category": "health",
    "description": "Calculate daily calorie target for weight loss, maintenance, or gain.",
    "formula": "Target = TDEE + Goal Adjustment",
    "fields": [
        {"name": "weight_kg", "label": "Weight (kg)", "type": "number", "min": 1, "required": True, "placeholder": "70"},
        {"name": "height_cm", "label": "Height (cm)", "type": "number", "min": 1, "required": True, "placeholder": "175"},
        {"name": "age", "label": "Age", "type": "number", "min": 1, "required": True, "placeholder": "30"},
        {"name": "sex", "label": "Sex", "type": "select", "options": [{"value": "male", "label": "Male"}, {"value": "female", "label": "Female"}], "required": True, "default": "male"},
        {"name": "activity", "label": "Activity Level", "type": "select", "required": True, "default": "moderate",
         "options": [
             {"value": "sedentary", "label": "Sedentary"}, {"value": "light", "label": "Light"},
             {"value": "moderate", "label": "Moderate"}, {"value": "active", "label": "Active"},
             {"value": "very_active", "label": "Very Active"}]},
        {"name": "goal", "label": "Goal", "type": "select", "required": True, "default": "maintain",
         "options": [
             {"value": "lose_aggressive", "label": "Lose weight (aggressive, −0.75kg/wk)"},
             {"value": "lose", "label": "Lose weight (−0.5kg/wk)"},
             {"value": "lose_mild", "label": "Lose weight (mild, −0.25kg/wk)"},
             {"value": "maintain", "label": "Maintain weight"},
             {"value": "gain_mild", "label": "Gain weight (mild)"},
             {"value": "gain", "label": "Gain weight"}]},
    ],
    "outputs": [
        {"key": "tdee", "label": "Maintenance Calories (TDEE)", "format": "number"},
        {"key": "target_calories", "label": "Daily Target", "format": "number"},
    ],
    "faq": [{"q": "Is 500 cal/day deficit too aggressive?", "a": "For most adults it's sustainable and produces ~0.5kg/week loss. Aggressive deficits over 1000/day can cause muscle loss and metabolic adaptation."}],
}

def calculate(inputs):
    base = tdee_mod.calculate(inputs)
    goal = str(inputs.get("goal", "maintain")).lower()
    if goal not in GOAL_ADJUSTMENT:
        raise ValueError(f"Invalid goal: {goal}")
    target = base["tdee"] + GOAL_ADJUSTMENT[goal]
    return {"tdee": base["tdee"], "target_calories": round(max(target, 1000), 0)}

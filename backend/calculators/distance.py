"""Distance Calculator. distance = speed × time"""
from typing import Any, Dict
from ._base import non_negative, require

META = {
    "slug": "distance",
    "name": "Distance Calculator",
    "category": "time",
    "description": "Calculate distance from speed and time.",
    "formula": "distance = speed × time",
    "fields": [
        {"name": "speed", "label": "Speed", "type": "number", "min": 0, "required": True, "placeholder": "60"},
        {"name": "time", "label": "Time (hours)", "type": "number", "min": 0, "required": True, "placeholder": "3"},
    ],
    "outputs": [{"key": "distance", "label": "Distance", "format": "number"}],
    "faq": [{"q": "Why time in hours?", "a": "Convention — to match speed in distance/hour. Convert your time before entering if needed."}],
}

def calculate(inputs):
    s, t = require(inputs, "speed", "time")
    non_negative(s, "speed"); non_negative(t, "time")
    return {"distance": round(s * t, 4)}

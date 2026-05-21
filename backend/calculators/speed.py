"""Speed Calculator. speed = distance / time"""
from typing import Any, Dict
from ._base import positive, require

META = {
    "slug": "speed",
    "name": "Speed Calculator",
    "category": "time",
    "description": "Calculate average speed from distance and time.",
    "formula": "speed = distance / time",
    "fields": [
        {"name": "distance", "label": "Distance", "type": "number", "min": 0, "required": True, "placeholder": "150"},
        {"name": "time", "label": "Time (hours)", "type": "number", "min": 0, "required": True, "placeholder": "2.5"},
    ],
    "outputs": [{"key": "speed", "label": "Speed (units / hour)", "format": "number"}],
    "faq": [{"q": "Units?", "a": "If distance is in km, speed is km/h. If miles, then mph. The math doesn't care — just stay consistent."}],
}

def calculate(inputs):
    d, t = require(inputs, "distance", "time")
    positive(t, "time")
    return {"speed": round(d / t, 4)}

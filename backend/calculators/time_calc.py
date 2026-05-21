"""Time Calculator. time = distance / speed"""
from typing import Any, Dict
from ._base import positive, require

META = {
    "slug": "time",
    "name": "Time Calculator",
    "category": "time",
    "description": "Calculate time required from distance and speed.",
    "formula": "time = distance / speed",
    "fields": [
        {"name": "distance", "label": "Distance", "type": "number", "min": 0, "required": True, "placeholder": "200"},
        {"name": "speed", "label": "Speed", "type": "number", "min": 0, "required": True, "placeholder": "80"},
    ],
    "outputs": [
        {"key": "time_hours", "label": "Time (hours)", "format": "number"},
        {"key": "time_hms", "label": "Time (h:m:s)", "format": "text"},
    ],
    "faq": [{"q": "Speed-time-distance triangle?", "a": "S=D/T, D=S·T, T=D/S — three forms of one equation. Cover the variable you want; the others tell you the operation."}],
}

def calculate(inputs):
    d, s = require(inputs, "distance", "speed")
    positive(s, "speed")
    hours = d / s
    h = int(hours)
    m = int((hours - h) * 60)
    sec = int(round(((hours - h) * 60 - m) * 60))
    return {"time_hours": round(hours, 4), "time_hms": f"{h}h {m}m {sec}s"}

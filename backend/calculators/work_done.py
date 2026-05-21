"""Work Done Calculator. W = F · d · cos(θ)"""
import math
from typing import Any, Dict
from ._base import non_negative, require, to_float

META = {
    "slug": "work-done",
    "name": "Work Done Calculator",
    "category": "physics",
    "description": "Calculate work done by a constant force over a displacement.",
    "formula": "W = F · d · cos(θ)",
    "fields": [
        {"name": "force", "label": "Force (N)", "type": "number", "required": True, "placeholder": "50"},
        {"name": "distance", "label": "Distance (m)", "type": "number", "min": 0, "required": True, "placeholder": "10"},
        {"name": "angle_degrees", "label": "Angle (degrees, default 0)", "type": "number", "required": False, "placeholder": "0"},
    ],
    "outputs": [{"key": "work_done_joules", "label": "Work (J)", "format": "number"}],
    "faq": [{"q": "When is work zero?", "a": "When force is perpendicular to motion (θ = 90°, cos = 0) — e.g. a bag hanging from your hand while you walk forward."}],
}

def calculate(inputs):
    f, d = require(inputs, "force", "distance")
    angle = to_float(inputs["angle_degrees"] if inputs.get("angle_degrees") not in (None, "") else 0, "angle_degrees")
    non_negative(d, "distance")
    return {"work_done_joules": round(f * d * math.cos(math.radians(angle)), 4)}

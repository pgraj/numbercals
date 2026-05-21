"""Impulse (J = F × Δt = Δp) — change in momentum from a force applied over time."""
from ._base import non_negative, require

META = {
    "slug": "impulse",
    "name": "Impulse Calculator",
    "category": "physics",
    "description": "Calculate impulse from force × time, and the resulting change in momentum.",
    "formula": "J = F × Δt = Δp",
    "fields": [
        {"name": "force", "label": "Force (N)", "type": "number", "required": True, "placeholder": "500"},
        {"name": "time", "label": "Time interval (s)", "type": "number", "min": 0, "required": True, "placeholder": "0.1"},
    ],
    "outputs": [
        {"key": "impulse", "label": "Impulse (N·s)", "format": "number"},
        {"key": "change_in_momentum", "label": "Change in Momentum (kg·m/s)", "format": "number"},
    ],
    "faq": [
        {"q": "Why are airbags useful?", "a": "They increase the time over which your body decelerates. Same impulse (Δp), spread over more time, means lower peak force. Lower force = less injury."},
    ],
}

def calculate(inputs):
    f, t = require(inputs, "force", "time")
    non_negative(t, "time")
    j = f * t
    return {"impulse": round(j, 4), "change_in_momentum": round(j, 4)}

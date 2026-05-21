"""Simple pendulum period — T = 2π·√(L/g)."""
import math
from ._base import positive, require, to_float

META = {
    "slug": "pendulum-period",
    "name": "Pendulum Period Calculator",
    "category": "physics",
    "description": "Calculate the period of a simple pendulum (small-angle approximation).",
    "formula": "T = 2π·√(L/g)",
    "fields": [
        {"name": "length", "label": "Length (m)", "type": "number", "min": 0, "required": True, "placeholder": "1"},
        {"name": "gravity", "label": "Gravity (m/s², default 9.81)", "type": "number", "min": 0, "required": False, "placeholder": "9.81"},
    ],
    "outputs": [
        {"key": "period_seconds", "label": "Period T (s)", "format": "number"},
        {"key": "frequency_hz", "label": "Frequency (Hz)", "format": "number"},
    ],
    "faq": [
        {"q": "Why doesn't mass appear?", "a": "Because for a simple pendulum (small angle, point mass on a massless rod), period depends only on length and gravity — not on mass."},
        {"q": "Why 'small-angle'?", "a": "For angles below ~15°, the period is essentially constant. At larger angles, the period grows slightly with amplitude."},
    ],
}

def calculate(inputs):
    (L,) = require(inputs, "length")
    g = to_float(inputs["gravity"] if inputs.get("gravity") not in (None, "") else 9.81, "gravity")
    positive(L, "length"); positive(g, "gravity")
    T = 2 * math.pi * math.sqrt(L / g)
    return {"period_seconds": round(T, 6), "frequency_hz": round(1/T, 6)}

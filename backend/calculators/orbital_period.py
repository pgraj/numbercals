"""Orbital period from Kepler's 3rd law — T = 2π·√(a³/GM)."""
import math
from ._base import positive, require, to_float

G = 6.67430e-11

BODIES = {
    "earth":   5.972e24,
    "sun":     1.989e30,
    "moon":    7.342e22,
    "mars":    6.4171e23,
    "jupiter": 1.898e27,
}

META = {
    "slug": "orbital-period",
    "name": "Orbital Period Calculator (Kepler's 3rd Law)",
    "category": "physics",
    "description": "Calculate the orbital period of a satellite or planet using Kepler's 3rd law.",
    "formula": "T = 2π·√(a³/GM)",
    "fields": [
        {"name": "central_body", "label": "Central Body", "type": "select", "required": True, "default": "earth",
         "options": [{"value": k, "label": k.title()} for k in BODIES] + [{"value": "custom", "label": "Custom"}]},
        {"name": "central_mass", "label": "Central mass (kg, only if 'Custom')", "type": "number", "min": 0, "required": False, "placeholder": "5.972e24"},
        {"name": "semi_major_axis", "label": "Semi-major axis (m)", "type": "number", "min": 0, "required": True, "placeholder": "6.778e6"},
    ],
    "outputs": [
        {"key": "period_seconds", "label": "Orbital Period (s)", "format": "number"},
        {"key": "period_minutes", "label": "Orbital Period (min)", "format": "number"},
        {"key": "period_hours", "label": "Orbital Period (hours)", "format": "number"},
        {"key": "period_days", "label": "Orbital Period (days)", "format": "number"},
        {"key": "period_years", "label": "Orbital Period (years)", "format": "number"},
    ],
    "faq": [
        {"q": "What's Kepler's 3rd law?", "a": "The square of a planet's orbital period is proportional to the cube of its semi-major axis: T² ∝ a³. Newton's gravitation gives the exact form: T² = (4π²/GM) · a³."},
        {"q": "Example: ISS orbit?", "a": "Semi-major axis ≈ 6.778 × 10⁶ m (Earth radius + 400 km altitude). Period ≈ 92.7 minutes — matches reality."},
    ],
}

def calculate(inputs):
    body = str(inputs.get("central_body", "earth")).lower()
    if body == "custom":
        M = to_float(inputs.get("central_mass"), "central_mass")
    elif body in BODIES:
        M = BODIES[body]
    else:
        raise ValueError(f"Unknown body: {body}")
    (a,) = require(inputs, "semi_major_axis")
    positive(M, "central_mass"); positive(a, "semi_major_axis")
    T = 2 * math.pi * math.sqrt(a**3 / (G * M))
    return {
        "period_seconds": round(T, 4),
        "period_minutes": round(T / 60, 4),
        "period_hours": round(T / 3600, 4),
        "period_days": round(T / 86400, 6),
        "period_years": round(T / (86400 * 365.25), 6),
    }

"""Escape velocity — minimum speed to escape a body's gravity. v = √(2GM/r)."""
import math
from ._base import positive, require, to_float

G = 6.67430e-11

# Body presets (mass_kg, radius_m)
BODIES = {
    "earth":   (5.972e24, 6.371e6),
    "moon":    (7.342e22, 1.7374e6),
    "mars":    (6.4171e23, 3.3895e6),
    "jupiter": (1.898e27, 6.9911e7),
    "sun":     (1.989e30, 6.9634e8),
    "mercury": (3.3011e23, 2.4397e6),
    "venus":   (4.8675e24, 6.0518e6),
    "saturn":  (5.683e26, 5.8232e7),
}

META = {
    "slug": "escape-velocity",
    "name": "Escape Velocity Calculator",
    "category": "physics",
    "description": "Calculate the minimum speed needed to escape a celestial body's gravitational pull.",
    "formula": "v_escape = √(2GM/r)",
    "fields": [
        {"name": "body", "label": "Celestial Body", "type": "select", "required": True, "default": "earth",
         "options": [{"value": k, "label": k.title()} for k in BODIES] + [{"value": "custom", "label": "Custom"}]},
        {"name": "mass", "label": "Mass (kg, only if 'Custom')", "type": "number", "min": 0, "required": False, "placeholder": "5.972e24"},
        {"name": "radius", "label": "Radius (m, only if 'Custom')", "type": "number", "min": 0, "required": False, "placeholder": "6371000"},
    ],
    "outputs": [
        {"key": "escape_velocity_mps", "label": "Escape Velocity (m/s)", "format": "number"},
        {"key": "escape_velocity_kmps", "label": "Escape Velocity (km/s)", "format": "number"},
        {"key": "escape_velocity_kmh", "label": "Escape Velocity (km/h)", "format": "number"},
    ],
    "faq": [
        {"q": "What's Earth's escape velocity?", "a": "About 11.2 km/s (40,270 km/h). That's the speed needed to leave Earth's gravity entirely with no further propulsion — though real spacecraft don't actually need this speed, because they keep thrusting."},
        {"q": "Black hole?", "a": "A black hole's escape velocity exceeds the speed of light — which is why light cannot escape from inside the event horizon."},
    ],
}

def calculate(inputs):
    body = str(inputs.get("body", "earth")).lower()
    if body == "custom":
        m = to_float(inputs.get("mass"), "mass")
        r = to_float(inputs.get("radius"), "radius")
    elif body in BODIES:
        m, r = BODIES[body]
    else:
        raise ValueError(f"Unknown body: {body}")
    positive(m, "mass"); positive(r, "radius")
    v = math.sqrt(2 * G * m / r)
    return {
        "escape_velocity_mps": round(v, 2),
        "escape_velocity_kmps": round(v / 1000, 4),
        "escape_velocity_kmh": round(v * 3.6, 1),
    }

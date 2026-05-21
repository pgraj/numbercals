"""Weight calculator — W = m × g (Newton's 2nd law in the gravitational case)."""
from ._base import non_negative, require, to_float

GRAVITY = {
    "earth": 9.80665, "moon": 1.625, "mars": 3.711, "jupiter": 24.79,
    "venus": 8.87, "mercury": 3.7, "saturn": 10.44, "uranus": 8.69,
    "neptune": 11.15, "pluto": 0.62, "sun": 274.0,
}

META = {
    "slug": "weight",
    "name": "Weight Calculator",
    "category": "physics",
    "description": "Calculate weight (gravitational force) from mass and gravitational acceleration. Includes presets for planets.",
    "formula": "W = m × g",
    "fields": [
        {"name": "mass", "label": "Mass (kg)", "type": "number", "min": 0, "required": True, "placeholder": "70"},
        {"name": "location", "label": "Location", "type": "select", "required": True, "default": "earth",
         "options": [{"value": k, "label": k.title() + f" (g = {v})"} for k, v in GRAVITY.items()] + [{"value": "custom", "label": "Custom g"}]},
        {"name": "custom_gravity", "label": "Custom g (m/s², if 'Custom' selected)", "type": "number", "min": 0, "required": False, "placeholder": "9.81"},
    ],
    "outputs": [
        {"key": "weight_newtons", "label": "Weight (N)", "format": "number"},
        {"key": "weight_kgf", "label": "Weight (kgf — kilograms-force)", "format": "number"},
        {"key": "gravity_used", "label": "Gravity used (m/s²)", "format": "number"},
    ],
    "faq": [
        {"q": "What's the difference between mass and weight?", "a": "Mass is how much matter you have (constant). Weight is the gravitational force on that mass (depends on g). You weigh ~6× less on the Moon, but your mass is identical."},
        {"q": "What's kgf?", "a": "Kilogram-force, an older unit equal to weight × g₀. 1 kgf ≈ 9.81 N. It's what bathroom scales display, even though they really measure force."},
    ],
}


def calculate(inputs):
    (m,) = require(inputs, "mass")
    non_negative(m, "mass")
    location = str(inputs.get("location", "earth")).lower()
    if location == "custom":
        g = to_float(inputs.get("custom_gravity"), "custom_gravity")
        non_negative(g, "custom_gravity")
    elif location in GRAVITY:
        g = GRAVITY[location]
    else:
        raise ValueError(f"Unknown location: {location}")
    w = m * g
    return {
        "weight_newtons": round(w, 4),
        "weight_kgf": round(w / 9.80665, 4),
        "gravity_used": g,
    }

"""Newton's Universal Law of Gravitation — F = G·m₁·m₂/r²."""
from ._base import positive, require

G = 6.67430e-11  # N·m²/kg²

META = {
    "slug": "universal-gravitation",
    "name": "Universal Gravitation Calculator",
    "category": "physics",
    "description": "Calculate the gravitational force between two masses using Newton's Law of Universal Gravitation.",
    "formula": "F = G · m₁·m₂ / r²,  where G = 6.674 × 10⁻¹¹ N·m²/kg²",
    "fields": [
        {"name": "mass_1", "label": "Mass 1 (kg)", "type": "number", "min": 0, "required": True, "placeholder": "5.972e24"},
        {"name": "mass_2", "label": "Mass 2 (kg)", "type": "number", "min": 0, "required": True, "placeholder": "7.342e22"},
        {"name": "distance", "label": "Distance between centres (m)", "type": "number", "min": 0, "required": True, "placeholder": "384400000"},
    ],
    "outputs": [{"key": "gravitational_force", "label": "Gravitational Force (N)", "format": "number"}],
    "faq": [
        {"q": "What's G?", "a": "The gravitational constant, ≈ 6.674 × 10⁻¹¹ N·m²/kg². One of the hardest fundamental constants to measure precisely."},
        {"q": "Why is gravity so weak?", "a": "On the scale of individual objects, gravity is roughly 10³⁶ times weaker than electromagnetism. It dominates at large scales only because it's always attractive and never cancels out, unlike electric charge."},
    ],
}

def calculate(inputs):
    m1, m2, r = require(inputs, "mass_1", "mass_2", "distance")
    positive(m1, "mass_1"); positive(m2, "mass_2"); positive(r, "distance")
    return {"gravitational_force": G * m1 * m2 / (r * r)}

"""Simple harmonic motion — period and frequency of a spring-mass system."""
import math
from ._base import positive, require

META = {
    "slug": "simple-harmonic-motion",
    "name": "Simple Harmonic Motion Calculator",
    "category": "physics",
    "description": "Calculate period, frequency, and angular frequency for a spring-mass system in simple harmonic motion.",
    "formula": "T = 2π·√(m/k);  f = 1/T;  ω = √(k/m)",
    "fields": [
        {"name": "mass", "label": "Mass (kg)", "type": "number", "min": 0, "required": True, "placeholder": "0.5"},
        {"name": "spring_constant", "label": "Spring Constant k (N/m)", "type": "number", "min": 0, "required": True, "placeholder": "50"},
    ],
    "outputs": [
        {"key": "period_seconds", "label": "Period T (s)", "format": "number"},
        {"key": "frequency_hz", "label": "Frequency f (Hz)", "format": "number"},
        {"key": "angular_frequency_rad_per_s", "label": "Angular Frequency ω (rad/s)", "format": "number"},
    ],
    "faq": [{"q": "What's SHM?", "a": "Motion where the restoring force is proportional to displacement (F = −kx). Springs, pendulums, oscillating molecules — all approximate SHM near equilibrium."}],
}

def calculate(inputs):
    m, k = require(inputs, "mass", "spring_constant")
    positive(m, "mass"); positive(k, "spring_constant")
    omega = math.sqrt(k / m)
    T = 2 * math.pi / omega
    return {
        "period_seconds": round(T, 6),
        "frequency_hz": round(1/T, 6),
        "angular_frequency_rad_per_s": round(omega, 6),
    }

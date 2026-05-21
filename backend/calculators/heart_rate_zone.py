"""Heart Rate Zone Calculator. Max HR = 220 − age. Zones defined as % of max."""
from typing import Any, Dict
from ._base import positive, require

ZONES = [
    ("Zone 1 — Very Light (recovery)", 0.50, 0.60),
    ("Zone 2 — Light (fat burn)", 0.60, 0.70),
    ("Zone 3 — Moderate (aerobic)", 0.70, 0.80),
    ("Zone 4 — Hard (anaerobic threshold)", 0.80, 0.90),
    ("Zone 5 — Max (VO₂ max)", 0.90, 1.00),
]

META = {
    "slug": "heart-rate-zone",
    "name": "Heart Rate Zone Calculator",
    "category": "health",
    "description": "Calculate the five heart rate training zones based on your age-predicted maximum.",
    "formula": "Max HR ≈ 220 − age; Zones = % of Max",
    "fields": [{"name": "age", "label": "Age", "type": "number", "min": 1, "required": True, "placeholder": "30"}],
    "outputs": [
        {"key": "max_hr", "label": "Max Heart Rate (bpm)", "format": "number"},
        {"key": "zones", "label": "Training Zones", "format": "table"},
    ],
    "faq": [{"q": "Is 220 − age accurate?", "a": "It's a population average. Individual max HR can vary by ±10–20 bpm — a treadmill test or chest-strap monitor will give a more personal number."}],
}

def calculate(inputs):
    (age,) = require(inputs, "age")
    positive(age, "age")
    max_hr = 220 - age
    zones = [{"zone": label, "low_bpm": round(max_hr * lo), "high_bpm": round(max_hr * hi)} for (label, lo, hi) in ZONES]
    return {"max_hr": round(max_hr, 0), "zones": zones}

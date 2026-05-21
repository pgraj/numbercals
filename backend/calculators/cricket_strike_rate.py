"""Cricket Strike Rate Impact Calculator.

Batting Strike Rate (SR) = (Runs / Balls Faced) × 100

Categorises the SR into game-context bands (Test, ODI, T20).
Optionally compares to a target SR to compute uplift required.
"""
from typing import Any, Dict
from ._base import non_negative, positive, require, to_float

META = {
    "slug": "cricket-strike-rate",
    "name": "Cricket Strike Rate Impact Calculator",
    "category": "sports",
    "description": "Calculate batting strike rate, compare to target, and assess performance in T20/ODI/Test contexts.",
    "formula": "SR = (Runs / Balls Faced) × 100",
    "fields": [
        {"name": "runs", "label": "Runs Scored", "type": "number", "min": 0, "required": True, "placeholder": "75"},
        {"name": "balls_faced", "label": "Balls Faced", "type": "number", "min": 1, "required": True, "placeholder": "50"},
        {"name": "format", "label": "Match Format", "type": "select", "required": True, "default": "t20",
         "options": [{"value": "test", "label": "Test"}, {"value": "odi", "label": "ODI"}, {"value": "t20", "label": "T20"}]},
        {"name": "target_strike_rate", "label": "Target SR (optional)", "type": "number", "min": 0, "required": False, "placeholder": "150"},
    ],
    "outputs": [
        {"key": "strike_rate", "label": "Strike Rate", "format": "number"},
        {"key": "rating", "label": "Performance Rating", "format": "text"},
        {"key": "runs_needed_to_match_target", "label": "Additional Runs Needed to Match Target SR", "format": "number"},
    ],
    "faq": [
        {"q": "What's a good strike rate?", "a": "Format-dependent. T20: 130+ is solid, 150+ is excellent. ODI: 90+ is solid, 110+ is excellent. Test: 50–60 is steady, 80+ is aggressive."},
    ],
}

BANDS = {
    "t20":  [(180, "Elite"), (150, "Excellent"), (130, "Solid"), (110, "Below par"), (0, "Poor")],
    "odi":  [(120, "Elite"), (100, "Excellent"), (85, "Solid"),  (70, "Below par"),  (0, "Poor")],
    "test": [(80,  "Aggressive / Elite"), (60, "Solid"), (45, "Steady"), (30, "Slow"), (0, "Defensive")],
}


def calculate(inputs):
    runs, balls = require(inputs, "runs", "balls_faced")
    non_negative(runs, "runs"); positive(balls, "balls_faced")
    fmt = str(inputs.get("format") or "t20").lower()
    if fmt not in BANDS: raise ValueError(f"Unknown format: {fmt}")

    sr = (runs / balls) * 100
    rating = next(label for thresh, label in BANDS[fmt] if sr >= thresh)

    extra = None
    target = inputs.get("target_strike_rate")
    if target not in (None, ""):
        t = to_float(target, "target_strike_rate")
        # runs_needed s.t. (runs + extra) / balls * 100 = t  =>  extra = t*balls/100 - runs
        extra = max((t * balls / 100) - runs, 0)

    return {
        "strike_rate": round(sr, 2),
        "rating": rating + (f" ({fmt.upper()})"),
        "runs_needed_to_match_target": round(extra, 1) if extra is not None else None,
    }

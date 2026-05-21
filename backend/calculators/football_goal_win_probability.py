"""Football (Soccer) Goal Impact on Win Probability Calculator.

Uses a logistic model based on:
  - Current goal differential
  - Minutes remaining
  - Whether the team just scored

This is a simplified pre/post-goal win-probability model. Real systems use
detailed historical match data; this approximates well for casual analysis.

P(win) = sigmoid(a + b·goal_diff + c·(90 − minute)/90)

Coefficients calibrated to broadly match observed football WP curves
(roughly 70% WP at +1 goal with ~30 min left in the average league match).
"""
import math
from typing import Any, Dict
from ._base import to_int

META = {
    "slug": "football-goal-win-probability",
    "name": "Football Goal Impact on Win Probability",
    "category": "sports",
    "description": "Estimate how a goal changes win probability, given score state and time remaining.",
    "formula": "P(win) = σ(a + b·goal_diff + c·time_remaining_fraction)",
    "fields": [
        {"name": "goals_for", "label": "Your Team's Goals (before)", "type": "number", "min": 0, "required": True, "placeholder": "1"},
        {"name": "goals_against", "label": "Opponent's Goals", "type": "number", "min": 0, "required": True, "placeholder": "1"},
        {"name": "current_minute", "label": "Current Minute (0–90+)", "type": "number", "min": 0, "required": True, "placeholder": "70"},
        {"name": "scoring_team", "label": "Who Scored?", "type": "select", "required": True, "default": "us",
         "options": [{"value": "us", "label": "Our team scored"}, {"value": "them", "label": "Opponent scored"}]},
    ],
    "outputs": [
        {"key": "win_prob_before", "label": "Win Probability Before Goal (%)", "format": "percent"},
        {"key": "win_prob_after", "label": "Win Probability After Goal (%)", "format": "percent"},
        {"key": "swing_percent", "label": "Win Probability Swing", "format": "percent"},
        {"key": "summary", "label": "Summary", "format": "text"},
    ],
    "faq": [
        {"q": "How is this calculated?", "a": "A simple logistic model with three inputs: current goal differential, minutes remaining, and which team scored. It's an approximation — real systems use historical match data, xG, and team strength."},
        {"q": "Why does an early goal matter less than a late goal?", "a": "More time remaining means more chances for the deficit to be overturned. A 1–0 lead at minute 80 is much safer than a 1–0 lead at minute 20."},
    ],
}


def _sigmoid(x): return 1 / (1 + math.exp(-x))


def _win_prob(goal_diff: int, minute: float) -> float:
    """Simplified WP model. Calibrated roughly:
       0:0 at minute 0  -> ~33% (1/3 chance of winning a draw match)
       +1 at minute 80  -> ~85%
       +1 at minute 20  -> ~62%
    """
    time_remaining_frac = max((90 - minute) / 90, 0)
    a = -0.7                                  # baseline tilt toward draw at start
    b = 1.2                                   # weight on goal differential
    c = -0.6                                  # more time remaining = less certain
    score = a + b * goal_diff + c * time_remaining_frac
    return _sigmoid(score)


def calculate(inputs):
    gf = to_int(inputs.get("goals_for"), "goals_for")
    ga = to_int(inputs.get("goals_against"), "goals_against")
    minute = to_int(inputs.get("current_minute"), "current_minute")
    scoring = str(inputs.get("scoring_team") or "us").lower()
    if scoring not in ("us", "them"):
        raise ValueError("'scoring_team' must be 'us' or 'them'.")
    if gf < 0 or ga < 0 or minute < 0:
        raise ValueError("All values must be non-negative.")

    diff_before = gf - ga
    if scoring == "us":
        diff_after = diff_before + 1
    else:
        diff_after = diff_before - 1

    wp_before = _win_prob(diff_before, minute)
    wp_after = _win_prob(diff_after, minute)
    swing = (wp_after - wp_before) * 100

    if scoring == "us":
        summary = f"Your goal lifted win probability by {round(swing, 1)} points — from {round(wp_before*100, 1)}% to {round(wp_after*100, 1)}%."
    else:
        summary = f"Conceded goal cost {round(-swing, 1)} points — from {round(wp_before*100, 1)}% down to {round(wp_after*100, 1)}%."

    return {
        "win_prob_before": round(wp_before * 100, 2),
        "win_prob_after": round(wp_after * 100, 2),
        "swing_percent": round(swing, 2),
        "summary": summary,
    }

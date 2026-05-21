"""Days Between Dates Calculator."""
from datetime import date
from typing import Any, Dict

META = {
    "slug": "days-between-dates",
    "name": "Days Between Dates Calculator",
    "category": "time",
    "description": "Calculate the number of days, weeks, months, and years between two dates.",
    "formula": "days = (end − start).days",
    "fields": [
        {"name": "start_date", "label": "Start Date", "type": "date", "required": True},
        {"name": "end_date", "label": "End Date", "type": "date", "required": True},
    ],
    "outputs": [
        {"key": "days", "label": "Days", "format": "number"},
        {"key": "weeks", "label": "Weeks (approx)", "format": "number"},
        {"key": "months", "label": "Months (approx)", "format": "number"},
        {"key": "years", "label": "Years (approx)", "format": "number"},
    ],
    "faq": [{"q": "Why are weeks/months 'approx'?", "a": "Months and years have variable day counts. We compute exact days, then divide by averages (7, 30.44, 365.25)."}],
}

def _parse(d: Any, name: str) -> date:
    if not d: raise ValueError(f"'{name}' is required.")
    try:
        return date.fromisoformat(str(d).strip())
    except ValueError:
        raise ValueError(f"'{name}' must be a valid date (YYYY-MM-DD).")

def calculate(inputs):
    s = _parse(inputs.get("start_date"), "start_date")
    e = _parse(inputs.get("end_date"), "end_date")
    days = abs((e - s).days)
    return {
        "days": days,
        "weeks": round(days / 7, 2),
        "months": round(days / 30.44, 2),
        "years": round(days / 365.25, 4),
    }

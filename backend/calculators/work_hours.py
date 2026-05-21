"""Work Hours Calculator. Computes hours between start/end with optional unpaid break."""
from datetime import datetime, timedelta
from typing import Any, Dict
from ._base import non_negative, to_float

META = {
    "slug": "work-hours",
    "name": "Work Hours Calculator",
    "category": "time",
    "description": "Calculate hours worked between two times, subtracting break duration.",
    "formula": "hours = end − start − break_minutes/60",
    "fields": [
        {"name": "start_time", "label": "Start Time (HH:MM)", "type": "time", "required": True, "placeholder": "09:00"},
        {"name": "end_time", "label": "End Time (HH:MM)", "type": "time", "required": True, "placeholder": "17:30"},
        {"name": "break_minutes", "label": "Break (minutes)", "type": "number", "min": 0, "required": False, "placeholder": "30"},
    ],
    "outputs": [
        {"key": "total_hours", "label": "Hours Worked", "format": "number"},
        {"key": "total_minutes", "label": "Minutes Worked", "format": "number"},
    ],
    "faq": [{"q": "Crosses midnight?", "a": "If end time is earlier than start, the calculator assumes the shift crossed midnight and adds 24 hours."}],
}

def _parse(t: Any, name: str) -> datetime:
    if not t: raise ValueError(f"'{name}' is required.")
    try:
        return datetime.strptime(str(t).strip(), "%H:%M")
    except ValueError:
        raise ValueError(f"'{name}' must be in HH:MM format (got {t!r}).")

def calculate(inputs):
    start = _parse(inputs.get("start_time"), "start_time")
    end = _parse(inputs.get("end_time"), "end_time")
    if end <= start:
        end += timedelta(days=1)
    brk = to_float(inputs["break_minutes"] if inputs.get("break_minutes") not in (None, "") else 0, "break_minutes")
    non_negative(brk, "break_minutes")
    total_minutes = (end - start).total_seconds() / 60 - brk
    if total_minutes < 0:
        raise ValueError("Break is longer than working window.")
    return {"total_hours": round(total_minutes / 60, 2), "total_minutes": round(total_minutes, 0)}

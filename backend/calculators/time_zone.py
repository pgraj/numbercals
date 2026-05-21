"""Time Zone Converter.

Converts a datetime from one IANA time zone to another.
Uses stdlib zoneinfo (Python 3.9+).
"""
from datetime import datetime
from typing import Any, Dict
from zoneinfo import ZoneInfo, available_timezones

# Common short-list of zones for the dropdown; full list available via API.
COMMON_ZONES = [
    "UTC", "Australia/Sydney", "Australia/Melbourne", "Australia/Perth",
    "Asia/Dubai", "Asia/Kolkata", "Asia/Singapore", "Asia/Tokyo", "Asia/Shanghai",
    "Europe/London", "Europe/Paris", "Europe/Berlin", "Europe/Moscow",
    "America/New_York", "America/Chicago", "America/Denver", "America/Los_Angeles",
    "America/Toronto", "America/Sao_Paulo", "Pacific/Auckland",
]

META = {
    "slug": "time-zone",
    "name": "Time Zone Converter",
    "category": "time",
    "description": "Convert a date/time from one time zone to another.",
    "formula": "Localise to source TZ → convert to target TZ via zoneinfo.",
    "fields": [
        {"name": "datetime_local", "label": "Date & Time", "type": "datetime-local", "required": True},
        {"name": "from_zone", "label": "From Time Zone", "type": "select", "required": True, "default": "UTC",
         "options": [{"value": z, "label": z} for z in COMMON_ZONES]},
        {"name": "to_zone", "label": "To Time Zone", "type": "select", "required": True, "default": "Australia/Sydney",
         "options": [{"value": z, "label": z} for z in COMMON_ZONES]},
    ],
    "outputs": [
        {"key": "converted", "label": "Converted Time", "format": "text"},
        {"key": "iso", "label": "ISO 8601", "format": "text"},
        {"key": "offset_difference_hours", "label": "Offset Difference (hours)", "format": "number"},
    ],
    "faq": [
        {"q": "Does this handle daylight saving?", "a": "Yes — zoneinfo uses the IANA tz database, which encodes DST rules for each region historically and forward."},
    ],
}


def calculate(inputs: Dict[str, Any]) -> Dict[str, Any]:
    dt_str = inputs.get("datetime_local")
    if not dt_str:
        raise ValueError("'datetime_local' is required.")
    from_zone = str(inputs.get("from_zone") or "UTC")
    to_zone = str(inputs.get("to_zone") or "UTC")
    tzs = available_timezones()
    if from_zone not in tzs:
        raise ValueError(f"Unknown 'from_zone': {from_zone}")
    if to_zone not in tzs:
        raise ValueError(f"Unknown 'to_zone': {to_zone}")
    try:
        # Accept "YYYY-MM-DDTHH:MM" or with seconds.
        naive = datetime.fromisoformat(str(dt_str).strip().replace(" ", "T"))
    except ValueError:
        raise ValueError("Could not parse 'datetime_local'. Use ISO format YYYY-MM-DDTHH:MM.")
    src = naive.replace(tzinfo=ZoneInfo(from_zone))
    dst = src.astimezone(ZoneInfo(to_zone))
    diff_h = (dst.utcoffset().total_seconds() - src.utcoffset().total_seconds()) / 3600
    return {
        "converted": dst.strftime("%Y-%m-%d %H:%M %Z"),
        "iso": dst.isoformat(),
        "offset_difference_hours": round(diff_h, 2),
    }

"""Body Fat Calculator — US Navy method.

Men:   495 / (1.0324 − 0.19077·log10(waist−neck) + 0.15456·log10(height)) − 450
Women: 495 / (1.29579 − 0.35004·log10(waist+hip−neck) + 0.22100·log10(height)) − 450
(all measurements in cm)
"""
import math
from typing import Any, Dict
from ._base import positive, require, to_float

META = {
    "slug": "body-fat",
    "name": "Body Fat Calculator (US Navy)",
    "category": "health",
    "description": "Estimate body fat percentage using the US Navy circumference method.",
    "formula": "US Navy circumference method (cm)",
    "fields": [
        {"name": "sex", "label": "Sex", "type": "select", "options": [{"value": "male", "label": "Male"}, {"value": "female", "label": "Female"}], "required": True, "default": "male"},
        {"name": "height_cm", "label": "Height (cm)", "type": "number", "min": 1, "required": True, "placeholder": "175"},
        {"name": "neck_cm", "label": "Neck (cm)", "type": "number", "min": 1, "required": True, "placeholder": "38"},
        {"name": "waist_cm", "label": "Waist (cm)", "type": "number", "min": 1, "required": True, "placeholder": "85"},
        {"name": "hip_cm", "label": "Hip (cm, women only)", "type": "number", "min": 0, "required": False, "placeholder": "95"},
    ],
    "outputs": [{"key": "body_fat_percent", "label": "Body Fat (%)", "format": "percent"}],
    "faq": [{"q": "How accurate is the Navy method?", "a": "Within ~3–4% of DEXA scans for most adults — much better than BMI for body composition, though not as accurate as a true scan."}],
}

def calculate(inputs):
    sex = str(inputs.get("sex", "male")).lower()
    h, neck, waist = require(inputs, "height_cm", "neck_cm", "waist_cm")
    positive(h, "height_cm"); positive(neck, "neck_cm"); positive(waist, "waist_cm")
    if sex == "male":
        if waist - neck <= 0:
            raise ValueError("Waist must be larger than neck.")
        bf = 495 / (1.0324 - 0.19077 * math.log10(waist - neck) + 0.15456 * math.log10(h)) - 450
    else:
        hip = to_float(inputs.get("hip_cm"), "hip_cm")
        positive(hip, "hip_cm")
        if waist + hip - neck <= 0:
            raise ValueError("Waist + hip must exceed neck.")
        bf = 495 / (1.29579 - 0.35004 * math.log10(waist + hip - neck) + 0.22100 * math.log10(h)) - 450
    return {"body_fat_percent": round(max(bf, 0), 2)}

"""Trigonometry calculator — sin/cos/tan and inverses, in degrees or radians."""
import math
from ._base import to_float

META = {
    "slug": "trigonometry",
    "name": "Trigonometry Calculator",
    "category": "math",
    "description": "Compute sin/cos/tan/sec/csc/cot of an angle, or arcsin/arccos/arctan of a value.",
    "formula": "sin θ, cos θ, tan θ (and inverses); choose degrees or radians",
    "fields": [
        {"name": "function", "label": "Function", "type": "select", "required": True, "default": "sin",
         "options": [
             {"value": "sin", "label": "sin"}, {"value": "cos", "label": "cos"}, {"value": "tan", "label": "tan"},
             {"value": "sec", "label": "sec (= 1/cos)"}, {"value": "csc", "label": "csc (= 1/sin)"}, {"value": "cot", "label": "cot (= 1/tan)"},
             {"value": "asin", "label": "arcsin (input in [−1, 1])"},
             {"value": "acos", "label": "arccos (input in [−1, 1])"},
             {"value": "atan", "label": "arctan (any input)"},
         ]},
        {"name": "unit", "label": "Angle Unit", "type": "select", "required": True, "default": "degrees",
         "options": [{"value": "degrees", "label": "Degrees"}, {"value": "radians", "label": "Radians"}]},
        {"name": "value", "label": "Input value", "type": "number", "required": True, "placeholder": "30"},
    ],
    "outputs": [{"key": "result", "label": "Result", "format": "number"}],
    "faq": [{"q": "Why is tan(90°) undefined?", "a": "Because cos(90°) = 0 and tan = sin/cos. Division by zero. Computers usually return a huge number; this calculator catches it."}],
}

def calculate(inputs):
    func = str(inputs.get("function", "sin"))
    unit = str(inputs.get("unit", "degrees"))
    val = to_float(inputs.get("value"), "value")
    # Forward trig: convert input to radians if needed
    if func in {"sin","cos","tan","sec","csc","cot"}:
        rad = math.radians(val) if unit == "degrees" else val
        if func == "sin": r = math.sin(rad)
        elif func == "cos": r = math.cos(rad)
        elif func == "tan":
            if abs(math.cos(rad)) < 1e-15: raise ValueError("tan is undefined at this angle.")
            r = math.tan(rad)
        elif func == "sec":
            c = math.cos(rad)
            if abs(c) < 1e-15: raise ValueError("sec is undefined where cos = 0.")
            r = 1/c
        elif func == "csc":
            s = math.sin(rad)
            if abs(s) < 1e-15: raise ValueError("csc is undefined where sin = 0.")
            r = 1/s
        elif func == "cot":
            t = math.tan(rad)
            if abs(t) < 1e-15: raise ValueError("cot is undefined where tan = 0.")
            r = 1/t
    else:
        # Inverse trig: output in chosen unit
        if func in {"asin","acos"} and not -1 <= val <= 1:
            raise ValueError(f"{func} input must be in [-1, 1].")
        if func == "asin": r = math.asin(val)
        elif func == "acos": r = math.acos(val)
        elif func == "atan": r = math.atan(val)
        if unit == "degrees": r = math.degrees(r)
    return {"result": round(r, 8)}

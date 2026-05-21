"""Exponential calculator — compute b^x for any base and exponent."""
import math
from ._base import to_float

META = {
    "slug": "exponential",
    "name": "Exponential Calculator",
    "category": "math",
    "description": "Compute b^x (b raised to the power x) for any base and exponent, including e^x.",
    "formula": "result = base^exponent",
    "fields": [
        {"name": "base_choice", "label": "Base", "type": "select", "required": True, "default": "custom",
         "options": [
             {"value": "e", "label": "e (Euler's number ≈ 2.71828)"},
             {"value": "10", "label": "10"},
             {"value": "2", "label": "2"},
             {"value": "custom", "label": "Custom base"},
         ]},
        {"name": "custom_base", "label": "Custom base (only if 'Custom')", "type": "number", "required": False, "placeholder": "3"},
        {"name": "exponent", "label": "Exponent", "type": "number", "required": True, "placeholder": "4"},
    ],
    "outputs": [{"key": "result", "label": "Result", "format": "number"}],
    "faq": [{"q": "What's e?", "a": "Euler's number, ≈ 2.71828. The base of natural logarithms. e^x is the function whose derivative equals itself."}],
}

def calculate(inputs):
    choice = str(inputs.get("base_choice", "custom"))
    exp = to_float(inputs.get("exponent"), "exponent")
    if choice == "e": base = math.e
    elif choice == "10": base = 10.0
    elif choice == "2": base = 2.0
    elif choice == "custom": base = to_float(inputs.get("custom_base"), "custom_base")
    else: raise ValueError(f"Unknown base: {choice}")
    if base <= 0 and not float(exp).is_integer():
        raise ValueError("Cannot raise a non-positive base to a non-integer exponent.")
    return {"result": round(base ** exp, 8)}

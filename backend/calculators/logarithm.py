"""Logarithm calculator — log base e, base 10, or custom base."""
import math
from ._base import positive, to_float

META = {
    "slug": "logarithm",
    "name": "Logarithm Calculator",
    "category": "math",
    "description": "Compute logarithms in any base — natural log (ln), common log (log₁₀), or a custom base.",
    "formula": "log_b(x) = ln(x) / ln(b)",
    "fields": [
        {"name": "value", "label": "Value (must be > 0)", "type": "number", "min": 0, "required": True, "placeholder": "100"},
        {"name": "base", "label": "Base", "type": "select", "required": True, "default": "10",
         "options": [
             {"value": "10", "label": "10 (common log)"},
             {"value": "e", "label": "e ≈ 2.718 (natural log)"},
             {"value": "2", "label": "2 (binary log)"},
             {"value": "custom", "label": "Custom base"},
         ]},
        {"name": "custom_base", "label": "Custom base (only if 'Custom' selected)", "type": "number", "min": 0, "required": False, "placeholder": "5"},
    ],
    "outputs": [{"key": "result", "label": "Logarithm", "format": "number"}],
    "faq": [{"q": "What's a logarithm?", "a": "The inverse of exponentiation. log₁₀(100) = 2 because 10² = 100. log₂(8) = 3 because 2³ = 8."}],
}

def calculate(inputs):
    val = to_float(inputs.get("value"), "value")
    positive(val, "value")
    base = str(inputs.get("base", "10"))
    if base == "10": return {"result": round(math.log10(val), 8)}
    if base == "e": return {"result": round(math.log(val), 8)}
    if base == "2": return {"result": round(math.log2(val), 8)}
    if base == "custom":
        b = to_float(inputs.get("custom_base"), "custom_base")
        positive(b, "custom_base")
        if b == 1: raise ValueError("Logarithm base cannot be 1.")
        return {"result": round(math.log(val) / math.log(b), 8)}
    raise ValueError(f"Unknown base: {base}")

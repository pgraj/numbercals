"""Concrete Volume Calculator — for slabs, footings, columns.

NOTE: Volume only. This calculator does NOT compute strength, load capacity,
or any structural property. For engineering decisions, consult a qualified
civil/structural engineer.
"""
from ._base import positive, require, to_float

META = {
    "slug": "concrete-volume",
    "name": "Concrete Volume Calculator",
    "category": "engineering",
    "description": "Calculate the volume of concrete needed for slabs, footings, or columns. For quantity estimation only — not structural design.",
    "formula": "Slab: V = L·W·D;  Column: V = π·r²·h;  + 5–10% wastage allowance",
    "fields": [
        {"name": "shape", "label": "Shape", "type": "select", "required": True, "default": "slab",
         "options": [
             {"value": "slab", "label": "Slab / Footing (rectangular)"},
             {"value": "column", "label": "Column (cylindrical)"},
         ]},
        {"name": "length", "label": "Length (m, slab only)", "type": "number", "min": 0, "required": False, "placeholder": "10"},
        {"name": "width", "label": "Width (m, slab only)", "type": "number", "min": 0, "required": False, "placeholder": "5"},
        {"name": "diameter", "label": "Diameter (m, column only)", "type": "number", "min": 0, "required": False, "placeholder": "0.3"},
        {"name": "depth_or_height", "label": "Depth or Height (m)", "type": "number", "min": 0, "required": True, "placeholder": "0.15"},
        {"name": "wastage_percent", "label": "Wastage allowance (%, default 10)", "type": "number", "min": 0, "required": False, "placeholder": "10"},
    ],
    "outputs": [
        {"key": "volume_m3", "label": "Net Volume (m³)", "format": "number"},
        {"key": "volume_with_wastage_m3", "label": "Volume with Wastage (m³)", "format": "number"},
        {"key": "volume_yd3", "label": "Volume (cubic yards)", "format": "number"},
    ],
    "faq": [
        {"q": "Why include wastage?", "a": "Real-world concrete pours always lose some volume to spillage, form leaks, irregular sub-grades, and pump line residue. 5–10% is typical; tight forms can use 5%, complex pours 15%."},
        {"q": "What about reinforcement?", "a": "This calculator gives concrete volume only. For rebar weight estimation, you need separate structural drawings — that's beyond this tool's scope."},
        {"q": "Is this structural advice?", "a": "No. This computes quantity for ordering. Slab thickness, footing depth, and column dimensions must be determined by a qualified structural engineer based on loads, soil, and codes."},
    ],
}

def calculate(inputs):
    import math
    shape = str(inputs.get("shape", "slab"))
    (d,) = require(inputs, "depth_or_height")
    positive(d, "depth_or_height")
    wastage = to_float(inputs["wastage_percent"] if inputs.get("wastage_percent") not in (None, "") else 10, "wastage_percent")
    if wastage < 0: raise ValueError("Wastage cannot be negative.")

    if shape == "slab":
        L = to_float(inputs.get("length"), "length"); W = to_float(inputs.get("width"), "width")
        positive(L, "length"); positive(W, "width")
        v = L * W * d
    elif shape == "column":
        diam = to_float(inputs.get("diameter"), "diameter")
        positive(diam, "diameter")
        v = math.pi * (diam/2)**2 * d
    else:
        raise ValueError(f"Unknown shape: {shape}")

    v_with = v * (1 + wastage/100)
    return {
        "volume_m3": round(v, 4),
        "volume_with_wastage_m3": round(v_with, 4),
        "volume_yd3": round(v_with * 1.30795, 4),
    }

"""Brick / block quantity estimator for a wall."""
from ._base import positive, require, to_float

META = {
    "slug": "brick-quantity",
    "name": "Brick Quantity Calculator",
    "category": "engineering",
    "description": "Estimate the number of bricks needed for a wall, including a mortar and wastage allowance.",
    "formula": "Wall area / Brick face area × wastage allowance",
    "fields": [
        {"name": "wall_length_m", "label": "Wall Length (m)", "type": "number", "min": 0, "required": True, "placeholder": "10"},
        {"name": "wall_height_m", "label": "Wall Height (m)", "type": "number", "min": 0, "required": True, "placeholder": "2.5"},
        {"name": "brick_length_mm", "label": "Brick Length (mm)", "type": "number", "min": 0, "required": True, "placeholder": "230"},
        {"name": "brick_height_mm", "label": "Brick Height (mm)", "type": "number", "min": 0, "required": True, "placeholder": "76"},
        {"name": "mortar_thickness_mm", "label": "Mortar Joint Thickness (mm)", "type": "number", "min": 0, "required": False, "placeholder": "10"},
        {"name": "wastage_percent", "label": "Wastage (%, default 5)", "type": "number", "min": 0, "required": False, "placeholder": "5"},
    ],
    "outputs": [
        {"key": "bricks_needed", "label": "Bricks Needed (with wastage)", "format": "number"},
        {"key": "wall_area_m2", "label": "Wall Area (m²)", "format": "number"},
    ],
    "faq": [
        {"q": "Does this account for openings?", "a": "No — calculate wall area minus window/door openings first, then plug that in by entering equivalent dimensions, OR estimate the full wall and subtract bricks for openings manually."},
        {"q": "Why include mortar in brick dimensions?", "a": "Because each brick effectively occupies (brick_length + mortar) × (brick_height + mortar) of wall space. The calculator handles this for you."},
    ],
}

def calculate(inputs):
    L, H, bL, bH = require(inputs, "wall_length_m", "wall_height_m", "brick_length_mm", "brick_height_mm")
    positive(L, "wall_length_m"); positive(H, "wall_height_m")
    positive(bL, "brick_length_mm"); positive(bH, "brick_height_mm")
    mortar = to_float(inputs["mortar_thickness_mm"] if inputs.get("mortar_thickness_mm") not in (None, "") else 10, "mortar_thickness_mm")
    wastage = to_float(inputs["wastage_percent"] if inputs.get("wastage_percent") not in (None, "") else 5, "wastage_percent")
    if mortar < 0 or wastage < 0:
        raise ValueError("Mortar and wastage must be non-negative.")
    wall_area = L * H
    brick_with_mortar_area = ((bL + mortar) / 1000) * ((bH + mortar) / 1000)
    bricks = wall_area / brick_with_mortar_area
    return {
        "bricks_needed": int(bricks * (1 + wastage/100) + 0.5),
        "wall_area_m2": round(wall_area, 4),
    }

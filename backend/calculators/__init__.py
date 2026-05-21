"""NumberCals calculator modules.

Each calculator is a self-contained module exposing:
  - META: dict describing the calculator (slug, name, category, fields, formula)
  - calculate(inputs: dict) -> dict: executes the formula and returns results

To add a new calculator: drop a new file in this folder following the
template in `_base.py`, then add it to `registry.py`.
"""

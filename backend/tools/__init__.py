"""
backend/tools/__init__.py
=========================
Registry of "tool" modules — distinct from `calculators/` because tools have
richer UIs (maps, canvases, multi-step inputs) instead of a simple form.

To add a new tool:
    1. Drop a new module here, e.g. `network_signal_planner.py`
    2. Give it a META dict and an `optimize()` (or equivalent) function
    3. Add the import + slug entry below

This file is the single source of truth for what tools exist. The FastAPI
routes in `main.py` read TOOL_REGISTRY to dispatch URLs.
"""

from . import cable_network

TOOL_REGISTRY = {
    cable_network.META["slug"]: cable_network,
    # add more tools here as you build them, e.g.
    # signal_loss_estimator.META["slug"]: signal_loss_estimator,
}

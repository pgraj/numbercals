"""Base contract for all calculators.

Every calculator file MUST expose:
  1. META: dict — see CalculatorMeta shape below
  2. calculate(inputs: dict) -> dict — pure function, takes validated inputs,
     returns results. Raise ValueError for any input-validation failure;
     the API layer translates these into HTTP 400 responses.

This file also provides helpers:
  - require(inputs, *names) — fetches required numeric inputs or raises.
  - to_float(value, name)   — coerces to float with clear error messaging.

Keeping each calculator in its own file means: one bug = one file to open.
The registry is the only thing that knows about all of them.
"""
from typing import Any, Dict, Iterable, Tuple


def to_float(value: Any, name: str) -> float:
    """Coerce a value to float, raising ValueError with a useful message."""
    if value is None or value == "":
        raise ValueError(f"'{name}' is required.")
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"'{name}' must be a number (got {value!r}).")


def to_int(value: Any, name: str) -> int:
    """Coerce a value to int, raising ValueError with a useful message."""
    if value is None or value == "":
        raise ValueError(f"'{name}' is required.")
    try:
        f = float(value)
        if f != int(f):
            raise ValueError(f"'{name}' must be a whole number (got {value!r}).")
        return int(f)
    except (TypeError, ValueError) as e:
        if isinstance(e, ValueError) and str(e).startswith("'"):
            raise
        raise ValueError(f"'{name}' must be an integer (got {value!r}).")


def require(inputs: Dict[str, Any], *names: str) -> Tuple[float, ...]:
    """Pull required float inputs in order. Shortcut for the common case."""
    return tuple(to_float(inputs.get(n), n) for n in names)


def positive(value: float, name: str) -> float:
    """Raise if value <= 0."""
    if value <= 0:
        raise ValueError(f"'{name}' must be greater than 0.")
    return value


def non_negative(value: float, name: str) -> float:
    """Raise if value < 0."""
    if value < 0:
        raise ValueError(f"'{name}' must be 0 or greater.")
    return value

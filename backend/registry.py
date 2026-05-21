"""Calculator Registry — the single dispatcher.

Each calculator module is imported explicitly here. The frontend selects a
calculator by slug; the registry hands back the matching module.

To DISABLE a broken calculator while debugging: comment out its import
and its REGISTRY entry. The rest of the platform keeps working.
To ADD a new calculator:
  1. Create calculators/<name>.py following the contract in _base.py
  2. Add an import below
  3. Add it to the REGISTRY list

That's it. No formula registry, no central switch — just one file per
calculator, registered explicitly here.
"""
from types import ModuleType
from typing import Dict, List

# Finance --------------------------------------------------------------------
from calculators import simple_interest
from calculators import compound_interest
from calculators import loan_emi
from calculators import mortgage
from calculators import roi
from calculators import cagr
from calculators import break_even_basic
from calculators import profit_margin
from calculators import discount
from calculators import future_value
from calculators import investment_growth
from calculators import dividend
from calculators import sip
from calculators import amortization
from calculators import interest_rate

# Health ---------------------------------------------------------------------
from calculators import bmi
from calculators import bmr
from calculators import tdee
from calculators import body_fat
from calculators import calorie
from calculators import ideal_weight
from calculators import water_intake
from calculators import heart_rate_zone

# Math -----------------------------------------------------------------------
from calculators import percentage
from calculators import fraction
from calculators import ratio
from calculators import average
from calculators import median
from calculators import mode
from calculators import standard_deviation
from calculators import variance
from calculators import probability
from calculators import permutation
from calculators import combination
from calculators import lcm
from calculators import gcd
from calculators import quadratic
from calculators import linear_equation

# Time & Motion --------------------------------------------------------------
from calculators import speed
from calculators import distance
from calculators import time_calc
from calculators import acceleration
from calculators import work_hours
from calculators import days_between
from calculators import time_zone

# Physics --------------------------------------------------------------------
from calculators import force
from calculators import kinetic_energy
from calculators import potential_energy
from calculators import work_done
from calculators import density
from calculators import pressure
from calculators import power_electrical
from calculators import ohms_law

# Business -------------------------------------------------------------------
from calculators import conversion_rate
from calculators import markup
from calculators import commission
from calculators import revenue

# Bucket 2 — Impact / Simulation calculators ---------------------------------
# Property
from calculators import rental_yield
from calculators import buy_vs_rent
from calculators import property_roi_advanced
from calculators import mortgage_stress_test
from calculators import cashflow_simulation
# Finance impact
from calculators import inflation_impact
from calculators import salary_increase_impact
from calculators import interest_rate_change_impact
# Business impact + SaaS
from calculators import revenue_impact
from calculators import price_change_impact
from calculators import marketing_spend_impact
from calculators import cac_impact
from calculators import ltv_growth_simulator
# Sports
from calculators import cricket_strike_rate
from calculators import football_goal_win_probability

# Bucket 3 — Geometry, advanced math, physics, astronomy, engineering -------
# Geometry — 2D
from calculators import area_square
from calculators import area_rectangle
from calculators import area_triangle
from calculators import area_circle
from calculators import area_parallelogram
from calculators import area_trapezoid
from calculators import area_rhombus
from calculators import area_ellipse
from calculators import regular_polygon
# Geometry — 3D
from calculators import volume_cube
from calculators import volume_cuboid
from calculators import volume_sphere
from calculators import volume_cylinder
from calculators import volume_cone
from calculators import volume_pyramid
from calculators import volume_torus
# Math — advanced
from calculators import pythagoras
from calculators import distance_formula
from calculators import distance_formula_3d
from calculators import midpoint
from calculators import slope
from calculators import trigonometry
from calculators import logarithm
from calculators import exponential
# Physics — Newton, momentum, gravity, projectile, oscillation
from calculators import weight
from calculators import momentum
from calculators import impulse
from calculators import universal_gravitation
from calculators import escape_velocity
from calculators import orbital_period
from calculators import projectile_motion
from calculators import pendulum_period
from calculators import simple_harmonic_motion
# Engineering — concrete, beam, brick
from calculators import concrete_volume
from calculators import beam_deflection_simple
from calculators import brick_quantity


# The full list — order here is the order shown on category pages.
ALL_MODULES: List[ModuleType] = [
    # Finance
    simple_interest, compound_interest, loan_emi, mortgage, roi, cagr,
    profit_margin, discount,
    future_value, investment_growth, dividend, sip, amortization,
    interest_rate,
    # Finance impact (Bucket 2)
    inflation_impact, salary_increase_impact, interest_rate_change_impact,
    # Health
    bmi, bmr, tdee, body_fat, calorie, ideal_weight, water_intake, heart_rate_zone,
    # Math
    percentage, fraction, ratio, average, median, mode, standard_deviation,
    variance, probability, permutation, combination, lcm, gcd, quadratic, linear_equation,
    # Math — advanced (Bucket 3)
    pythagoras, distance_formula, distance_formula_3d, midpoint, slope,
    trigonometry, logarithm, exponential,
    # Time & Motion
    speed, distance, time_calc, acceleration, work_hours, days_between, time_zone,
    # Physics
    force, kinetic_energy, potential_energy, work_done, density, pressure,
    power_electrical, ohms_law,
    # Physics — advanced (Bucket 3)
    weight, momentum, impulse, universal_gravitation, escape_velocity,
    orbital_period, projectile_motion, pendulum_period, simple_harmonic_motion,
    # Business
    break_even_basic, conversion_rate, markup, commission, revenue,
    # Business impact + SaaS (Bucket 2)
    revenue_impact, price_change_impact, marketing_spend_impact,
    cac_impact, ltv_growth_simulator,
    # Property (Bucket 2)
    rental_yield, buy_vs_rent, property_roi_advanced,
    mortgage_stress_test, cashflow_simulation,
    # Sports (Bucket 2)
    cricket_strike_rate, football_goal_win_probability,
    # Geometry (Bucket 3) — 2D
    area_square, area_rectangle, area_triangle, area_circle,
    area_parallelogram, area_trapezoid, area_rhombus, area_ellipse, regular_polygon,
    # Geometry (Bucket 3) — 3D
    volume_cube, volume_cuboid, volume_sphere, volume_cylinder,
    volume_cone, volume_pyramid, volume_torus,
    # Engineering (Bucket 3)
    concrete_volume, beam_deflection_simple, brick_quantity,
]


REGISTRY: Dict[str, ModuleType] = {mod.META["slug"]: mod for mod in ALL_MODULES}


# Category labels for nav.
CATEGORIES = [
    {"slug": "finance", "name": "Finance"},
    {"slug": "health", "name": "Health"},
    {"slug": "math", "name": "Math"},
    {"slug": "geometry", "name": "Geometry"},
    {"slug": "time", "name": "Time & Motion"},
    {"slug": "physics", "name": "Physics"},
    {"slug": "engineering", "name": "Engineering"},
    {"slug": "business", "name": "Business"},
    {"slug": "property", "name": "Property"},
    {"slug": "sports", "name": "Sports"},
]


def get(slug: str) -> ModuleType:
    """Fetch a calculator module by slug. Raises KeyError if not found."""
    if slug not in REGISTRY:
        raise KeyError(f"No calculator registered with slug '{slug}'.")
    return REGISTRY[slug]


def list_by_category(category: str) -> List[ModuleType]:
    """All calculators in a given category, in display order."""
    return [m for m in ALL_MODULES if m.META["category"] == category]


def related(slug: str, limit: int = 5) -> List[ModuleType]:
    """Same-category calculators excluding the given one — used for internal linking / SEO."""
    if slug not in REGISTRY:
        return []
    cat = REGISTRY[slug].META["category"]
    siblings = [m for m in ALL_MODULES if m.META["category"] == cat and m.META["slug"] != slug]
    return siblings[:limit]

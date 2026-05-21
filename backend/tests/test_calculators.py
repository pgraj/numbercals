"""Comprehensive pytest suite for all 75 calculators.

Tests three classes of cases:
  1. HAPPY PATH      — typical inputs, verify output structure and types
  2. REFERENCE VALUE — hand-computed expected outputs for accuracy verification
  3. ERROR PATH      — invalid inputs raise ValueError (HTTP 400 from API)

Run from /backend with:
    pytest tests/ -v
    pytest tests/ -v --tb=short    # less verbose tracebacks
    pytest tests/ --md=TEST_REPORT.md  # if pytest-md installed
"""
import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import registry

# =============================================================================
# REFERENCE VALUES — hand-computed; verifies calculator MATH is correct.
# =============================================================================
# Format: (slug, inputs, {output_key: expected_value}, tolerance)
# Tolerance: relative for non-zero, absolute for zero.

REFERENCE_CASES = [
    # --- Finance ---
    ("simple-interest",
     {"principal": 10000, "rate": 5, "time": 3},
     {"interest": 1500.0, "total_amount": 11500.0}, 0.001),

    ("compound-interest",
     {"principal": 10000, "rate": 5, "time": 10, "compounds_per_year": 1},
     # 10000 * 1.05^10 = 16288.95
     {"final_amount": 16288.95, "interest_earned": 6288.95}, 0.001),

    ("loan-emi",
     {"principal": 100000, "annual_rate": 6, "tenure_months": 12},
     # Standard EMI = 100000 * 0.005 * 1.005^12 / (1.005^12 - 1) = 8606.64
     {"emi": 8606.64}, 0.01),

    ("roi",
     {"initial_investment": 1000, "final_value": 1500},
     {"net_gain": 500.0, "roi_percent": 50.0}, 0.001),

    ("cagr",
     {"start_value": 1000, "end_value": 2000, "years": 10},
     # 2^(1/10) - 1 = 0.07177 = 7.177%
     {"cagr_percent": 7.1773}, 0.001),

    ("discount",
     {"original_price": 200, "discount_percent": 25},
     {"final_price": 150.0, "amount_saved": 50.0}, 0.001),

    ("future-value",
     {"present_value": 1000, "annual_rate": 8, "years": 5},
     # 1000 * 1.08^5 = 1469.33
     {"future_value": 1469.33}, 0.001),

    # --- Health ---
    ("bmi",
     {"weight_kg": 70, "height_cm": 175},
     # 70 / 1.75² = 22.857
     {"bmi": 22.86, "category": "Normal weight"}, 0.001),

    ("bmi",
     {"weight_kg": 50, "height_cm": 170},
     # 50 / 1.7² = 17.30 → Underweight
     {"bmi": 17.30, "category": "Underweight"}, 0.01),

    ("bmi",
     {"weight_kg": 95, "height_cm": 175},
     # 95 / 1.75² = 31.02 → Obese
     {"bmi": 31.02, "category": "Obese"}, 0.01),

    ("bmr",
     {"weight_kg": 70, "height_cm": 175, "age": 30, "sex": "male"},
     # Mifflin-St Jeor: 10*70 + 6.25*175 - 5*30 + 5 = 700+1093.75-150+5 = 1648.75 → 1649
     {"bmr": 1649}, 1),

    ("bmr",
     {"weight_kg": 60, "height_cm": 165, "age": 30, "sex": "female"},
     # 10*60 + 6.25*165 - 5*30 - 161 = 600+1031.25-150-161 = 1320.25 → 1320
     {"bmr": 1320}, 1),

    ("tdee",
     {"weight_kg": 70, "height_cm": 175, "age": 30, "sex": "male", "activity": "sedentary"},
     # BMR * 1.2 = 1648.75 * 1.2 = 1978.5 → 1979
     {"tdee": 1979}, 1),

    # --- Math ---
    ("percentage",
     {"mode": "of", "x": 20, "y": 150},
     # 20% of 150 = 30
     {"result": 30.0}, 0.001),

    ("percentage",
     {"mode": "is_what_percent", "x": 25, "y": 200},
     # 25 is 12.5% of 200
     {"result": 12.5}, 0.001),

    ("percentage",
     {"mode": "change", "x": 100, "y": 125},
     # +25%
     {"result": 25.0}, 0.001),

    ("average",
     {"numbers": "10, 20, 30, 40, 50"},
     {"mean": 30.0, "count": 5, "sum": 150.0}, 0.001),

    ("median",
     {"numbers": "1, 2, 3, 4, 5"},
     {"median": 3.0}, 0.001),

    ("median",
     {"numbers": "1, 2, 3, 4"},
     {"median": 2.5}, 0.001),  # even-count: average of middle two

    ("gcd",
     {"numbers": "48, 36"},
     {"gcd": 12}, 0),

    ("lcm",
     {"numbers": "4, 6"},
     {"lcm": 12}, 0),

    ("permutation",
     {"n": 5, "r": 2},
     # 5! / 3! = 20
     {"permutations": 20}, 0),

    ("combination",
     {"n": 5, "r": 2},
     # 5! / (2! 3!) = 10
     {"combinations": 10}, 0),

    ("quadratic",
     {"a": 1, "b": -3, "c": 2},
     # x²-3x+2 = (x-1)(x-2) → roots 1 and 2
     {"discriminant": 1, "root1": "2.0", "root2": "1.0",
      "nature": "Two distinct real roots"}, 0.001),

    ("linear-equation",
     {"a": 2, "b": -6},
     # 2x - 6 = 0 → x = 3
     {"x": 3.0}, 0.001),

    # --- Time & Motion / Physics ---
    ("speed",
     {"distance": 100, "time": 2},
     {"speed": 50.0}, 0.001),

    ("force",
     {"mass": 10, "acceleration": 9.8},
     {"force_newtons": 98.0}, 0.001),

    ("kinetic-energy",
     {"mass": 2, "velocity": 10},
     # 0.5 * 2 * 100 = 100 J
     {"kinetic_energy_joules": 100.0}, 0.001),

    ("ohms-law",
     {"voltage": 12, "current": 2},
     # R = V/I = 6
     {"voltage": 12.0, "current": 2.0, "resistance": 6.0}, 0.001),

    ("days-between-dates",
     {"start_date": "2024-01-01", "end_date": "2024-12-31"},
     {"days": 365}, 0),  # 2024 is leap year

    # --- Business ---
    ("conversion-rate",
     {"visitors": 10000, "conversions": 250},
     {"conversion_rate_percent": 2.5}, 0.001),

    ("markup",
     {"cost": 50, "selling_price": 75},
     # (75-50)/50 = 50%
     {"markup_percent": 50.0, "profit": 25.0}, 0.001),

    ("profit-margin",
     {"revenue": 100, "cost": 60},
     # (100-60)/100 = 40%
     {"gross_profit": 40.0, "margin_percent": 40.0}, 0.001),

    # --- Property (Bucket 2) ---
    ("rental-yield",
     {"property_price": 1000000, "weekly_rent": 500, "annual_expenses": 0},
     # 500*52 = 26000; 26000/1000000 = 2.6%
     {"annual_rent": 26000.0, "gross_yield_percent": 2.6, "net_yield_percent": 2.6}, 0.001),

    ("interest-rate-change-impact",
     {"loan_amount": 100000, "current_rate": 5, "new_rate": 6, "term_years": 10},
     # EMI(5%, 10y) ≈ 1060.66; EMI(6%, 10y) ≈ 1110.21; diff ≈ 49.55/mo
     {"current_emi": 1060.66, "new_emi": 1110.21}, 0.01),

    # --- Bucket 2 finance ---
    ("inflation-impact",
     {"amount_today": 100000, "inflation_rate": 3, "years": 10},
     # 100000 / 1.03^10 = 74409.39
     {"future_purchasing_power": 74409.39}, 0.01),

    ("salary-increase-impact",
     {"current_salary": 100000, "annual_raise_percent": 5, "inflation_rate": 3, "years": 10},
     # nominal: 100000 * 1.05^10 = 162889.46
     # real: 162889.46 / 1.03^10 = 121199.76
     {"future_nominal_salary": 162889.46, "future_real_salary": 121199.76}, 0.01),

    # --- Bucket 2 business ---
    ("revenue-impact",
     {"current_price": 100, "current_volume": 1000, "price_change_percent": 10, "volume_change_percent": 0},
     # 110*1000 = 110000, change +10000 (+10%)
     {"current_revenue": 100000.0, "new_revenue": 110000.0,
      "revenue_change": 10000.0, "revenue_change_percent": 10.0}, 0.001),

    ("price-change-impact",
     {"current_price": 100, "current_volume": 1000, "unit_cost": 50,
      "price_change_percent": 10, "elasticity": 1.0},
     # +10% price, elasticity=-1 (unit elastic) → volume -10% to 900
     # new revenue 110*900 = 99000 (slight drop from 100000 - unit elastic on revenue)
     # current profit (100-50)*1000 = 50000
     # new profit (110-50)*900 = 54000 → +8%
     {"new_volume": 900.0, "new_revenue": 99000.0, "new_profit": 54000.0}, 0.001),

    # --- Bucket 2 SaaS ---
    ("ltv-growth-simulator",
     {"current_arpu": 100, "current_churn_percent": 5, "gross_margin_percent": 100,
      "new_arpu": 100, "new_churn_percent": 2.5},
     # current LTV = 100 / 0.05 = 2000
     # new LTV = 100 / 0.025 = 4000 → +100%
     {"current_ltv": 2000.0, "new_ltv": 4000.0, "ltv_increase_percent": 100.0}, 0.001),

    # --- Bucket 2 sports ---
    ("cricket-strike-rate",
     {"runs": 100, "balls_faced": 50, "format": "t20"},
     # SR = 100/50 * 100 = 200 → Elite
     {"strike_rate": 200.0}, 0.001),

    # --- Bucket 3 geometry — 2D ---
    ("area-square",
     {"side": 5},
     # A=25, P=20, d=5√2 ≈ 7.0711
     {"area": 25.0, "perimeter": 20.0, "diagonal": 7.0710678}, 0.0001),

    ("area-rectangle",
     {"length": 4, "width": 3},
     # 3-4-5 right triangle diagonal
     {"area": 12.0, "perimeter": 14.0, "diagonal": 5.0}, 0.0001),

    ("area-triangle",
     {"method": "base_height", "base": 10, "height": 6},
     {"area": 30.0}, 0.0001),

    ("area-triangle",
     {"method": "three_sides", "base": 3, "side_b": 4, "side_c": 5},
     # 3-4-5 right triangle, area = 6, perimeter = 12
     {"area": 6.0, "perimeter": 12.0}, 0.0001),

    ("area-circle",
     {"known_value": "radius", "value": 1},
     # A=π, C=2π, d=2
     {"area": 3.14159265, "circumference": 6.28318531, "diameter": 2.0, "radius": 1.0}, 0.0001),

    ("area-circle",
     {"known_value": "area", "value": 12.566370614},
     # A = 4π → r = 2
     {"radius": 2.0}, 0.0001),

    ("area-rhombus",
     {"diagonal_1": 6, "diagonal_2": 8},
     # A = 0.5*6*8 = 24, side = √(9+16) = 5, P = 20
     {"area": 24.0, "side_length": 5.0, "perimeter": 20.0}, 0.0001),

    ("regular-polygon",
     {"num_sides": 4, "side_length": 5},
     # Square: area = 25, perimeter = 20, interior angle = 90°
     {"area": 25.0, "perimeter": 20.0, "interior_angle_degrees": 90.0}, 0.0001),

    # --- Bucket 3 geometry — 3D ---
    ("volume-cube",
     {"side": 3},
     # V=27, SA=54, d=3√3 ≈ 5.196
     {"volume": 27.0, "surface_area": 54.0, "space_diagonal": 5.196152}, 0.0001),

    ("volume-cuboid",
     {"length": 2, "width": 3, "height": 4},
     # V=24, SA=2(6+8+12)=52, d=√(4+9+16)=√29 ≈ 5.385
     {"volume": 24.0, "surface_area": 52.0, "space_diagonal": 5.385165}, 0.0001),

    ("volume-sphere",
     {"known_value": "radius", "value": 1},
     # V = 4π/3, SA = 4π
     {"volume": 4.188790, "surface_area": 12.566371, "diameter": 2.0}, 0.0001),

    ("volume-cylinder",
     {"radius": 2, "height": 5},
     # V = π·4·5 = 20π ≈ 62.832
     {"volume": 62.831853}, 0.0001),

    ("volume-cone",
     {"radius": 3, "height": 4},
     # V = (1/3)·π·9·4 = 12π ≈ 37.699;  slant = √(9+16) = 5
     {"volume": 37.699112, "slant_height": 5.0}, 0.0001),

    # --- Bucket 3 math — advanced ---
    ("pythagoras",
     {"solve_for": "c", "a": 3, "b": 4},
     # Classic 3-4-5
     {"result": 5.0}, 0.0001),

    ("pythagoras",
     {"solve_for": "a", "b": 4, "c": 5},
     {"result": 3.0}, 0.0001),

    ("distance-formula",
     {"x1": 0, "y1": 0, "x2": 3, "y2": 4},
     # 3-4-5 again
     {"distance": 5.0, "dx": 3.0, "dy": 4.0}, 0.0001),

    ("distance-formula-3d",
     {"x1": 0, "y1": 0, "z1": 0, "x2": 3, "y2": 4, "z2": 12},
     # 3-4-12-13 Pythagorean quadruple
     {"distance": 13.0}, 0.0001),

    ("midpoint",
     {"x1": 0, "y1": 0, "x2": 10, "y2": 20},
     {"midpoint_x": 5.0, "midpoint_y": 10.0}, 0.0001),

    ("slope",
     {"x1": 0, "y1": 0, "x2": 1, "y2": 1},
     # Slope = 1, y-intercept = 0, angle = 45°
     {"slope": 1.0, "y_intercept": 0.0, "angle_degrees": 45.0}, 0.0001),

    ("trigonometry",
     {"function": "sin", "unit": "degrees", "value": 30},
     # sin(30°) = 0.5
     {"result": 0.5}, 0.0001),

    ("trigonometry",
     {"function": "cos", "unit": "degrees", "value": 60},
     # cos(60°) = 0.5
     {"result": 0.5}, 0.0001),

    ("logarithm",
     {"value": 1000, "base": "10"},
     # log10(1000) = 3
     {"result": 3.0}, 0.0001),

    ("logarithm",
     {"value": 8, "base": "2"},
     # log2(8) = 3
     {"result": 3.0}, 0.0001),

    ("exponential",
     {"base_choice": "10", "exponent": 3},
     # 10^3 = 1000
     {"result": 1000.0}, 0.0001),

    ("exponential",
     {"base_choice": "e", "exponent": 0},
     # e^0 = 1
     {"result": 1.0}, 0.0001),

    # --- Bucket 3 physics ---
    ("weight",
     {"mass": 10, "location": "earth"},
     # 10 × 9.80665 ≈ 98.07 N
     {"weight_newtons": 98.0665, "gravity_used": 9.80665}, 0.001),

    ("momentum",
     {"mass": 10, "velocity": 5},
     # p = 50
     {"momentum": 50.0}, 0.0001),

    ("impulse",
     {"force": 100, "time": 2},
     # J = 200
     {"impulse": 200.0, "change_in_momentum": 200.0}, 0.0001),

    ("escape-velocity",
     {"body": "earth"},
     # Earth: ~11186 m/s
     {"escape_velocity_kmps": 11.186}, 0.01),

    ("pendulum-period",
     {"length": 1, "gravity": 9.81},
     # T = 2π·√(1/9.81) ≈ 2.006 s
     {"period_seconds": 2.006409}, 0.001),

    ("simple-harmonic-motion",
     {"mass": 1, "spring_constant": 1},
     # ω = 1, T = 2π
     {"angular_frequency_rad_per_s": 1.0, "period_seconds": 6.283185}, 0.0001),

    ("projectile-motion",
     {"initial_velocity": 10, "angle_degrees": 45, "gravity": 10},
     # Easy numbers: R = 100·sin(90°)/10 = 10; H = 100·0.5/20 = 2.5; T = 20·sin(45°)/10 ≈ 1.414
     {"range_m": 10.0, "max_height_m": 2.5}, 0.001),

    # --- Bucket 3 engineering ---
    ("concrete-volume",
     {"shape": "slab", "length": 10, "width": 5, "depth_or_height": 0.2, "wastage_percent": 0},
     # 10 m³ exactly, no wastage
     {"volume_m3": 10.0, "volume_with_wastage_m3": 10.0}, 0.0001),
]


# =============================================================================
# ERROR CASES — invalid inputs MUST raise ValueError.
# =============================================================================
ERROR_CASES = [
    # Missing required inputs
    ("simple-interest", {"principal": 1000, "rate": 5}),   # missing time
    ("bmi", {"weight_kg": 70}),                             # missing height
    ("quadratic", {"a": 1, "b": 2}),                        # missing c
    # Invalid types
    ("simple-interest", {"principal": "abc", "rate": 5, "time": 3}),
    ("loan-emi", {"principal": 100000, "annual_rate": 5, "tenure_months": "ten"}),
    # Negative where positive required
    ("bmi", {"weight_kg": -70, "height_cm": 175}),
    ("loan-emi", {"principal": 100000, "annual_rate": 5, "tenure_months": -12}),
    ("cagr", {"start_value": 0, "end_value": 100, "years": 5}),
    # Discount > 100%
    ("discount", {"original_price": 100, "discount_percent": 150}),
    # Deposit > price
    ("mortgage", {"home_price": 100000, "down_payment": 200000, "annual_rate": 6, "term_years": 30}),
    # Divide by zero in linear equation
    ("linear-equation", {"a": 0, "b": 5}),
    # Conversions > visitors
    ("conversion-rate", {"visitors": 100, "conversions": 200}),
    # Stress test: price = variable cost (no contribution margin)
    ("break-even", {"fixed_costs": 1000, "price_per_unit": 50, "variable_cost_per_unit": 50}),
    # Bad time format
    ("work-hours", {"start_time": "9am", "end_time": "5pm"}),
    # Empty number list
    ("average", {"numbers": ""}),
    # Ohms law with < 2 values
    ("ohms-law", {"voltage": 12}),
    # Bad timezone
    ("time-zone", {"datetime_local": "2025-01-01T10:00", "from_zone": "Made/Up", "to_zone": "UTC"}),
]


# =============================================================================
# HAPPY-PATH SAMPLES — same as smoke_test, but every calc must produce a dict
# with all output keys declared in META.
# =============================================================================
from tests.smoke_test import SAMPLES


# =============================================================================
# TESTS
# =============================================================================

def test_registry_is_consistent():
    """Every module in ALL_MODULES has a META.slug present in REGISTRY."""
    for mod in registry.ALL_MODULES:
        assert "slug" in mod.META, f"{mod.__name__} missing META.slug"
        assert mod.META["slug"] in registry.REGISTRY, f"{mod.META['slug']} not in REGISTRY"


def test_every_calculator_has_a_sample():
    """Every registered calculator has a sample in the test suite (smoke_test.SAMPLES)."""
    missing = set(registry.REGISTRY) - set(SAMPLES)
    assert not missing, f"Calculators without sample inputs: {missing}"


def test_every_calculator_has_required_meta():
    """Every calculator's META has the keys the templates depend on."""
    required = {"slug", "name", "category", "description", "formula", "fields", "outputs", "faq"}
    for slug, mod in registry.REGISTRY.items():
        missing = required - set(mod.META.keys())
        assert not missing, f"{slug} META missing: {missing}"
        assert isinstance(mod.META["fields"], list), f"{slug}: fields must be a list"
        assert isinstance(mod.META["outputs"], list), f"{slug}: outputs must be a list"
        # Each field has a name + type + label
        for f in mod.META["fields"]:
            assert "name" in f and "label" in f and "type" in f, f"{slug}: field missing name/label/type"
        # Each output has a key + label
        for o in mod.META["outputs"]:
            assert "key" in o and "label" in o, f"{slug}: output missing key/label"


# ---- Happy-path: every calculator runs with sample inputs ----
@pytest.mark.parametrize("slug", sorted(registry.REGISTRY.keys()))
def test_happy_path(slug):
    """Every calculator runs cleanly with its sample input and returns a dict."""
    mod = registry.get(slug)
    result = mod.calculate(SAMPLES[slug])
    assert isinstance(result, dict), f"{slug}: calculate() must return dict"
    assert len(result) > 0, f"{slug}: result was empty"


# ---- Reference values: hand-checked math ----
@pytest.mark.parametrize("slug,inputs,expected,tol", REFERENCE_CASES,
                         ids=[f"{c[0]}::{i}" for i, c in enumerate(REFERENCE_CASES)])
def test_reference_value(slug, inputs, expected, tol):
    """Reference-value verification: outputs match hand-computed expectations."""
    mod = registry.get(slug)
    result = mod.calculate(inputs)
    for key, exp_value in expected.items():
        assert key in result, f"{slug}: output '{key}' missing from result"
        actual = result[key]
        if isinstance(exp_value, str):
            assert actual == exp_value, f"{slug}.{key}: expected {exp_value!r}, got {actual!r}"
        elif exp_value == 0:
            assert abs(actual - exp_value) <= max(tol, 1e-6), f"{slug}.{key}: expected {exp_value}, got {actual}"
        else:
            rel_err = abs(actual - exp_value) / abs(exp_value)
            assert rel_err <= tol, (
                f"{slug}.{key}: expected {exp_value}, got {actual}, "
                f"relative error {rel_err:.6f} > tol {tol}"
            )


# ---- Error paths: invalid input MUST raise ValueError ----
@pytest.mark.parametrize("slug,bad_inputs", ERROR_CASES,
                         ids=[f"{c[0]}::err{i}" for i, c in enumerate(ERROR_CASES)])
def test_error_path(slug, bad_inputs):
    """Invalid inputs raise ValueError (which the API maps to HTTP 400)."""
    mod = registry.get(slug)
    with pytest.raises(ValueError):
        mod.calculate(bad_inputs)


# ---- Output shape: every declared output key actually appears in result ----
@pytest.mark.parametrize("slug", sorted(registry.REGISTRY.keys()))
def test_output_keys_match_meta(slug):
    """Every output key declared in META.outputs is present in calculate()'s result.

    (calculate() may also return EXTRA keys not in META — that's fine, the
    frontend has a catch-all; but it must include everything META promises.)
    """
    mod = registry.get(slug)
    result = mod.calculate(SAMPLES[slug])
    declared_keys = {o["key"] for o in mod.META["outputs"]}
    missing = declared_keys - set(result.keys())
    assert not missing, f"{slug}: META declares outputs {missing} that calculate() did not return"


# ---- Numerical stability spot checks ----
def test_bmi_extreme_inputs():
    """BMI handles edge weights without crashing."""
    from calculators import bmi
    # Very low / very high — should compute, not crash
    assert bmi.calculate({"weight_kg": 30, "height_cm": 150})["category"] == "Underweight"
    assert bmi.calculate({"weight_kg": 200, "height_cm": 150})["category"] == "Obese"


def test_loan_emi_zero_interest():
    """EMI calculator handles 0% interest correctly (no division by zero)."""
    from calculators import loan_emi
    # 0% interest, 12 months, 12000 principal → 1000/month
    r = loan_emi.calculate({"principal": 12000, "annual_rate": 0, "tenure_months": 12})
    assert abs(r["emi"] - 1000) < 0.01


def test_quadratic_complex_roots():
    """Quadratic returns complex roots when discriminant negative."""
    from calculators import quadratic
    # x²+1=0 → roots ±i
    r = quadratic.calculate({"a": 1, "b": 0, "c": 1})
    assert "complex" in r["nature"].lower()
    assert "i" in r["root1"].lower()


def test_mortgage_stress_test_assessments():
    """Stress test verdict transitions correctly."""
    from calculators import mortgage_stress_test
    # Small loan, high income → PASS
    r = mortgage_stress_test.calculate({
        "loan_amount": 100000, "current_rate": 5, "term_years": 30,
        "annual_income": 200000, "buffer_percent": 3,
    })
    assert "PASS" in r["assessment"]


def test_inflation_impact_zero_inflation():
    """Zero inflation = no purchasing power loss."""
    from calculators import inflation_impact
    r = inflation_impact.calculate({"amount_today": 100000, "inflation_rate": 0, "years": 10})
    assert r["loss_of_purchasing_power"] == 0
    assert r["future_purchasing_power"] == 100000


def test_price_change_impact_elasticity_sign_invariant():
    """Calculator accepts elasticity as both 1.5 and -1.5, same answer."""
    from calculators import price_change_impact
    inputs_pos = {"current_price": 100, "current_volume": 1000, "unit_cost": 40,
                  "price_change_percent": 10, "elasticity": 1.5}
    inputs_neg = {**inputs_pos, "elasticity": -1.5}
    r_pos = price_change_impact.calculate(inputs_pos)
    r_neg = price_change_impact.calculate(inputs_neg)
    assert r_pos["new_volume"] == r_neg["new_volume"]
    # +10% price + |1.5| elasticity → -15% volume → 850
    assert abs(r_pos["new_volume"] - 850) < 0.01


def test_football_wp_swing_directional():
    """Scoring lifts WP; conceding drops it."""
    from calculators import football_goal_win_probability
    scored = football_goal_win_probability.calculate({
        "goals_for": 1, "goals_against": 1, "current_minute": 70, "scoring_team": "us"})
    conceded = football_goal_win_probability.calculate({
        "goals_for": 1, "goals_against": 1, "current_minute": 70, "scoring_team": "them"})
    assert scored["swing_percent"] > 0
    assert conceded["swing_percent"] < 0

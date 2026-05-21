"""Smoke test — verify every calculator imports and executes with sample inputs.

Run from /backend with:  python tests/smoke_test.py
"""
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import registry

# Sample inputs per calculator — exercises each calculate() function.
SAMPLES = {
    # Finance
    "simple-interest":     {"principal": 10000, "rate": 5, "time": 3},
    "compound-interest":   {"principal": 10000, "rate": 8, "time": 5, "compounds_per_year": 12},
    "loan-emi":            {"principal": 500000, "annual_rate": 8.5, "tenure_months": 240},
    "mortgage":            {"home_price": 750000, "down_payment": 150000, "annual_rate": 6.25, "term_years": 30},
    "roi":                 {"initial_investment": 10000, "final_value": 13500},
    "cagr":                {"start_value": 10000, "end_value": 16500, "years": 5},
    "break-even":          {"fixed_costs": 50000, "price_per_unit": 100, "variable_cost_per_unit": 40},
    "profit-margin":       {"revenue": 100000, "cost": 60000},
    "discount":            {"original_price": 200, "discount_percent": 25},
    "future-value":        {"present_value": 10000, "annual_rate": 7, "years": 10},
    "investment-growth":   {"initial_amount": 10000, "monthly_contribution": 500, "annual_rate": 8, "years": 20},
    "dividend":            {"annual_dividend_per_share": 2.5, "share_price": 50, "shares_held": 100},
    "sip":                 {"monthly_investment": 5000, "annual_rate": 12, "years": 15},
    "amortization":        {"principal": 300000, "annual_rate": 6.5, "term_years": 30},
    "interest-rate":       {"present_value": 10000, "future_value": 15000, "years": 5},
    # Health
    "bmi":                 {"weight_kg": 70, "height_cm": 175},
    "bmr":                 {"weight_kg": 70, "height_cm": 175, "age": 30, "sex": "male"},
    "tdee":                {"weight_kg": 70, "height_cm": 175, "age": 30, "sex": "male", "activity": "moderate"},
    "body-fat":            {"sex": "male", "height_cm": 175, "neck_cm": 38, "waist_cm": 85},
    "calorie":             {"weight_kg": 70, "height_cm": 175, "age": 30, "sex": "male", "activity": "moderate", "goal": "lose"},
    "ideal-weight":        {"height_cm": 175, "sex": "male"},
    "water-intake":        {"weight_kg": 70, "exercise_minutes": 30},
    "heart-rate-zone":     {"age": 30},
    # Math
    "percentage":          {"mode": "of", "x": 20, "y": 150},
    "fraction":            {"a": 1, "b": 2, "op": "+", "c": 1, "d": 3},
    "ratio":               {"a": 12, "b": 18, "c": 30},
    "average":             {"numbers": "5, 10, 15, 20, 25"},
    "median":              {"numbers": "3, 1, 4, 1, 5, 9, 2, 6"},
    "mode":                {"numbers": "1, 2, 2, 3, 3, 3, 4"},
    "standard-deviation":  {"numbers": "2, 4, 4, 4, 5, 5, 7, 9"},
    "variance":            {"numbers": "2, 4, 4, 4, 5, 5, 7, 9"},
    "probability":         {"favorable": 1, "total": 6},
    "permutation":         {"n": 10, "r": 3},
    "combination":         {"n": 10, "r": 3},
    "lcm":                 {"numbers": "12, 18, 24"},
    "gcd":                 {"numbers": "48, 36, 24"},
    "quadratic":           {"a": 1, "b": -3, "c": 2},
    "linear-equation":     {"a": 2, "b": -6},
    # Time & Motion
    "speed":               {"distance": 150, "time": 2.5},
    "distance":            {"speed": 60, "time": 3},
    "time":                {"distance": 200, "speed": 80},
    "acceleration":        {"initial_velocity": 0, "final_velocity": 27, "time": 10},
    "work-hours":          {"start_time": "09:00", "end_time": "17:30", "break_minutes": 30},
    "days-between-dates":  {"start_date": "2024-01-01", "end_date": "2025-06-15"},
    "time-zone":           {"datetime_local": "2025-06-15T10:00", "from_zone": "UTC", "to_zone": "Australia/Sydney"},
    # Physics
    "force":               {"mass": 10, "acceleration": 9.8},
    "kinetic-energy":      {"mass": 1500, "velocity": 20},
    "potential-energy":    {"mass": 10, "height": 20},
    "work-done":           {"force": 50, "distance": 10, "angle_degrees": 0},
    "density":             {"mass": 1000, "volume": 1},
    "pressure":            {"force": 100, "area": 2},
    "power-electrical":    {"voltage": 230, "current": 5},
    "ohms-law":            {"voltage": 230, "current": 5},
    # Business
    "conversion-rate":     {"visitors": 10000, "conversions": 250},
    "markup":              {"cost": 50, "selling_price": 75},
    "commission":          {"sales": 100000, "rate": 5},
    "revenue":             {"price": 29.99, "quantity": 500},
    # Property (Bucket 2)
    "rental-yield":        {"property_price": 750000, "weekly_rent": 650, "annual_expenses": 8000},
    "buy-vs-rent":         {"property_price": 750000, "deposit": 150000, "mortgage_rate": 6.25, "term_years": 30,
                            "buying_costs_percent": 5, "ongoing_costs_percent": 1.5, "capital_growth_percent": 4,
                            "weekly_rent": 650, "rent_growth_percent": 3, "investment_return_percent": 7, "years": 10},
    "property-roi-advanced": {"property_price": 750000, "deposit": 150000, "mortgage_rate": 6.25,
                              "loan_term_years": 30, "weekly_rent": 650, "annual_expenses": 8000,
                              "buying_costs_percent": 5, "capital_growth_percent": 4, "holding_years": 10},
    "mortgage-stress-test": {"loan_amount": 600000, "current_rate": 6.25, "term_years": 30,
                             "buffer_percent": 3, "annual_income": 150000, "other_monthly_debts": 500},
    "cashflow-simulation": {"property_price": 750000, "deposit": 150000, "mortgage_rate": 6.25,
                            "loan_term_years": 30, "weekly_rent": 650, "annual_expenses": 8000,
                            "rent_growth_percent": 3, "expense_growth_percent": 2.5,
                            "capital_growth_percent": 4, "simulation_years": 10},
    # Finance impact (Bucket 2)
    "inflation-impact":    {"amount_today": 100000, "inflation_rate": 3, "years": 10},
    "salary-increase-impact": {"current_salary": 100000, "annual_raise_percent": 5, "inflation_rate": 3, "years": 10},
    "interest-rate-change-impact": {"loan_amount": 500000, "current_rate": 6.25, "new_rate": 7, "term_years": 25},
    # Business impact + SaaS (Bucket 2)
    "revenue-impact":      {"current_price": 100, "current_volume": 1000, "price_change_percent": 5, "volume_change_percent": -2},
    "price-change-impact": {"current_price": 100, "current_volume": 1000, "unit_cost": 40,
                            "price_change_percent": 10, "elasticity": -1.5},
    "marketing-spend-impact": {"additional_spend": 50000, "expected_roas": 4, "gross_margin_percent": 60},
    "cac-impact":          {"current_cac": 500, "new_cac": 350, "arpu_monthly": 100,
                            "gross_margin_percent": 80, "monthly_churn_percent": 3, "new_customers_per_month": 100},
    "ltv-growth-simulator": {"current_arpu": 100, "current_churn_percent": 3, "gross_margin_percent": 80,
                             "new_arpu": 120, "new_churn_percent": 2},
    # Sports (Bucket 2)
    "cricket-strike-rate": {"runs": 75, "balls_faced": 50, "format": "t20", "target_strike_rate": 150},
    "football-goal-win-probability": {"goals_for": 1, "goals_against": 1, "current_minute": 70, "scoring_team": "us"},
    # Geometry — 2D (Bucket 3)
    "area-square":         {"side": 5},
    "area-rectangle":      {"length": 8, "width": 5},
    "area-triangle":       {"method": "base_height", "base": 10, "height": 6},
    "area-circle":         {"known_value": "radius", "value": 5},
    "area-parallelogram":  {"base": 8, "height": 5, "side": 6},
    "area-trapezoid":      {"base_a": 10, "base_b": 6, "height": 4, "side_c": 5, "side_d": 5},
    "area-rhombus":        {"diagonal_1": 12, "diagonal_2": 8},
    "area-ellipse":        {"semi_major": 5, "semi_minor": 3},
    "regular-polygon":     {"num_sides": 6, "side_length": 5},
    # Geometry — 3D (Bucket 3)
    "volume-cube":         {"side": 5},
    "volume-cuboid":       {"length": 10, "width": 6, "height": 4},
    "volume-sphere":       {"known_value": "radius", "value": 5},
    "volume-cylinder":     {"radius": 3, "height": 10},
    "volume-cone":         {"radius": 3, "height": 8},
    "volume-pyramid":      {"base_side": 6, "height": 8},
    "volume-torus":        {"major_radius": 5, "minor_radius": 2},
    # Math — advanced (Bucket 3)
    "pythagoras":          {"solve_for": "c", "a": 3, "b": 4},
    "distance-formula":    {"x1": 1, "y1": 2, "x2": 4, "y2": 6},
    "distance-formula-3d": {"x1": 0, "y1": 0, "z1": 0, "x2": 3, "y2": 4, "z2": 12},
    "midpoint":            {"x1": 2, "y1": 3, "x2": 8, "y2": 11},
    "slope":               {"x1": 1, "y1": 2, "x2": 4, "y2": 11},
    "trigonometry":        {"function": "sin", "unit": "degrees", "value": 30},
    "logarithm":           {"value": 100, "base": "10"},
    "exponential":         {"base_choice": "e", "exponent": 1},
    # Physics — advanced (Bucket 3)
    "weight":              {"mass": 70, "location": "earth"},
    "momentum":            {"mass": 1500, "velocity": 20},
    "impulse":             {"force": 500, "time": 0.1},
    "universal-gravitation": {"mass_1": 5.972e24, "mass_2": 7.342e22, "distance": 384400000},
    "escape-velocity":     {"body": "earth"},
    "orbital-period":      {"central_body": "earth", "semi_major_axis": 6.778e6},
    "projectile-motion":   {"initial_velocity": 30, "angle_degrees": 45},
    "pendulum-period":     {"length": 1},
    "simple-harmonic-motion": {"mass": 0.5, "spring_constant": 50},
    # Engineering (Bucket 3)
    "concrete-volume":     {"shape": "slab", "length": 10, "width": 5, "depth_or_height": 0.15, "wastage_percent": 10},
    "beam-deflection-simple": {"load_n": 5000, "length_m": 4, "elastic_modulus_pa": 200e9, "moment_of_inertia_m4": 8.33e-6},
    "brick-quantity":      {"wall_length_m": 10, "wall_height_m": 2.5, "brick_length_mm": 230, "brick_height_mm": 76, "mortar_thickness_mm": 10, "wastage_percent": 5},
}


def main() -> int:
    passed, failed = 0, 0
    missing = []
    for slug in registry.REGISTRY:
        if slug not in SAMPLES:
            missing.append(slug)
            continue
        try:
            result = registry.get(slug).calculate(SAMPLES[slug])
            assert isinstance(result, dict), "calculate() must return a dict"
            passed += 1
        except Exception as e:
            failed += 1
            print(f"FAIL  {slug}: {e}")
            traceback.print_exc()
    print(f"\nSmoke test: {passed} passed, {failed} failed, {len(missing)} without samples")
    if missing:
        print("No sample for:", missing)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

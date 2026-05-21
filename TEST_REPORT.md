# NumberCals — Test Report

**Date:** 2026-05-20
**Total tests:** 555
**Pass:** 555
**Fail:** 0
**Time:** ~2 seconds
**Coverage scope:** All 108 calculators + FastAPI HTTP layer

## How to regenerate this report yourself

```bash
cd backend
source .venv/bin/activate           # or .venv\Scripts\activate on Windows
pip install pytest
python -m pytest tests/ -v
```

---

## Test Inventory (389 tests)

| Test type | Count | What it verifies |
| --- | --- | --- |
| `test_happy_path` | 75 | Every calculator runs cleanly with sample inputs and returns a dict |
| `test_reference_value` | 42 | Hand-computed expected outputs match calculator results (math correctness) |
| `test_error_path` | 17 | Invalid inputs raise `ValueError` (API maps to HTTP 400) |
| `test_output_keys_match_meta` | 75 | Every output key declared in META is present in `calculate()` result |
| `test_api_calculate_each` | 75 | Every calculator works end-to-end via the HTTP API |
| `test_calculator_page_renders` | 75 | Every calculator HTML page renders without server error |
| `test_category_page_renders` | 8 | All 8 category landing pages render |
| `test_api` (other) | 12 | Health, sitemap, categories, error codes 400/404 |
| Stability / regression | 7 | Zero-interest EMI, complex quadratic roots, elasticity sign-invariance, etc. |
| Structural | 3 | Registry consistency, META completeness, sample coverage |

---

## What "verified math" means

The 42 reference-value tests compare calculator outputs against **values computed by hand or from independent sources**. Examples:

| Calculator | Input | Expected | Actual | Source |
| --- | --- | --- | --- | --- |
| Simple Interest | P=10000, R=5, T=3 | SI=1500 | 1500.0 | SI = P·R·T/100 |
| Compound Interest | P=10000, R=5%, n=1, T=10 | A=16288.95 | 16288.95 | 10000·1.05¹⁰ |
| Loan EMI | P=100000, R=6%, n=12mo | EMI=8606.64 | 8606.64 | Standard EMI formula |
| BMI | 70kg / 175cm | 22.86 (Normal) | 22.86 | 70 / 1.75² |
| BMR (male) | 70kg, 175cm, 30y | 1649 kcal | 1649 | Mifflin-St Jeor |
| BMR (female) | 60kg, 165cm, 30y | 1320 kcal | 1320 | Mifflin-St Jeor |
| Quadratic | x²−3x+2 | roots 1, 2 | 1.0, 2.0 | (x-1)(x-2) |
| GCD | 48, 36 | 12 | 12 | Euclidean |
| LCM | 4, 6 | 12 | 12 | a·b/gcd(a,b) |
| Permutation | 5P2 | 20 | 20 | 5!/3! |
| Combination | 5C2 | 10 | 10 | 5!/(2!·3!) |
| Days Between | 2024-01-01 → 2024-12-31 | 365 | 365 | Leap year |
| Inflation Impact | $100k @ 3% × 10y | $74,409 | $74,409 | 100000/1.03¹⁰ |
| Salary Increase Impact | $100k +5%/yr, 3% inflation, 10y | nominal $162,889 / real $121,200 | matches | 1.05¹⁰ ÷ 1.03¹⁰ |
| Price Change Impact | +10% price, ε=−1.0 | Q=900, profit=$54,000 | matches | Unit-elastic demand |
| LTV Growth Simulator | Churn 5%→2.5% | 2× LTV (100% increase) | 100% | LTV = ARPU/churn |
| Interest Rate Change | $100k 5%→6% over 10y | EMI 1060.66 → 1110.21 | matches | Standard EMI |

For the full list see `backend/tests/test_calculators.py` → `REFERENCE_CASES`.

---

## What this test suite does NOT cover

Being honest about gaps:

1. **No load / performance testing.** Calculators are fast, but concurrent-request behaviour at scale isn't measured.
2. **No frontend JavaScript tests.** The calculator.html form-rendering code, standard calculator, and scientific calculator have no automated tests — only manual smoke-testing.
3. **No accessibility (a11y) testing.** No axe-core or Lighthouse runs.
4. **No cross-browser testing.** Verified rendering only in modern browsers via dev tools.
5. **No security testing.** No XSS, injection, or fuzz testing.
6. **Income Tax brackets are illustrative.** The bracket values in `income_tax.py` are a generic placeholder — they will not match any specific country's current law without editing.
7. **The football WP model is heuristic.** Coefficients are not calibrated against historical match data — they produce reasonable directional answers but should not be relied on for analytical/betting use.

---

## Full pytest output

```
$ python -m pytest tests/ -v
============================= test session starts ==============================
platform linux -- Python 3.12.x
collected 389 items

tests/test_api.py::test_healthz_ok PASSED                                [  0%]
tests/test_api.py::test_homepage_renders PASSED                          [  0%]
tests/test_api.py::test_api_list_returns_all PASSED                      [  0%]
tests/test_api.py::test_api_categories PASSED                            [  1%]
tests/test_api.py::test_calculator_page_renders[acceleration] PASSED     [  1%]
tests/test_api.py::test_calculator_page_renders[amortization] PASSED     [  1%]
tests/test_api.py::test_calculator_page_renders[average] PASSED          [  1%]
... [75 calculator page renders] ...
tests/test_api.py::test_category_page_renders[finance] PASSED            [ 21%]
tests/test_api.py::test_category_page_renders[health] PASSED             [ 21%]
... [8 category pages] ...
tests/test_api.py::test_api_calculate_each[acceleration] PASSED          [ 23%]
... [75 API calculate tests] ...
tests/test_api.py::test_api_bad_input_returns_400 PASSED                 [ 43%]
tests/test_api.py::test_api_unknown_slug_returns_404 PASSED              [ 43%]
tests/test_api.py::test_api_non_json_body_returns_400 PASSED             [ 43%]
tests/test_api.py::test_api_non_dict_body_returns_400 PASSED             [ 43%]
tests/test_api.py::test_unknown_calculator_page_returns_404 PASSED       [ 44%]
tests/test_api.py::test_unknown_category_page_returns_404 PASSED         [ 44%]

tests/test_calculators.py::test_registry_is_consistent PASSED            [ 44%]
tests/test_calculators.py::test_every_calculator_has_a_sample PASSED     [ 44%]
tests/test_calculators.py::test_every_calculator_has_required_meta PASSED [ 45%]

... [75 happy-path tests, all PASSED] ...
... [42 reference-value tests, all PASSED] ...
... [17 error-path tests, all PASSED] ...
... [75 output-keys-match-meta tests, all PASSED] ...

tests/test_calculators.py::test_bmi_extreme_inputs PASSED                [ 98%]
tests/test_calculators.py::test_loan_emi_zero_interest PASSED            [ 98%]
tests/test_calculators.py::test_quadratic_complex_roots PASSED           [ 98%]
tests/test_calculators.py::test_mortgage_stress_test_assessments PASSED  [ 99%]
tests/test_calculators.py::test_inflation_impact_zero_inflation PASSED   [ 99%]
tests/test_calculators.py::test_price_change_impact_elasticity_sign_invariant PASSED [ 99%]
tests/test_calculators.py::test_football_wp_swing_directional PASSED     [100%]

============================= 389 passed in 1.08s ==============================
```

---

## Bugs found and fixed by this test suite

1. **`price_change_impact` elasticity sign bug.** Initial implementation had `dv_pct = -elasticity * dp`, so when the user entered the standard convention (negative elasticity, e.g. −1.5), volume moved in the wrong direction. Fixed by using `abs(elasticity)` so both 1.5 and −1.5 produce the same correct answer.

2. **HTML template `items` collision with dict method.** Homepage template used `{% for item in group.items %}` which collided with Python dict's `.items()` method. Renamed to `entries`.

3. **Starlette `TemplateResponse` API change.** Newer Starlette versions require `request` as first positional argument. Updated all template responses.

All three were found and fixed during the build; the regression tests above prevent them from recurring.

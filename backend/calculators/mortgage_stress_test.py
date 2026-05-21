"""Mortgage Stress Test Calculator.

Tests whether a borrower can still afford their loan if interest rates rise.
Used by APRA and most lenders to assess serviceability (typical buffer: +3%).

Reports:
  - Current EMI at current rate
  - Stressed EMI at current rate + buffer
  - DTI (debt-to-income ratio) before and after
  - Pass/Fail recommendation
"""
from typing import Any, Dict
from ._base import non_negative, positive, require, to_float, to_int

META = {
    "slug": "mortgage-stress-test",
    "name": "Mortgage Stress Test Calculator",
    "category": "property",
    "description": "Test loan affordability if interest rates rise. Standard APRA-style assessment.",
    "formula": "Stress EMI = EMI at (current rate + buffer)",
    "fields": [
        {"name": "loan_amount", "label": "Loan Amount", "type": "number", "min": 0, "required": True, "placeholder": "600000"},
        {"name": "current_rate", "label": "Current Interest Rate (%)", "type": "number", "min": 0, "required": True, "placeholder": "6.25"},
        {"name": "term_years", "label": "Loan Term (years)", "type": "number", "min": 1, "required": True, "placeholder": "30"},
        {"name": "buffer_percent", "label": "Stress Buffer (%, default 3)", "type": "number", "min": 0, "required": False, "placeholder": "3"},
        {"name": "annual_income", "label": "Annual Gross Household Income", "type": "number", "min": 0, "required": True, "placeholder": "150000"},
        {"name": "other_monthly_debts", "label": "Other Monthly Debt Payments", "type": "number", "min": 0, "required": False, "placeholder": "500"},
    ],
    "outputs": [
        {"key": "current_monthly_payment", "label": "Current Monthly Payment", "format": "currency"},
        {"key": "stressed_monthly_payment", "label": "Stressed Monthly Payment", "format": "currency"},
        {"key": "monthly_payment_increase", "label": "Increase per Month", "format": "currency"},
        {"key": "current_dti_percent", "label": "Current DTI (%)", "format": "percent"},
        {"key": "stressed_dti_percent", "label": "Stressed DTI (%)", "format": "percent"},
        {"key": "assessment", "label": "Assessment", "format": "text"},
    ],
    "faq": [
        {"q": "What DTI is considered safe?", "a": "Lenders typically consider DTI under 35–40% comfortable. Above 50% is high-risk. APRA-supervised banks must apply a +3% interest rate buffer to all serviceability assessments."},
        {"q": "Why test at +3%?", "a": "It's the buffer mandated by APRA in Australia (raised from 2.5% in 2021). It protects borrowers and the financial system from rate-rise shocks."},
    ],
}


def _emi(principal, rate, years):
    n = years * 12
    r = (rate / 100) / 12
    if r == 0: return principal / n if n else 0
    return principal * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)


def calculate(inputs):
    loan, current_rate, income = require(inputs, "loan_amount", "current_rate", "annual_income")
    term = to_int(inputs.get("term_years"), "term_years")
    buffer = to_float(inputs["buffer_percent"] if inputs.get("buffer_percent") not in (None, "") else 3, "buffer_percent")
    other_debt = to_float(inputs["other_monthly_debts"] if inputs.get("other_monthly_debts") not in (None, "") else 0, "other_monthly_debts")

    non_negative(loan, "loan_amount"); non_negative(current_rate, "current_rate")
    positive(term, "term_years"); positive(income, "annual_income")

    current_pay = _emi(loan, current_rate, term)
    stressed_pay = _emi(loan, current_rate + buffer, term)
    monthly_income = income / 12

    current_dti = ((current_pay + other_debt) / monthly_income) * 100
    stressed_dti = ((stressed_pay + other_debt) / monthly_income) * 100

    if stressed_dti < 35:
        assess = "PASS — Comfortable serviceability even under stress."
    elif stressed_dti < 45:
        assess = "MARGINAL — Serviceability is tight under stress; reduce loan or increase income."
    else:
        assess = "FAIL — Loan would likely be unaffordable if rates rise. Reduce loan size."

    return {
        "current_monthly_payment": round(current_pay, 2),
        "stressed_monthly_payment": round(stressed_pay, 2),
        "monthly_payment_increase": round(stressed_pay - current_pay, 2),
        "current_dti_percent": round(current_dti, 2),
        "stressed_dti_percent": round(stressed_dti, 2),
        "assessment": assess,
    }

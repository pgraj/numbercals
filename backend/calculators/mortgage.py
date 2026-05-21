"""Mortgage Calculator.

Uses the standard amortizing-loan formula (same math as EMI), with home-loan
specific input labels. Optionally factors in property tax and home insurance
to give a total monthly housing payment.
"""
from typing import Any, Dict

from ._base import non_negative, positive, require, to_float, to_int

META = {
    "slug": "mortgage",
    "name": "Mortgage Calculator",
    "category": "finance",
    "description": "Calculate monthly mortgage payment, total interest, and optional total housing cost including tax and insurance.",
    "formula": "M = P · r(1+r)^n / [(1+r)^n − 1]",
    "fields": [
        {"name": "home_price", "label": "Home Price", "type": "number", "min": 0, "required": True, "placeholder": "750000"},
        {"name": "down_payment", "label": "Down Payment", "type": "number", "min": 0, "required": True, "placeholder": "150000"},
        {"name": "annual_rate", "label": "Annual Interest Rate (%)", "type": "number", "min": 0, "required": True, "placeholder": "6.25"},
        {"name": "term_years", "label": "Loan Term (years)", "type": "number", "min": 1, "required": True, "placeholder": "30"},
        {"name": "annual_property_tax", "label": "Annual Property Tax (optional)", "type": "number", "min": 0, "required": False, "placeholder": "0"},
        {"name": "annual_insurance", "label": "Annual Home Insurance (optional)", "type": "number", "min": 0, "required": False, "placeholder": "0"},
    ],
    "outputs": [
        {"key": "loan_amount", "label": "Loan Amount", "format": "currency"},
        {"key": "monthly_principal_interest", "label": "Monthly Payment (P&I)", "format": "currency"},
        {"key": "monthly_total", "label": "Total Monthly Housing Cost", "format": "currency"},
        {"key": "total_interest", "label": "Total Interest Over Term", "format": "currency"},
        {"key": "total_paid", "label": "Total Paid Over Term", "format": "currency"},
    ],
    "faq": [
        {"q": "What is PITI?", "a": "Principal, Interest, Tax, and Insurance — the four main components of a total monthly housing payment."},
        {"q": "Does a larger down payment reduce my monthly payment?", "a": "Yes — a larger down payment reduces the loan principal, lowering both monthly payment and total interest."},
    ],
}


def calculate(inputs: Dict[str, Any]) -> Dict[str, Any]:
    home_price, down, r_annual = require(inputs, "home_price", "down_payment", "annual_rate")
    term_years = to_int(inputs.get("term_years"), "term_years")
    tax = to_float(inputs["annual_property_tax"] if inputs.get("annual_property_tax") not in (None, "") else 0, "annual_property_tax")
    insurance = to_float(inputs["annual_insurance"] if inputs.get("annual_insurance") not in (None, "") else 0, "annual_insurance")

    non_negative(home_price, "home_price")
    non_negative(down, "down_payment")
    non_negative(r_annual, "annual_rate")
    positive(term_years, "term_years")
    non_negative(tax, "annual_property_tax")
    non_negative(insurance, "annual_insurance")

    if down > home_price:
        raise ValueError("'down_payment' cannot exceed 'home_price'.")

    loan = home_price - down
    n = term_years * 12
    r = (r_annual / 12) / 100

    if r == 0:
        pi = loan / n if n else 0
    else:
        pi = loan * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)

    monthly_tax = tax / 12
    monthly_insurance = insurance / 12
    monthly_total = pi + monthly_tax + monthly_insurance
    total_paid = pi * n
    total_interest = total_paid - loan

    return {
        "loan_amount": round(loan, 2),
        "monthly_principal_interest": round(pi, 2),
        "monthly_total": round(monthly_total, 2),
        "total_interest": round(total_interest, 2),
        "total_paid": round(total_paid, 2),
    }

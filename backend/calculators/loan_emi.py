"""Loan EMI Calculator.

Formula: EMI = [P × r × (1+r)^n] / [(1+r)^n − 1]
  P = principal loan amount
  r = monthly interest rate (annual_rate / 12 / 100)
  n = number of monthly installments
"""
from typing import Any, Dict

from ._base import non_negative, positive, require, to_int

META = {
    "slug": "loan-emi",
    "name": "Loan EMI Calculator",
    "category": "finance",
    "description": "Calculate the Equated Monthly Installment (EMI) for any loan.",
    "formula": "EMI = [P · r · (1+r)^n] / [(1+r)^n − 1]",
    "fields": [
        {"name": "principal", "label": "Loan Amount", "type": "number", "min": 0, "required": True, "placeholder": "500000"},
        {"name": "annual_rate", "label": "Annual Interest Rate (%)", "type": "number", "min": 0, "required": True, "placeholder": "8.5"},
        {"name": "tenure_months", "label": "Loan Tenure (months)", "type": "number", "min": 1, "required": True, "placeholder": "240"},
    ],
    "outputs": [
        {"key": "emi", "label": "Monthly EMI", "format": "currency"},
        {"key": "total_payment", "label": "Total Payment Over Tenure", "format": "currency"},
        {"key": "total_interest", "label": "Total Interest Payable", "format": "currency"},
    ],
    "faq": [
        {"q": "What is EMI?", "a": "Equated Monthly Installment — a fixed payment made every month covering both principal and interest."},
        {"q": "Does a longer tenure reduce EMI?", "a": "Yes — longer tenure lowers the monthly EMI but increases total interest paid over the life of the loan."},
    ],
}


def calculate(inputs: Dict[str, Any]) -> Dict[str, Any]:
    p, r_annual = require(inputs, "principal", "annual_rate")
    n = to_int(inputs.get("tenure_months"), "tenure_months")
    non_negative(p, "principal")
    non_negative(r_annual, "annual_rate")
    positive(n, "tenure_months")

    r = (r_annual / 12) / 100
    if r == 0:
        emi = p / n
    else:
        emi = p * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)

    total_payment = emi * n
    total_interest = total_payment - p
    return {
        "emi": round(emi, 2),
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_interest, 2),
    }

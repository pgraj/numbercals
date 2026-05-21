"""Property Cashflow Simulation Calculator.

Projects year-by-year cashflow for an investment property over N years,
showing rent, mortgage interest+principal split, expenses, net cashflow,
and equity build-up.
"""
from typing import Any, Dict, List
from ._base import non_negative, positive, require, to_float, to_int

META = {
    "slug": "cashflow-simulation",
    "name": "Property Cashflow Simulation",
    "category": "property",
    "description": "Project annual cashflow, mortgage paydown, and equity growth for an investment property over time.",
    "formula": "Annual cashflow = Rent − Expenses − Mortgage; Equity = Property Value − Loan Balance",
    "fields": [
        {"name": "property_price", "label": "Property Price", "type": "number", "min": 0, "required": True, "placeholder": "750000"},
        {"name": "deposit", "label": "Deposit", "type": "number", "min": 0, "required": True, "placeholder": "150000"},
        {"name": "mortgage_rate", "label": "Mortgage Rate (%)", "type": "number", "min": 0, "required": True, "placeholder": "6.25"},
        {"name": "loan_term_years", "label": "Loan Term (years)", "type": "number", "min": 1, "required": True, "placeholder": "30"},
        {"name": "weekly_rent", "label": "Weekly Rent (Year 1)", "type": "number", "min": 0, "required": True, "placeholder": "650"},
        {"name": "annual_expenses", "label": "Annual Expenses (Year 1)", "type": "number", "min": 0, "required": False, "placeholder": "8000"},
        {"name": "rent_growth_percent", "label": "Annual Rent Growth (%)", "type": "number", "min": 0, "required": False, "placeholder": "3"},
        {"name": "expense_growth_percent", "label": "Annual Expense Growth (%)", "type": "number", "min": 0, "required": False, "placeholder": "2.5"},
        {"name": "capital_growth_percent", "label": "Annual Capital Growth (%)", "type": "number", "required": False, "placeholder": "4"},
        {"name": "simulation_years", "label": "Years to Simulate", "type": "number", "min": 1, "required": True, "placeholder": "10"},
    ],
    "outputs": [
        {"key": "schedule", "label": "Year-by-Year Cashflow", "format": "table"},
        {"key": "total_cashflow", "label": "Cumulative Cashflow", "format": "currency"},
        {"key": "final_equity", "label": "Final Equity", "format": "currency"},
    ],
    "faq": [
        {"q": "What's the difference between cashflow and total return?", "a": "Cashflow is just the year's rent minus costs. Total return adds capital growth (which you don't realise until sale) and mortgage paydown (equity building)."},
    ],
}


def _emi(principal, rate, years):
    n = years * 12
    r = (rate / 100) / 12
    if r == 0: return principal / n if n else 0
    return principal * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)


def calculate(inputs):
    price, deposit, mrate, weekly = require(inputs, "property_price", "deposit", "mortgage_rate", "weekly_rent")
    loan_term = to_int(inputs.get("loan_term_years"), "loan_term_years")
    sim_years = to_int(inputs.get("simulation_years"), "simulation_years")
    expenses_y1 = to_float(inputs["annual_expenses"] if inputs.get("annual_expenses") not in (None, "") else 0, "annual_expenses")
    rent_growth = to_float(inputs["rent_growth_percent"] if inputs.get("rent_growth_percent") not in (None, "") else 3, "rent_growth_percent")
    exp_growth = to_float(inputs["expense_growth_percent"] if inputs.get("expense_growth_percent") not in (None, "") else 2.5, "expense_growth_percent")
    cap_growth = to_float(inputs["capital_growth_percent"] if inputs.get("capital_growth_percent") not in (None, "") else 4, "capital_growth_percent")

    positive(price, "property_price"); non_negative(deposit, "deposit"); positive(loan_term, "loan_term_years")
    if deposit > price: raise ValueError("Deposit cannot exceed property price.")

    loan = price - deposit
    monthly_pay = _emi(loan, mrate, loan_term)
    r = (mrate / 100) / 12

    schedule: List[Dict[str, Any]] = []
    balance = loan
    property_value = price
    annual_rent = weekly * 52
    annual_expenses = expenses_y1
    cum_cashflow = 0.0

    for year in range(1, sim_years + 1):
        # Build up the year's interest + principal paydown
        interest_paid = 0.0
        principal_paid = 0.0
        for _ in range(12):
            if balance <= 0: break
            interest_m = balance * r
            principal_m = monthly_pay - interest_m
            principal_m = min(principal_m, balance)
            interest_paid += interest_m
            principal_paid += principal_m
            balance -= principal_m

        mortgage_paid = interest_paid + principal_paid
        net_cf = annual_rent - annual_expenses - mortgage_paid
        cum_cashflow += net_cf
        property_value *= 1 + (cap_growth / 100)
        equity = property_value - balance

        schedule.append({
            "year": year,
            "rent": round(annual_rent, 0),
            "expenses": round(annual_expenses, 0),
            "mortgage": round(mortgage_paid, 0),
            "net_cashflow": round(net_cf, 0),
            "loan_balance": round(max(balance, 0), 0),
            "property_value": round(property_value, 0),
            "equity": round(equity, 0),
        })

        annual_rent *= 1 + (rent_growth / 100)
        annual_expenses *= 1 + (exp_growth / 100)

    return {
        "schedule": schedule,
        "total_cashflow": round(cum_cashflow, 2),
        "final_equity": round(property_value - max(balance, 0), 2),
    }

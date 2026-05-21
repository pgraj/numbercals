"""Property ROI Calculator (Advanced).

Calculates returns for an investment property over a holding period:
  - Annual cashflow (rent − all costs including mortgage)
  - Capital gain over the period
  - Cash-on-cash return (annual cashflow / cash invested)
  - Total ROI including capital gain

Cash invested = deposit + buying costs (stamp duty + legal)
"""
from typing import Any, Dict
from ._base import non_negative, positive, require, to_float, to_int

META = {
    "slug": "property-roi-advanced",
    "name": "Property ROI Calculator (Advanced)",
    "category": "property",
    "description": "Advanced investment property return analysis — cashflow, capital gain, cash-on-cash, total ROI.",
    "formula": "Total ROI = (Net Cashflow + Capital Gain) / Cash Invested × 100",
    "fields": [
        {"name": "property_price", "label": "Property Price", "type": "number", "min": 0, "required": True, "placeholder": "750000"},
        {"name": "deposit", "label": "Deposit", "type": "number", "min": 0, "required": True, "placeholder": "150000"},
        {"name": "mortgage_rate", "label": "Mortgage Rate (% p.a.)", "type": "number", "min": 0, "required": True, "placeholder": "6.25"},
        {"name": "loan_term_years", "label": "Loan Term (years)", "type": "number", "min": 1, "required": True, "placeholder": "30"},
        {"name": "weekly_rent", "label": "Weekly Rent", "type": "number", "min": 0, "required": True, "placeholder": "650"},
        {"name": "annual_expenses", "label": "Annual Expenses (excl. mortgage)", "type": "number", "min": 0, "required": False, "placeholder": "8000"},
        {"name": "buying_costs_percent", "label": "Buying Costs (% of price)", "type": "number", "min": 0, "required": False, "placeholder": "5"},
        {"name": "capital_growth_percent", "label": "Expected Capital Growth (% p.a.)", "type": "number", "required": False, "placeholder": "4"},
        {"name": "holding_years", "label": "Holding Period (years)", "type": "number", "min": 1, "required": True, "placeholder": "10"},
    ],
    "outputs": [
        {"key": "annual_rent", "label": "Annual Rent", "format": "currency"},
        {"key": "annual_mortgage_payment", "label": "Annual Mortgage Payment", "format": "currency"},
        {"key": "annual_cashflow", "label": "Annual Cashflow (Year 1)", "format": "currency"},
        {"key": "cash_invested", "label": "Total Cash Invested (Deposit + Buying Costs)", "format": "currency"},
        {"key": "cash_on_cash_percent", "label": "Cash-on-Cash Return (Year 1)", "format": "percent"},
        {"key": "capital_gain", "label": "Capital Gain Over Period", "format": "currency"},
        {"key": "total_return", "label": "Total Return (Cashflow + Capital Gain)", "format": "currency"},
        {"key": "total_roi_percent", "label": "Total ROI on Cash Invested (%)", "format": "percent"},
        {"key": "annualised_roi_percent", "label": "Annualised ROI (%)", "format": "percent"},
    ],
    "faq": [
        {"q": "What is cash-on-cash return?", "a": "Annual pre-tax cashflow divided by the actual cash you put in (deposit + buying costs). It ignores capital growth and measures only the income return on your real money."},
        {"q": "Why is the answer often negative?", "a": "Many investment properties are 'negatively geared' — annual rent doesn't cover mortgage + costs. Returns rely on capital growth. This calculator makes that trade-off visible."},
    ],
}


def _amortizing_payment(principal, rate_annual, years):
    n = years * 12
    r = (rate_annual / 100) / 12
    if r == 0: return principal / n if n else 0
    return principal * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)


def calculate(inputs):
    price, deposit, m_rate, weekly = require(inputs, "property_price", "deposit", "mortgage_rate", "weekly_rent")
    loan_term = to_int(inputs.get("loan_term_years"), "loan_term_years")
    hold_years = to_int(inputs.get("holding_years"), "holding_years")
    expenses = to_float(inputs["annual_expenses"] if inputs.get("annual_expenses") not in (None, "") else 0, "annual_expenses")
    buying_pct = to_float(inputs["buying_costs_percent"] if inputs.get("buying_costs_percent") not in (None, "") else 5, "buying_costs_percent")
    growth_pct = to_float(inputs["capital_growth_percent"] if inputs.get("capital_growth_percent") not in (None, "") else 4, "capital_growth_percent")

    positive(price, "property_price"); non_negative(deposit, "deposit"); non_negative(weekly, "weekly_rent")
    positive(loan_term, "loan_term_years"); positive(hold_years, "holding_years")
    if deposit > price: raise ValueError("Deposit cannot exceed property price.")

    loan = price - deposit
    annual_rent = weekly * 52
    monthly_pay = _amortizing_payment(loan, m_rate, loan_term)
    annual_mortgage = monthly_pay * 12
    annual_cashflow = annual_rent - expenses - annual_mortgage

    buying_costs = price * (buying_pct / 100)
    cash_invested = deposit + buying_costs

    end_value = price * ((1 + growth_pct / 100) ** hold_years)
    capital_gain = end_value - price

    # Sum cashflow over holding (Year 1 value held flat — simple, transparent)
    total_cashflow = annual_cashflow * hold_years
    total_return = total_cashflow + capital_gain
    total_roi = (total_return / cash_invested * 100) if cash_invested > 0 else 0
    cocc = (annual_cashflow / cash_invested * 100) if cash_invested > 0 else 0
    annualised = (((total_return + cash_invested) / cash_invested) ** (1 / hold_years) - 1) * 100 if cash_invested > 0 and (total_return + cash_invested) > 0 else 0

    return {
        "annual_rent": round(annual_rent, 2),
        "annual_mortgage_payment": round(annual_mortgage, 2),
        "annual_cashflow": round(annual_cashflow, 2),
        "cash_invested": round(cash_invested, 2),
        "cash_on_cash_percent": round(cocc, 2),
        "capital_gain": round(capital_gain, 2),
        "total_return": round(total_return, 2),
        "total_roi_percent": round(total_roi, 2),
        "annualised_roi_percent": round(annualised, 2),
    }

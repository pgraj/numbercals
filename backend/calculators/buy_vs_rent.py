"""Buy vs Rent Calculator.

Compares the total net cost of buying a property vs renting an equivalent
one over N years. Returns the better option and the dollar difference.

BUY side:
  - Mortgage interest cost over the period (approximated as a level annuity)
  - Buying costs (stamp duty, legal — flat %)
  - Ongoing costs (rates, insurance, maintenance — % of property value/year)
  - Less: property value growth (capital gain)

RENT side:
  - Rent payments over the period (with annual rent growth)
  - Less: investment growth of the down payment + buying costs invested
          at the alternative return rate (opportunity cost recovery)

This is the standard "rent-vs-buy" framework — assumptions matter. Tweak
the inputs to test sensitivity.
"""
from typing import Any, Dict

from ._base import non_negative, positive, require, to_float, to_int

META = {
    "slug": "buy-vs-rent",
    "name": "Buy vs Rent Calculator",
    "category": "property",
    "description": "Compare the total cost of buying vs renting the same property over a chosen time horizon.",
    "formula": "Net Buy Cost vs (Rent Cost − Investment Growth of Deposit)",
    "fields": [
        {"name": "property_price", "label": "Property Price", "type": "number", "min": 0, "required": True, "placeholder": "750000"},
        {"name": "deposit", "label": "Deposit (incl. buying costs you'd pay upfront)", "type": "number", "min": 0, "required": True, "placeholder": "150000"},
        {"name": "mortgage_rate", "label": "Mortgage Rate (% p.a.)", "type": "number", "min": 0, "required": True, "placeholder": "6.25"},
        {"name": "term_years", "label": "Loan Term (years)", "type": "number", "min": 1, "required": True, "placeholder": "30"},
        {"name": "buying_costs_percent", "label": "Buying Costs (% of price, stamp duty + legal)", "type": "number", "min": 0, "required": False, "placeholder": "5"},
        {"name": "ongoing_costs_percent", "label": "Ongoing Costs (% of price per year)", "type": "number", "min": 0, "required": False, "placeholder": "1.5"},
        {"name": "capital_growth_percent", "label": "Expected Capital Growth (% p.a.)", "type": "number", "required": False, "placeholder": "4"},
        {"name": "weekly_rent", "label": "Weekly Rent for Equivalent Property", "type": "number", "min": 0, "required": True, "placeholder": "650"},
        {"name": "rent_growth_percent", "label": "Annual Rent Growth (%)", "type": "number", "min": 0, "required": False, "placeholder": "3"},
        {"name": "investment_return_percent", "label": "Alternative Investment Return (% p.a.)", "type": "number", "required": False, "placeholder": "7"},
        {"name": "years", "label": "Comparison Horizon (years)", "type": "number", "min": 1, "required": True, "placeholder": "10"},
    ],
    "outputs": [
        {"key": "total_buy_cost", "label": "Net Cost — Buying", "format": "currency"},
        {"key": "total_rent_cost", "label": "Net Cost — Renting", "format": "currency"},
        {"key": "difference", "label": "Difference (rent − buy)", "format": "currency"},
        {"key": "winner", "label": "Better Option", "format": "text"},
        {"key": "breakeven_year", "label": "Approx Break-even Year", "format": "text"},
    ],
    "faq": [
        {"q": "Why doesn't this say 'always buy'?", "a": "Because owning costs money too — interest, rates, maintenance, opportunity cost on the deposit. Over short horizons (under ~5 years), renting often wins purely on cost. The crossover depends heavily on assumed capital growth and the alternative investment return."},
        {"q": "What numbers should I use for capital growth?", "a": "Long-run Australian capital city averages are around 5–7% nominal, but with high variance. Use a conservative number (3–4%) for stress testing."},
    ],
}


def _amortizing_payment(principal: float, annual_rate: float, years: int) -> float:
    n = years * 12
    r = (annual_rate / 100) / 12
    if r == 0:
        return principal / n if n else 0
    return principal * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)


def calculate(inputs: Dict[str, Any]) -> Dict[str, Any]:
    price, deposit, mortgage_rate, weekly_rent = require(
        inputs, "property_price", "deposit", "mortgage_rate", "weekly_rent"
    )
    term_years = to_int(inputs.get("term_years"), "term_years")
    years = to_int(inputs.get("years"), "years")
    buying_pct = to_float(inputs["buying_costs_percent"] if inputs.get("buying_costs_percent") not in (None, "") else 5, "buying_costs_percent")
    ongoing_pct = to_float(inputs["ongoing_costs_percent"] if inputs.get("ongoing_costs_percent") not in (None, "") else 1.5, "ongoing_costs_percent")
    growth_pct = to_float(inputs["capital_growth_percent"] if inputs.get("capital_growth_percent") not in (None, "") else 4, "capital_growth_percent")
    rent_growth_pct = to_float(inputs["rent_growth_percent"] if inputs.get("rent_growth_percent") not in (None, "") else 3, "rent_growth_percent")
    invest_pct = to_float(inputs["investment_return_percent"] if inputs.get("investment_return_percent") not in (None, "") else 7, "investment_return_percent")

    positive(price, "property_price")
    non_negative(deposit, "deposit")
    non_negative(mortgage_rate, "mortgage_rate")
    positive(term_years, "term_years")
    positive(years, "years")
    if deposit > price:
        raise ValueError("'deposit' cannot exceed 'property_price'.")

    # ---- BUY side ----
    loan = price - deposit
    monthly_payment = _amortizing_payment(loan, mortgage_rate, term_years)
    # Total mortgage paid over the comparison horizon (capped at loan term)
    months_held = min(years * 12, term_years * 12)
    mortgage_paid = monthly_payment * months_held

    buying_costs = price * (buying_pct / 100)

    # Ongoing costs grow with the property value (rough approximation)
    ongoing_total = 0.0
    val = price
    for _ in range(years):
        ongoing_total += val * (ongoing_pct / 100)
        val *= 1 + (growth_pct / 100)
    end_value = val

    # Remaining mortgage balance after `years` (only if loan term > years)
    r = (mortgage_rate / 100) / 12
    n_total = term_years * 12
    n_held = years * 12
    if r == 0:
        remaining_balance = max(loan - monthly_payment * n_held, 0)
    elif n_held >= n_total:
        remaining_balance = 0
    else:
        # Standard remaining-balance formula
        remaining_balance = loan * ((1 + r) ** n_total - (1 + r) ** n_held) / (((1 + r) ** n_total) - 1)

    equity_at_end = end_value - remaining_balance

    # Net buying cost = cash out − net equity at end
    cash_out_buy = deposit + buying_costs + mortgage_paid + ongoing_total
    total_buy_cost = cash_out_buy - equity_at_end

    # ---- RENT side ----
    rent_total = 0.0
    annual_rent = weekly_rent * 52
    for _ in range(years):
        rent_total += annual_rent
        annual_rent *= 1 + (rent_growth_pct / 100)

    # Opportunity: instead of buying, invest the deposit + buying costs at invest_pct
    invest_base = deposit + buying_costs
    invest_growth = invest_base * ((1 + invest_pct / 100) ** years)
    investment_gain = invest_growth - invest_base

    total_rent_cost = rent_total - investment_gain

    # ---- Break-even sweep — find first year where buying becomes cheaper ----
    breakeven_year = None
    for y in range(1, years + 1):
        # Recompute both sides at year y (light recomputation, kept inline for clarity)
        months_y = min(y * 12, n_total)
        mort_y = monthly_payment * months_y
        val_y = price
        ong_y = 0.0
        for _ in range(y):
            ong_y += val_y * (ongoing_pct / 100)
            val_y *= 1 + (growth_pct / 100)
        if r == 0:
            rem_y = max(loan - monthly_payment * (y * 12), 0)
        elif y * 12 >= n_total:
            rem_y = 0
        else:
            rem_y = loan * ((1 + r) ** n_total - (1 + r) ** (y * 12)) / (((1 + r) ** n_total) - 1)
        equity_y = val_y - rem_y
        buy_y = deposit + buying_costs + mort_y + ong_y - equity_y

        rent_y = 0.0
        ann = weekly_rent * 52
        for _ in range(y):
            rent_y += ann
            ann *= 1 + (rent_growth_pct / 100)
        invest_gain_y = invest_base * ((1 + invest_pct / 100) ** y) - invest_base
        rent_total_y = rent_y - invest_gain_y

        if buy_y < rent_total_y:
            breakeven_year = y
            break

    diff = total_rent_cost - total_buy_cost
    winner = "Buying is cheaper" if diff > 0 else "Renting is cheaper" if diff < 0 else "Even"

    return {
        "total_buy_cost": round(total_buy_cost, 2),
        "total_rent_cost": round(total_rent_cost, 2),
        "difference": round(diff, 2),
        "winner": winner,
        "breakeven_year": str(breakeven_year) if breakeven_year else f"Beyond {years} years",
    }

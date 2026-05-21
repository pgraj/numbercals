"""CAC Impact Simulator.

Models the impact of reducing Customer Acquisition Cost on:
  - Total acquisition cost
  - LTV/CAC ratio
  - Payback period in months

LTV = ARPU × Gross Margin / Churn Rate (simplified)
Payback Period = CAC / (ARPU × Gross Margin)
"""
from typing import Any, Dict
from ._base import positive, require

META = {
    "slug": "cac-impact",
    "name": "CAC Impact Simulator",
    "category": "business",
    "description": "Model the financial impact of reducing your Customer Acquisition Cost. Calculates LTV/CAC ratio change and payback period improvement.",
    "formula": "LTV = ARPU·Margin/Churn;  LTV/CAC = LTV÷CAC;  Payback = CAC ÷ (ARPU·Margin)",
    "fields": [
        {"name": "current_cac", "label": "Current CAC", "type": "number", "min": 0, "required": True, "placeholder": "500"},
        {"name": "new_cac", "label": "Target (Reduced) CAC", "type": "number", "min": 0, "required": True, "placeholder": "350"},
        {"name": "arpu_monthly", "label": "ARPU (monthly)", "type": "number", "min": 0, "required": True, "placeholder": "100"},
        {"name": "gross_margin_percent", "label": "Gross Margin (%)", "type": "number", "min": 0, "required": True, "placeholder": "80"},
        {"name": "monthly_churn_percent", "label": "Monthly Churn (%)", "type": "number", "min": 0, "required": True, "placeholder": "3"},
        {"name": "new_customers_per_month", "label": "New Customers per Month", "type": "number", "min": 0, "required": True, "placeholder": "100"},
    ],
    "outputs": [
        {"key": "ltv", "label": "Customer LTV", "format": "currency"},
        {"key": "current_ltv_cac", "label": "Current LTV/CAC Ratio", "format": "number"},
        {"key": "new_ltv_cac", "label": "New LTV/CAC Ratio", "format": "number"},
        {"key": "current_payback_months", "label": "Current Payback Period (months)", "format": "number"},
        {"key": "new_payback_months", "label": "New Payback Period (months)", "format": "number"},
        {"key": "monthly_savings", "label": "Monthly CAC Savings", "format": "currency"},
        {"key": "annual_savings", "label": "Annual CAC Savings", "format": "currency"},
    ],
    "faq": [
        {"q": "What's a healthy LTV/CAC?", "a": "The SaaS rule of thumb: 3× or higher is healthy, 1× or lower is unsustainable. Anything 5×+ may indicate under-investment in growth."},
        {"q": "What's a good payback period?", "a": "12 months for SMB SaaS, 18 months for mid-market, up to 24 for enterprise. Faster payback = less capital required to scale."},
    ],
}


def calculate(inputs):
    current_cac, new_cac, arpu, margin, churn, new_cust = require(
        inputs, "current_cac", "new_cac", "arpu_monthly", "gross_margin_percent", "monthly_churn_percent", "new_customers_per_month"
    )
    positive(margin, "gross_margin_percent")
    positive(churn, "monthly_churn_percent")

    monthly_gross = arpu * (margin / 100)
    # Simple LTV: monthly gross profit / monthly churn rate
    ltv = monthly_gross / (churn / 100)

    current_ratio = ltv / current_cac if current_cac else 0
    new_ratio = ltv / new_cac if new_cac else 0
    current_payback = current_cac / monthly_gross if monthly_gross else 0
    new_payback = new_cac / monthly_gross if monthly_gross else 0

    monthly_savings = (current_cac - new_cac) * new_cust

    return {
        "ltv": round(ltv, 2),
        "current_ltv_cac": round(current_ratio, 2),
        "new_ltv_cac": round(new_ratio, 2),
        "current_payback_months": round(current_payback, 1),
        "new_payback_months": round(new_payback, 1),
        "monthly_savings": round(monthly_savings, 2),
        "annual_savings": round(monthly_savings * 12, 2),
    }

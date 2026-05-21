"""Site branding — single source of truth.

All site-wide name, domain, and tagline text lives here so future renames or
domain changes are one-line edits.

To change the site name or domain in the future:
  1. Update SITE_NAME and SITE_DOMAIN below
  2. Restart the server — every template picks up the change automatically
"""

# Brand
SITE_NAME = "NumberCals"
SITE_TAGLINE = "Free online calculators for finance, health, math, physics, and more."
SITE_DESCRIPTION_SHORT = "Free, fast, mobile-friendly calculators. No sign-up required."

# Domain & URLs — used in canonical URLs, sitemap, OG tags
SITE_DOMAIN = "numbercals.com"
SITE_URL = f"https://{SITE_DOMAIN}"

# Contact (placeholder — replace with real address before launch)
SITE_CONTACT_EMAIL = f"hello@{SITE_DOMAIN}"

# Social / Open Graph image (placeholder — add a real OG image at /static/og.png)
SITE_OG_IMAGE = f"{SITE_URL}/static/og.png"

# Disclaimers — shown in footer and on relevant calculators
DISCLAIMER_GENERAL = (
    "Results are estimates only — not financial, medical, legal, or tax advice. "
    "We do not provide tax calculators; consult a qualified tax professional for tax matters."
)

# Ad network configuration (set when you have accounts approved)
# Leave empty strings to disable. The templates will skip rendering ad slots
# when the corresponding publisher ID is not set.
ADSENSE_PUBLISHER_ID = ""   # e.g. "ca-pub-XXXXXXXXXXXXXXXX"
EZOIC_SITE_ID = ""          # numeric Ezoic site id
GOOGLE_ANALYTICS_ID = "G-61RGVM24YH"    # e.g. "G-XXXXXXXXXX"

"""
backend/seo.py
==============
Dynamic sitemap.xml and robots.txt generators.

Reads REGISTRY (calculators) and TOOL_REGISTRY (tools) and emits a fresh
sitemap on every request — so the moment you add a new tool, Google can
discover it without any manual sitemap maintenance.

Wire this into main.py — see main_patch_seo.py.
"""

from datetime import date

SITE_URL = "https://numbercals.com"


def build_sitemap(calc_slugs: list[str], tool_slugs: list[str]) -> str:
    """Generate a Google-compatible sitemap.xml string."""
    today = date.today().isoformat()
    static_pages = [
        ("/",           "1.0", "weekly"),
        ("/about",      "0.5", "monthly"),
        ("/contact",    "0.5", "yearly"),
        ("/disclaimer", "0.5", "yearly"),
        ("/terms",      "0.3", "yearly"),
        ("/privacy",    "0.3", "yearly"),
    ]

    urls = []
    for path, priority, freq in static_pages:
        urls.append(_url(path, today, priority, freq))
    for slug in calc_slugs:
        urls.append(_url(f"/calculator/{slug}", today, "0.8", "monthly"))
    for slug in tool_slugs:
        urls.append(_url(f"/tools/{slug}", today, "0.9", "monthly"))

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )


def _url(path, lastmod, priority, freq):
    return (
        "  <url>\n"
        f"    <loc>{SITE_URL}{path}</loc>\n"
        f"    <lastmod>{lastmod}</lastmod>\n"
        f"    <changefreq>{freq}</changefreq>\n"
        f"    <priority>{priority}</priority>\n"
        "  </url>"
    )


def build_robots() -> str:
    """Generate robots.txt — allow all, point to sitemap."""
    return (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /api/\n"
        "\n"
        f"Sitemap: {SITE_URL}/sitemap.xml\n"
    )

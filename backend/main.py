"""NumberCals — FastAPI application.

This file does three things:

  1. JSON API at /api/* for any frontend to consume.
  2. Server-rendered HTML pages at /, /calculator/<slug>, /category/<slug>,
     /tools/standard, /tools/scientific — for SEO.
  3. Static assets at /static (CSS, JS).

The actual calculation logic lives in calculators/<name>.py — one file each.
This file just dispatches: it looks up the slug in registry.REGISTRY and
calls the module's calculate() function.

Run locally:
    pip install -r requirements.txt
    uvicorn main:app --reload --port 8000

Then open http://localhost:8000
"""
from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import registry
import branding

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title=branding.SITE_NAME, version="0.1.0")

# CORS — wide open in dev; tighten for production by listing your domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files (CSS, client-side JS for Standard / Scientific calculators).
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "templates")


# ----- JSON API -------------------------------------------------------------

@app.get("/api/categories")
def api_categories() -> Dict[str, Any]:
    """List all categories."""
    return {"categories": registry.CATEGORIES}


@app.get("/api/calculators")
def api_calculators() -> Dict[str, Any]:
    """List every registered calculator (metadata only, no formulas executed)."""
    return {
        "calculators": [
            {
                "slug": m.META["slug"],
                "name": m.META["name"],
                "category": m.META["category"],
                "description": m.META.get("description", ""),
            }
            for m in registry.ALL_MODULES
        ]
    }


@app.get("/api/calculators/{slug}")
def api_calculator(slug: str) -> Dict[str, Any]:
    """Full metadata (fields, outputs, FAQ) for one calculator."""
    try:
        mod = registry.get(slug)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"No calculator '{slug}'.")
    return {"meta": mod.META}


@app.post("/api/calculate/{slug}")
async def api_calculate(slug: str, request: Request) -> Dict[str, Any]:
    """Execute the calculator. Body: JSON dict of inputs."""
    try:
        mod = registry.get(slug)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"No calculator '{slug}'.")
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Request body must be valid JSON.")
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Request body must be a JSON object.")
    try:
        result = mod.calculate(payload)
    except ValueError as e:
        # Input-validation error — caller's fault, return 400.
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Unexpected error — log-worthy. The slug tells you exactly which file to open.
        raise HTTPException(status_code=500, detail=f"Internal error in '{slug}': {e}")
    return {"slug": slug, "inputs": payload, "result": result}


# ----- HTML pages (server-rendered for SEO) ---------------------------------

def _ctx(**extra) -> Dict[str, Any]:
    """Common template context — categories for nav, plus site-wide branding."""
    return {
        "categories": registry.CATEGORIES,
        "branding": branding,
        **extra,
    }


@app.get("/", response_class=HTMLResponse)
def page_home(request: Request) -> HTMLResponse:
    grouped = []
    for cat in registry.CATEGORIES:
        items = registry.list_by_category(cat["slug"])
        grouped.append({"category": cat, "entries": [m.META for m in items]})
    return templates.TemplateResponse(
        request, "home.html",
        _ctx(grouped=grouped, total=len(registry.ALL_MODULES)),
    )


@app.get("/calculator/{slug}", response_class=HTMLResponse)
def page_calculator(request: Request, slug: str) -> HTMLResponse:
    try:
        mod = registry.get(slug)
    except KeyError:
        raise HTTPException(status_code=404, detail="Calculator not found.")
    related = [m.META for m in registry.related(slug, limit=5)]
    return templates.TemplateResponse(
        request, "calculator.html",
        _ctx(meta=mod.META, related=related),
    )


@app.get("/category/{slug}", response_class=HTMLResponse)
def page_category(request: Request, slug: str) -> HTMLResponse:
    cat = next((c for c in registry.CATEGORIES if c["slug"] == slug), None)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found.")
    items = [m.META for m in registry.list_by_category(slug)]
    return templates.TemplateResponse(
        request, "category.html",
        _ctx(category=cat, items=items),
    )


@app.get("/tools/standard-calculator", response_class=HTMLResponse)
def page_standard(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "standard_calculator.html", _ctx())


@app.get("/tools/scientific-calculator", response_class=HTMLResponse)
def page_scientific(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "scientific_calculator.html", _ctx())


@app.get("/about", response_class=HTMLResponse)
def page_about(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "about.html", _ctx())


@app.get("/contact", response_class=HTMLResponse)
def page_contact(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "contact.html", _ctx())


@app.get("/privacy", response_class=HTMLResponse)
def page_privacy(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "privacy.html", _ctx())


@app.get("/terms", response_class=HTMLResponse)
def page_terms(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "terms.html", _ctx())


@app.get("/robots.txt")
def robots() -> Response:
    body = f"User-agent: *\nAllow: /\nSitemap: {branding.SITE_URL}/sitemap.xml\n"
    return Response(content=body, media_type="text/plain")


@app.get("/sitemap.xml")
def sitemap() -> Response:
    """XML sitemap built from registry + branding.SITE_URL, with lastmod dates."""
    from datetime import date
    today = date.today().isoformat()
    base = branding.SITE_URL

    body = '<?xml version="1.0" encoding="UTF-8"?>\n'
    body += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    # High-priority pages
    pages = [
        (f"{base}/", "1.0", today),
        (f"{base}/about", "0.5", today),
        (f"{base}/contact", "0.3", today),
        (f"{base}/privacy", "0.3", today),
        (f"{base}/terms", "0.3", today),
        (f"{base}/tools/standard-calculator", "0.7", today),
        (f"{base}/tools/scientific-calculator", "0.7", today),
    ]
    # Categories
    for c in registry.CATEGORIES:
        pages.append((f"{base}/category/{c['slug']}", "0.8", today))
    # Calculators
    for m in registry.ALL_MODULES:
        pages.append((f"{base}/calculator/{m.META['slug']}", "0.9", today))

    for url, priority, lastmod in pages:
        body += "  <url>\n"
        body += f"    <loc>{url}</loc>\n"
        body += f"    <lastmod>{lastmod}</lastmod>\n"
        body += f"    <priority>{priority}</priority>\n"
        body += "  </url>\n"
    body += "</urlset>\n"
    return Response(content=body, media_type="application/xml")


@app.get("/healthz")
def healthz() -> Dict[str, Any]:
    return {"status": "ok", "calculators_loaded": len(registry.ALL_MODULES)}

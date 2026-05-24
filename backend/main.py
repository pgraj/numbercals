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
from fastapi.responses import HTMLResponse, JSONResponse, Response, PlainTextResponse

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from tools import TOOL_REGISTRY

import registry
import branding
import datetime


from seo import build_sitemap, build_robots

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





@app.post("/api/tools/{slug}/calculate")
async def tool_calculate(slug: str, request: Request):
    tool = TOOL_REGISTRY.get(slug)
    if tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    payload = await request.json()
    try:
        return JSONResponse(tool.optimize(**payload))
    except TypeError as e:
        return JSONResponse({"ok": False, "error": f"Bad inputs: {e}"}, status_code=400)
    except Exception as e:
        return JSONResponse({"ok": False, "error": f"Server error: {e}"}, status_code=500)

@app.get("/disclaimer", response_class=HTMLResponse)
def disclaimer(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "disclaimer.html", _ctx())


# ----- HTML pages (server-rendered for SEO) ---------------------------------

def _ctx(**extra) -> Dict[str, Any]:
    """Common template context — categories for nav, plus site-wide branding."""
    return {
        "categories": registry.CATEGORIES,
        "branding": branding,
        "current_year": datetime.date.today().year,   # ← optional, for legal footer © line
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


# -----------------------------------------------------------------------------
# EDIT 3: Do the same for the calculator page route (REPLACE existing).
# This makes every calculator page eligible for the same SEO benefits.
# -----------------------------------------------------------------------------
@app.get("/calculator/{slug}", response_class=HTMLResponse)
def page_calculator(request: Request, slug: str) -> HTMLResponse:
    try:
        mod = registry.get(slug)
    except KeyError:
        raise HTTPException(status_code=404, detail="Calculator not found.")
    related = [m.META for m in registry.related(slug, limit=5)]

    # Build SEO context
    title = mod.META.get("title", mod.META.get("name", slug.replace("-", " ").title()))
    seo_ctx = dict(mod.META.get("seo", {}))
    seo_ctx.setdefault("title", f"{title} — Free Calculator | NumberCals")
    seo_ctx.setdefault(
        "description",
        mod.META.get(
            "description",
            f"Free {title.lower()} — instant results, no signup. "
            "Educational use only; verify with a qualified professional before acting.",
        ),
    )
    seo_ctx.setdefault("page_type", "SoftwareApplication")
    seo_ctx.setdefault("category", mod.META.get("category", "Engineering"))
    seo_ctx["canonical"] = f"{branding.SITE_URL}/calculator/{slug}"
    seo_ctx["breadcrumbs"] = [
        {"name": "Home", "url": "/"},
        {"name": mod.META.get("category", "Calculators"), "url": "/"},
        {"name": title, "url": f"/calculator/{slug}"},
    ]
    if mod.META.get("seo_content", {}).get("faqs"):
        seo_ctx["faqs"] = mod.META["seo_content"]["faqs"]

    return templates.TemplateResponse(
        request, "calculator.html",
        _ctx(meta=mod.META, related=related, seo=seo_ctx),
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
    seo_ctx = {
        "title": "Standard Calculator — Free Online Basic Calculator | NumberCals",
        "description": (
            "Free online standard calculator. Addition, subtraction, "
            "multiplication, division, percentage, and square root. "
            "No signup, no ads, works in any browser."
        ),
        "keywords": (
            "standard calculator, online calculator, basic calculator, "
            "free calculator, simple calculator"
        ),
        "page_type":  "SoftwareApplication",
        "category":   "Mathematics",
        "canonical":  "https://numbercals.com/tools/standard-calculator",
        "breadcrumbs": [
            {"name": "Home",                "url": "/"},
            {"name": "Calculators",         "url": "/"},
            {"name": "Standard Calculator", "url": "/tools/standard-calculator"},
        ],
    }

    meta = {
        "title": "Standard Calculator",
        "icon":  "🔢",
        "description": "Free online standard calculator for everyday arithmetic.",
        "seo_content": {
            "how_it_works": [
                "The NumberCals standard calculator handles everyday "
                "arithmetic: addition, subtraction, multiplication, division, "
                "percentage, and square root. It runs entirely in your "
                "browser — no signup, no ads, no install.",

                "Calculations follow standard order of operations. Press "
                "AC to clear everything, or CE to clear just the last "
                "entry. The display shows your current expression and the "
                "most recent answer.",
            ],
            "use_cases": [
                "Everyday quick calculations — split bills, work out tips, "
                "convert percentages",
                "Shopping comparisons and discount calculations",
                "Simple bookkeeping and budgeting math",
                "Anyone who needs a clean, fast calculator without ads or signup",
            ],
            "faqs": [
                {"q": "Is the standard calculator free?",
                 "a": "Yes — completely free, no signup, no ads, no usage limits."},
                {"q": "Does it work offline?",
                 "a": "Once the page is loaded, calculations run locally in "
                      "your browser. You only need internet to load the page."},
                {"q": "Where do I find scientific functions?",
                 "a": "Use the Scientific Calculator for trigonometry, "
                      "logarithms, exponents, and factorials."},
                {"q": "Can I use this on my phone?",
                 "a": "Yes — the calculator adapts to phone, tablet, and "
                      "desktop screen sizes."},
            ],
        },
    }

    seo_ctx["faqs"] = meta["seo_content"]["faqs"]

    return templates.TemplateResponse(
        request, "standard_calculator.html",
        _ctx(meta=meta, seo=seo_ctx),
    )


@app.get("/tools/scientific-calculator", response_class=HTMLResponse)
def page_scientific(request: Request) -> HTMLResponse:
    # ----- SEO context (used by _seo_head.html in <head>) -----
    seo_ctx = {
        "title": "Scientific Calculator — Free Online with Trig, Log, Exponents | NumberCals",
        "description": (
            "Free online scientific calculator. Trigonometric, logarithmic, "
            "exponential, factorial, and statistical functions. No signup, "
            "no ads, works in any browser."
        ),
        "keywords": (
            "scientific calculator, online scientific calculator, "
            "free scientific calculator, trig calculator, log calculator, "
            "factorial calculator, exponent calculator"
        ),
        "page_type":  "SoftwareApplication",
        "category":   "Mathematics",
        "canonical":  "https://numbercals.com/tools/scientific-calculator",
        "breadcrumbs": [
            {"name": "Home",                  "url": "/"},
            {"name": "Calculators",           "url": "/"},
            {"name": "Scientific Calculator", "url": "/tools/scientific-calculator"},
        ],
    }

    # ----- META + indexable content (used by _tool_seo_content.html) -----
    meta = {
        "title": "Scientific Calculator",
        "icon":  "🧮",
        "description": (
            "Free online scientific calculator with trigonometric, logarithmic, "
            "exponential, and factorial functions."
        ),
        "seo_content": {
            "how_it_works": [
                "The NumberCals scientific calculator runs entirely in your "
                "browser. It supports the standard scientific functions you'd "
                "find on a TI-30 or Casio fx-991: basic arithmetic, exponents "
                "and roots, trigonometric and inverse trigonometric functions "
                "(sin, cos, tan, asin, acos, atan), natural and base-10 "
                "logarithms, factorials, and constants like π and e.",

                "Calculations follow standard order of operations (BODMAS / "
                "PEMDAS) and respect parentheses. Trigonometric functions "
                "can be evaluated in radians or degrees. Memory functions "
                "(M+, M−, MR, MC) store intermediate results so you don't "
                "need to re-type them in longer multi-step calculations.",

                "Everything runs as JavaScript locally, so there is no network "
                "round-trip per calculation. The page works offline once "
                "loaded and adapts to phone, tablet, and desktop screens. No "
                "data leaves your device.",
            ],
            "use_cases": [
                "Students working through algebra, trigonometry, calculus, "
                "or statistics homework",
                "Engineers and scientists needing a quick calculation without "
                "opening MATLAB or Python",
                "Anyone who has misplaced their physical calculator or doesn't "
                "want to install yet another app",
                "Teachers demonstrating function behaviour during a classroom "
                "lesson or video tutorial",
                "Test-prep candidates practising for SAT, ACT, GRE, GMAT, or "
                "engineering entrance exams that allow scientific calculators",
            ],
            "faqs": [
                {"q": "Is the scientific calculator really free?",
                 "a": "Yes — completely free, with no signup, no ads, and no "
                      "usage limits. It runs entirely in your browser."},
                {"q": "Does it work offline?",
                 "a": "Once the page has loaded, all calculations run locally "
                      "in JavaScript. You only need an internet connection to "
                      "load the page initially."},
                {"q": "Does it support radians and degrees?",
                 "a": "Yes. The mode toggle switches between RAD and DEG. "
                      "Trigonometric functions use whichever mode is "
                      "currently selected."},
                {"q": "What functions are included?",
                 "a": "Arithmetic (+, −, ×, ÷), powers and roots (x², x³, "
                      "xʸ, √, ∛), trigonometric (sin, cos, tan and inverses), "
                      "logarithms (log, ln), exponentials (eˣ, 10ˣ), "
                      "factorials (n!), and the constants π and e."},
                {"q": "How is this different from the standard calculator?",
                 "a": "The standard calculator handles basic arithmetic for "
                      "everyday math. The scientific calculator adds the "
                      "trigonometric, logarithmic, exponential, and factorial "
                      "functions plus parentheses and mathematical constants — "
                      "covering algebra through engineering coursework."},
                {"q": "Is this calculator approved for standardised exams?",
                 "a": "Online calculators are generally not permitted in "
                      "exam halls — most exam boards require an approved "
                      "physical calculator (TI-30, Casio fx-991, etc.). "
                      "Use this tool for practice and study, not during "
                      "the exam itself."},
            ],
        },
    }

    # Mirror FAQs into seo dict so FAQPage JSON-LD picks them up
    seo_ctx["faqs"] = meta["seo_content"]["faqs"]

    return templates.TemplateResponse(
        request, "scientific_calculator.html",
        _ctx(meta=meta, seo=seo_ctx),
    )


# ----- Generic tools route — MUST stay below all dedicated tool routes -----
@app.get("/tools/{slug}", response_class=HTMLResponse)
def tool_page(request: Request, slug: str) -> HTMLResponse:
    tool = TOOL_REGISTRY.get(slug)
    if tool is None:
        raise HTTPException(status_code=404, detail="Tool not found.")

    seo_ctx = dict(tool.META.get("seo", {}))
    seo_ctx["canonical"] = f"https://numbercals.com/tools/{slug}"
    seo_ctx["faqs"] = tool.META.get("seo_content", {}).get("faqs", [])
    seo_ctx["breadcrumbs"] = [
        {"name": "Home",             "url": "/"},
        {"name": "Tools",            "url": "/tools"},
        {"name": tool.META["title"], "url": f"/tools/{slug}"},
    ]

    return templates.TemplateResponse(
        request, tool.META["template"],
        _ctx(meta=tool.META, seo=seo_ctx),
    )

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

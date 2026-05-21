# NumberCals — Python Calculator Platform

108 free online calculators across finance, health, math, physics, time, business, property, and sports.
**One file per calculator** — designed for easy debugging.

Includes 15 advanced Bucket-2 simulation calculators: rental yield, buy-vs-rent,
property cashflow, mortgage stress test, inflation impact, price elasticity,
CAC/LTV simulators, and more.

**Note:** This platform deliberately excludes tax-computation calculators (income tax, sales tax, etc.) due to legal-liability concerns. Tax rules vary by jurisdiction and change annually — consult a qualified tax professional or use official government calculators for tax matters.

## Documentation

- 📋 `TEST_REPORT.md` — 376 tests, all passing. Includes hand-verified reference values.
- 🚀 `DEPLOYMENT.md` — Step-by-step deployment guide (Render and VPS paths).
- 🔐 `PRODUCTION_READINESS.md` — Honest assessment of what's needed before public launch.

---

## Quick start (local development)

### Mac / Linux

```bash
unzip numbercals.zip
cd numbercals
./run.sh
```

### Windows

1. Unzip `numbercals.zip`
2. Open the `numbercals` folder
3. Double-click `run.bat`

The script creates a venv, installs deps, and starts the server at http://localhost:8000.

Requires Python 3.9+.

---

## Deploying to production

See `DEPLOYMENT.md` for the full guide. The short version:

- **Render (managed, $7/mo):** push to GitHub, connect to Render, it reads `render.yaml` and deploys
- **VPS ($5–6/mo):** `docker build -t numbercals . && docker run -d -p 127.0.0.1:8000:8000 numbercals`, plus nginx + certbot

Both paths produce a public HTTPS site at `https://numbercals.com` (or whatever domain you set).

---

## Customising

Open `backend/branding.py` — single source of truth for:

- Site name, domain, tagline
- Contact email
- Ad network IDs (AdSense, Ezoic) — empty by default
- Google Analytics ID — empty by default

Change values, restart the server, every page updates.

---

## Architecture

```
numbercals/
├── run.sh / run.bat               ← Local development runner
├── render.yaml                    ← Deploy to Render
├── Dockerfile                     ← Deploy to a VPS
├── README.md, DEPLOYMENT.md, PRODUCTION_READINESS.md, TEST_REPORT.md
└── backend/
    ├── main.py                    ← FastAPI app (HTML + JSON API)
    ├── branding.py                ← Site name, domain, ad IDs
    ├── registry.py                ← slug → calculator module dispatcher
    ├── requirements.txt
    ├── calculators/               ← One file per calculator (72 total)
    │   ├── _base.py
    │   ├── simple_interest.py
    │   └── ... (71 more)
    ├── templates/
    │   ├── base.html              ← Layout: nav, footer, ad slots
    │   ├── home.html, calculator.html, category.html
    │   ├── about.html, contact.html, privacy.html, terms.html
    │   └── standard_calculator.html, scientific_calculator.html
    ├── static/
    └── tests/
        ├── smoke_test.py
        ├── test_calculators.py
        └── test_api.py
```

### How a request flows

1. User picks a calculator → form rendered from META.fields
2. Browser POSTs JSON to `/api/calculate/<slug>`
3. `main.py` looks up slug in `registry.REGISTRY` → gets module
4. Module's `calculate(inputs)` runs and returns a dict
5. JSON returned to browser, formatted per META.outputs (currency / percent / table / etc)

One bug = one file to open.

---

## Adding a new calculator (3 steps)

1. Create `backend/calculators/my_new_calc.py` with `META` dict + `calculate()` function
2. Add `from calculators import my_new_calc` to `registry.py`
3. Append `my_new_calc` to `ALL_MODULES` in `registry.py`

Frontend picks it up automatically — homepage card, category page, sitemap, FAQ schema.

---

## Verify everything works

```bash
cd backend
source .venv/bin/activate      # Mac/Linux
.venv\Scripts\activate         # Windows
python -m pytest tests/ -q
```

Expected: `555 passed`.

---

## JSON API

| Method | Path | Description |
| --- | --- | --- |
| GET  | `/api/categories`              | List all categories |
| GET  | `/api/calculators`             | List all calculators (metadata) |
| GET  | `/api/calculators/{slug}`      | Full metadata for one calculator |
| POST | `/api/calculate/{slug}`        | Run a calculation — body is JSON dict |
| GET  | `/healthz`                     | Health check |
| GET  | `/sitemap.xml`                 | Sitemap for search engines |
| GET  | `/robots.txt`                  | robots.txt |

Errors: 400 (bad input), 404 (unknown slug), 500 (unexpected error, with slug in message).

---

## Calculator counts

| Category | Count |
| --- | --- |
| Finance | 16 |
| Health | 8 |
| Math | 23 |
| Geometry | 16 |
| Time & Motion | 6 |
| Physics | 18 |
| Engineering | 3 |
| Business | 11 |
| Property | 5 |
| Sports | 2 |
| **Total** | **108** |

**Out of scope by design:** income tax, sales tax, and any other tax calculators.

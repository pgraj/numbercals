# NumberCals — Production Readiness Assessment

**Short answer: not yet.** This is solid development-grade code with full test coverage of the business logic, but it needs ~1–2 days of hardening before going live to the public internet.

Below is a checklist of what's present, what's missing, and what to do about each. Items are flagged:

- 🟢 **READY** — works as-is in production
- 🟡 **NEEDS CHANGE** — small edit before deploy (most are 1-line changes)
- 🔴 **MISSING** — needs to be added before public launch

---

## 1. Application correctness

| Item | Status | Notes |
| --- | --- | --- |
| 72 calculators tested with reference values | 🟢 READY | 376 tests pass; see TEST_REPORT.md |
| HTTP API error handling (400/404/500) | 🟢 READY | Tested; ValueError → 400, KeyError → 404 |
| Server-rendered HTML for SEO | 🟢 READY | All pages render with canonical URL, OG tags, FAQ schema |
| Mobile responsive UI | 🟢 READY | Tailwind mobile-first; 44px tap targets |
| Tax calculators removed | 🟢 READY | Deliberate decision — tax rules are jurisdictional, change annually, and create legal liability. Footer disclaimer makes this explicit. |
| Football WP model is heuristic | 🟡 NEEDS CHANGE | Add a "for illustration only" disclaimer or recalibrate against historical match data |

## 2. Security

| Item | Status | Notes |
| --- | --- | --- |
| CORS is wide open (`allow_origins=["*"]`) | 🔴 MUST FIX | Open `main.py`, change to `allow_origins=["https://yourdomain.com"]`. This is currently exploitable for cross-site abuse. |
| No rate limiting | 🔴 MUST FIX | Anyone can hammer `/api/calculate/*` indefinitely. Add `slowapi` or put the app behind Cloudflare/nginx with rate limits. |
| No HTTPS in the stack as shipped | 🔴 MUST FIX | Uvicorn alone serves HTTP. Put it behind nginx, Caddy, or a managed load balancer (e.g. AWS ALB) that terminates TLS. |
| No security headers (CSP, HSTS, X-Frame-Options) | 🔴 MISSING | Add `secure-headers` middleware or set them at the reverse proxy. |
| Input validation centralised in calculators | 🟢 READY | Every calculator raises `ValueError` for bad input → HTTP 400, no traceback leaked. |
| No SQL / no database | 🟢 READY | Nothing to inject into — pure-function calculators. |
| Templates auto-escape user input | 🟢 READY | Jinja2 autoescape is on by default. Tested with HTML special characters in slugs / titles. |
| No secrets in repo | 🟢 READY | Nothing to commit beyond code. Add real secrets via env vars only. |

## 3. Performance & deployment

| Item | Status | Notes |
| --- | --- | --- |
| `--reload` flag is dev-only | 🔴 MUST CHANGE | The runner script uses `uvicorn --reload`. For production, run via `gunicorn -k uvicorn.workers.UvicornWorker -w 4 main:app` (4 workers, no reload). |
| Tailwind via CDN | 🟡 NEEDS CHANGE | Works, but adds ~200KB of unused CSS and depends on Tailwind CDN being up. Replace with a built bundle: `npx tailwindcss -i in.css -o static/tailwind.css --minify`, then change `base.html` to link the local file. |
| No caching headers on static assets | 🟡 NEEDS CHANGE | Set `Cache-Control: public, max-age=31536000, immutable` for /static/* — easy at the reverse-proxy layer. |
| No CDN | 🟡 NEEDS CHANGE | For SEO-friendly global performance, put CloudFront / Cloudflare in front. |
| Sitemap placeholder URL | 🔴 MUST CHANGE | `main.py` `/sitemap.xml` hardcodes `https://example.com`. Replace with your real domain. |
| Health check at `/healthz` | 🟢 READY | Returns 200 + calculator count; suitable for load-balancer health checks. |
| Logs to stdout | 🟡 NEEDS CHANGE | Uvicorn logs go to stdout. Acceptable, but add a structured logging format (JSON) and ship to your log aggregator (CloudWatch / Loki / Datadog). |

## 4. Observability

| Item | Status | Notes |
| --- | --- | --- |
| Application logs | 🟡 NEEDS CHANGE | Default uvicorn access log; add request ID + JSON formatting |
| Error tracking | 🔴 MISSING | Add Sentry (10 lines): `pip install sentry-sdk; sentry_sdk.init(dsn=...)` |
| Metrics | 🔴 MISSING | Add `prometheus-fastapi-instrumentator` for request rate, latency, error count per endpoint |
| Uptime monitoring | 🔴 MISSING | UptimeRobot / Pingdom against `/healthz` |
| Per-calculator usage analytics | 🔴 MISSING | If you want to know which calculators are popular for SEO investment decisions, add basic event logging |

## 5. SEO

| Item | Status | Notes |
| --- | --- | --- |
| Canonical URLs | 🟢 READY | Every page sets canonical |
| Open Graph tags | 🟢 READY | OG title + description on every page |
| FAQ JSON-LD schema | 🟢 READY | Auto-generated from META.faq on every calculator page |
| Sitemap.xml | 🟡 NEEDS CHANGE | Works, but the base URL is `example.com` — must replace |
| robots.txt | 🔴 MISSING | Add a basic `/robots.txt` route or static file |
| Image OG tags | 🔴 MISSING | No `og:image` set. Add per-category preview images. |
| Page load speed (Lighthouse score) | 🟡 NEEDS MEASUREMENT | Tailwind CDN drags this down; measure after switching to built bundle |
| Analytics tag | 🔴 MISSING | No Google Analytics / Plausible. Add to `base.html`. |

## 6. Monetisation (if planned)

| Item | Status | Notes |
| --- | --- | --- |
| AdSense / ad slots | 🔴 MISSING | No ad code in templates. Decide on placement and add to `base.html` |
| Affiliate links | 🔴 MISSING | Not implemented. Plug into the related-calculators block if relevant |

## 7. Legal

| Item | Status | Notes |
| --- | --- | --- |
| Disclaimer in footer | 🟢 READY | "Results are estimates — not financial, medical, or legal advice." present |
| Privacy policy | 🔴 MISSING | Required if you add analytics, ads, or any form of tracking |
| Terms of use | 🔴 MISSING | Recommended even for a free utility site |
| Cookie banner | 🔴 MISSING | Required in EU / UK if you use analytics cookies |

---

## Minimum changes to deploy publicly (P0 — must do before launch)

Time estimate: **2–4 hours**, in this order:

1. **Replace `https://example.com` in `main.py` `/sitemap.xml`** with your real domain (1 line).
2. **Tighten CORS** in `main.py`: change `allow_origins=["*"]` to `["https://yourdomain.com"]` (1 line).
3. **Run with gunicorn instead of `uvicorn --reload`.** Example: `gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000 main:app`.
4. **Put nginx/Caddy in front for HTTPS + rate limiting + caching headers.** Sample nginx block in the appendix below.
5. **Build Tailwind locally** (replaces CDN). 5 minutes:
   ```bash
   cd backend && npm install -D tailwindcss
   npx tailwindcss -i input.css -o static/tailwind.css --minify
   ```
   Then in `templates/base.html` replace the `<script src="https://cdn.tailwindcss.com">` line with `<link rel="stylesheet" href="/static/tailwind.css">`.
6. **Add a `robots.txt`** at `static/robots.txt`:
   ```
   User-agent: *
   Allow: /
   Sitemap: https://yourdomain.com/sitemap.xml
   ```

## Strongly recommended before launch (P1)

7. **Add Sentry** for error tracking (15 minutes).
8. **Add Prometheus instrumentation** for basic metrics (15 minutes).
9. **Add an analytics tag** (5 minutes if you have a property).
10. **Write privacy policy + terms of use** templates (30 minutes with a generator).
11. **Set Cache-Control headers** on /static/* at the reverse-proxy layer.

## Nice to have (P2)

12. Add `og:image` per calculator/category.
13. Add structured data (`Calculator` or `HowTo` schema) per calculator page.
14. Pre-compute Lighthouse scores in CI.
15. Add a CI workflow (GitHub Actions) that runs `pytest tests/` on every push.

---

## Appendix — Sample nginx config

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate     /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Static asset caching
    location /static/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_cache_valid 200 1y;
        add_header Cache-Control "public, max-age=31536000, immutable";
    }

    # Rate limit the API
    limit_req_zone $binary_remote_addr zone=api:10m rate=30r/m;
    location /api/ {
        limit_req zone=api burst=10 nodelay;
        proxy_pass http://127.0.0.1:8000;
    }

    # Everything else
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Appendix — Sample systemd service for gunicorn

```ini
[Unit]
Description=NumberCals
After=network.target

[Service]
User=numbercals
WorkingDirectory=/opt/numbercals/backend
Environment="PATH=/opt/numbercals/backend/.venv/bin"
ExecStart=/opt/numbercals/backend/.venv/bin/gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 127.0.0.1:8000 main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## Honest summary

What I built: a tested, working calculator platform with verified math, sensible architecture, and clean separation of concerns. The 389-test suite (TEST_REPORT.md) is real and reproducible.

What's not here: the 8–12 hours of deployment-engineering work to make this safe and observable on the public internet. None of it is hard. None of it has been done yet. Use the P0 list above as your launch checklist.

If you want, I can build any of the P0 items as a follow-up.

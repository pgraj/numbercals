# NumberCals — SEO & AdSense Readiness

This document is the honest scorecard of where the site stands for search ranking
and ad-network approval.

## What's already implemented (technical SEO) ✅

| Item | Status | Where |
|---|---|---|
| Server-side rendered HTML (crawlable without JS) | ✅ | All routes |
| Unique `<title>` per page | ✅ | base.html + per-page overrides |
| Unique `<meta description>` per page | ✅ | base.html + per-page overrides |
| Canonical URLs on every page | ✅ | base.html |
| Open Graph tags (og:type, title, description, url, image, site_name) | ✅ | base.html |
| Twitter Card tags | ✅ | base.html |
| Mobile-responsive | ✅ | Tailwind mobile-first |
| Semantic HTML (h1/h2/h3 hierarchy) | ✅ | All templates |
| Breadcrumb visual navigation | ✅ | calculator.html, category.html |
| Sitemap.xml with `lastmod` and `priority` | ✅ | main.py `/sitemap.xml` |
| robots.txt referencing sitemap | ✅ | main.py `/robots.txt` |
| Favicons (SVG + PNG at 16/32/180px) | ✅ | static/favicon.* |
| og:image (1200×630 PNG and SVG) | ✅ | static/og.png |
| **JSON-LD: Organization + WebSite** (sitewide) | ✅ | base.html |
| **JSON-LD: Article** (per-calculator) | ✅ | calculator.html |
| **JSON-LD: BreadcrumbList** (per-calculator) | ✅ | calculator.html |
| **JSON-LD: FAQPage** (per-calculator) | ✅ | calculator.html |
| Internal linking via Related Calculators | ✅ | calculator.html |
| "About this calculator" content block before form | ✅ | calculator.html |
| "What you'll need" + "What you'll get" sections | ✅ | calculator.html |
| About / Contact / Privacy / Terms pages | ✅ | templates/ |

## What's NOT done (and what to do about each) ⚠️

| Item | Why it matters | What to do |
|---|---|---|
| **Per-calculator long-form content** | AdSense reviewers reject thin pages. Current pages have ~250 words of unique content (formula + FAQ + about). Top calculator sites have 500–1000. | Manually write 2–3 paragraphs per high-value calculator (mortgage, BMI, EMI, BMR, compound interest). Treat as a slow project — you can launch first, write later. |
| **Real examples on each calculator page** | Google's helpful-content algorithm specifically looks for "worked examples". | Add a "Worked Example" section to META for high-value calcs, then surface it in the template. |
| **Google Search Console verification** | Required to submit sitemap and monitor indexing. | Add property at search.google.com/search-console, verify via Cloudflare DNS TXT, submit sitemap. |
| **Google Analytics property** | Tracks which calculators get traffic. | Create at analytics.google.com, paste the G-XXXX ID into `branding.py`. |
| **Bing Webmaster verification** | Bing/DuckDuckGo source from Bing's index. ~10% of search traffic. | Similar process at bing.com/webmasters. |
| **Backlinks** | The single biggest ranking factor. New domains rank slowly without them. | Submit to relevant directories: ProductHunt, GitHub Awesome lists, Reddit (carefully). |
| **Page speed** | Tailwind CDN adds ~150ms latency. Google penalises slow pages. | Switch to built Tailwind bundle before launch — see `PRODUCTION_READINESS.md`. |
| **Image alt text** | If you ever add images, they need alt text. | Currently moot — no images. |
| **Schema.org `Calculator` type** | This is a non-standard type some SEO tools recommend. | Article + FAQPage are enough. Skip this unless ranking stalls. |

## AdSense Approval Checklist

AdSense has gotten strict. New sites typically get rejected for "low value content"
even when technically fine. Here's the realistic path:

### Before you apply (P0)

- [ ] Site live on `https://numbercals.com` with HTTPS working
- [ ] All 108 calculators work end-to-end (verified by pytest)
- [ ] Privacy Policy page exists and is linked from footer ✅ (done)
- [ ] Terms of Use page exists and is linked from footer ✅ (done)
- [ ] About page describes what the site does ✅ (done)
- [ ] Contact page with a real email address ✅ (done — uses `hello@numbercals.com`, set it up at your registrar/mail provider)
- [ ] Site is indexable: robots.txt allows crawlers ✅ (done)
- [ ] Sitemap submitted to Google Search Console (you have to do this)
- [ ] At least 1–2 weeks of indexing — some pages appearing in `site:numbercals.com` Google search
- [ ] Site has no broken links (test before applying)
- [ ] Domain is at least 1 month old (AdSense unofficially prefers older domains)

### Then apply

- [ ] Sign up at https://adsense.google.com
- [ ] Add `numbercals.com` as a site
- [ ] Add the AdSense script (your account ID goes in `branding.py` → `ADSENSE_PUBLISHER_ID`)
- [ ] Wait 1–14 days for review

### If rejected ("Low Value Content" is the common reason)

- [ ] Wait 1 month
- [ ] Add long-form content (300+ words of unique writing) to 20+ calculator pages
- [ ] Reapply

### Alternative: apply to Ezoic in parallel

- [ ] Sign up at https://ezoic.com
- [ ] They accept newer sites more readily
- [ ] Lower payouts than mature AdSense, but you start earning
- [ ] Can run alongside AdSense once approved

## Validation: how to check your SEO is actually working

After you deploy:

1. **Google Rich Results Test** — https://search.google.com/test/rich-results
   Paste any calculator URL. Should detect: Article, BreadcrumbList, FAQPage,
   WebSite, Organization.

2. **Schema.org Validator** — https://validator.schema.org/
   More detailed than Google's tool. Should show zero errors.

3. **PageSpeed Insights** — https://pagespeed.web.dev/
   Aim for mobile score 90+, desktop 95+. Will flag Tailwind CDN as an issue —
   addressed by switching to built bundle in production.

4. **Open Graph Debugger** — https://developers.facebook.com/tools/debug/
   Paste URL, check og:image renders. If it doesn't, force a re-scrape.

5. **Twitter Card Validator** — https://cards-dev.twitter.com/validator
   Same idea, for Twitter Cards.

6. **`site:numbercals.com` search** — Once deployed, search Google for this query
   to see what's indexed. Initially nothing. After 1–2 weeks, you should see
   most pages appear.

7. **Search Console "Coverage" report** — Tells you which pages Google indexed
   and which it couldn't. Check weekly.

## Realistic timeline

| Week | What happens |
|---|---|
| 1 | Deploy site, submit sitemap to Search Console |
| 2 | First few pages indexed by Google |
| 3-4 | Most pages indexed; start ranking for very long-tail queries |
| 4-8 | Apply to AdSense (after content is mature) or Ezoic |
| 8-12 | First meaningful traffic from organic search |
| 3-6 months | Steady traffic builds; ranking for medium-difficulty queries |
| 6-12 months | Significant traffic if SEO is good; revenue depends on niches |

Calculator sites can do very well in the long run because:
- Search intent is very specific (high conversion to "engagement")
- Every calculator is a unique landing page
- People come back to use the same calculator repeatedly

But it's still SEO — you need patience and consistent effort.

## What I cannot do for you

These steps require your accounts:

1. Register the domain at Cloudflare (or your chosen registrar)
2. Push the code to your GitHub
3. Create a Render account and deploy
4. Set up DNS in Cloudflare
5. Create Google Search Console account and verify the domain
6. Create Google Analytics property
7. Apply to AdSense / Ezoic
8. Set up the contact email account (`hello@numbercals.com`)
9. Any content writing (worked examples, blog posts, etc.) — though I can help draft them

The code is ready. The deployment process is documented in `DEPLOYMENT.md`. Once
you've registered the domain and pushed the code, the rest is your accounts and
your time.

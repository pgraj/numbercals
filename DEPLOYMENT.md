# NumberCals Deployment Guide

This guide walks you through deploying NumberCals to a public-facing URL with
a custom domain (`numbercals.com`) and HTTPS.

Two deployment paths are covered:
- **Path A — Render Free** (managed, easiest, **$0/month**) — pick this for the first launch. Sleeps after 15 min idle, ~60s cold start when waking up. Fine for low-traffic launch period.
- **Path B — VPS** (DigitalOcean / Hetzner, $5-6/month, more control) — migrate here later if useful

Both paths assume:
- You own `numbercals.com` (or whatever domain you registered)
- You have a GitHub account
- The code from this repo is pushed to a GitHub repo (call it whatever you want)

---

## Pre-deployment: domain setup

### Step 1 — Register the domain

If you haven't already, register `numbercals.com` (or `.com`) at one of:

- **Cloudflare Registrar** (recommended — cheapest, no upsells) — https://www.cloudflare.com/products/registrar/
- **Namecheap** — https://www.namecheap.com
- **Porkbun** — https://porkbun.com

Cost: ~$10–15/year for `.com` or `.net`.

### Step 2 — Set up Cloudflare DNS (free, recommended either way)

Even if you registered elsewhere, point the domain to Cloudflare's nameservers
for free CDN, HTTPS, and DDoS protection:

1. Sign up at https://cloudflare.com (free plan is fine)
2. "Add a Site" → enter `numbercals.com`
3. Cloudflare gives you two nameserver addresses (e.g. `aria.ns.cloudflare.com`)
4. At your registrar, change the domain's nameservers to those two
5. Wait 5 minutes to a few hours for propagation

You'll add the actual DNS record (A or CNAME) at Cloudflare in Step 4 of whichever path you pick.

---

## Path A — Deploy on Render

Easiest path. ~30 minutes total.

### Step 1 — Push the code to GitHub

```bash
cd numbercals
git init
git add .
git commit -m "Initial commit"
# Create a new repo at https://github.com/new (private or public, your call)
git remote add origin git@github.com:YOUR_USERNAME/numbercals.git
git push -u origin main
```

### Step 2 — Create the Render service

1. Sign up at https://render.com
2. New → Blueprint
3. Connect your GitHub account → select the `numbercals` repo
4. Render reads `render.yaml` and provisions the service automatically
5. First deploy takes ~3 minutes; you'll get a URL like `numbercals.onrender.com`

Visit that URL — your site should be live.

### Step 3 — Add the custom domain in Render

1. In the Render dashboard, go to your service → Settings → Custom Domains
2. Add `numbercals.com` and `www.numbercals.com`
3. Render shows you a target value (something like `numbercals.onrender.com`)

### Step 4 — Point DNS at Render (in Cloudflare)

1. Go to Cloudflare → your domain → DNS → Records
2. Add a `CNAME` record:
   - Name: `@` (or `numbercals.com`)
   - Target: the Render target from Step 3
   - Proxy status: **Proxied** (orange cloud on)
3. Add another `CNAME` for `www` pointing to the same target

Wait a few minutes. Render will auto-issue an HTTPS certificate. You should now be able to visit `https://numbercals.com`.

### Step 5 — Update `branding.py` and redeploy

The site name and domain are already set in `backend/branding.py`. Verify the
domain matches what you registered. If you used `.com` instead of `.net`,
change `SITE_DOMAIN` in that file, commit, and push — Render auto-deploys.

### Step 6 — Configure analytics and ads (optional, do later)

Open `backend/branding.py` and fill in:

```python
GOOGLE_ANALYTICS_ID = "G-XXXXXXXXXX"     # from Google Analytics
ADSENSE_PUBLISHER_ID = "ca-pub-XXXXXXXX" # from AdSense (after approval)
EZOIC_SITE_ID = "12345"                  # from Ezoic (after approval)
```

The templates conditionally render ad slots and tracking only when these are set,
so you can launch without them and add them in once approved. Commit + push for
auto-redeploy.

---

## Path B — Deploy on a VPS (DigitalOcean / Hetzner)

More work, more control. ~2 hours if you're comfortable with Linux.

### Step 1 — Provision a VPS

Pick one:
- **DigitalOcean Basic Droplet** — $6/month, 1 vCPU, 1 GB RAM, choose Sydney region
- **Hetzner CX22** — €4.5/month, 2 vCPU, 4 GB RAM, choose Helsinki or Ashburn region
- **Linode Nanode** — $5/month, 1 vCPU, 1 GB RAM

Choose Ubuntu 24.04 LTS as the OS. Add your SSH key during creation.

### Step 2 — Initial server setup

SSH in as root, then:

```bash
# Create a non-root user
adduser numbercals
usermod -aG sudo numbercals

# Copy SSH keys to the new user
rsync --archive --chown=numbercals:numbercals ~/.ssh /home/numbercals

# Lock down SSH (disable root login and password auth)
sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
systemctl restart ssh

# Set up firewall
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable
```

Log out, log back in as `numbercals`:

```bash
ssh numbercals@YOUR_SERVER_IP
```

### Step 3 — Install Docker

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin nginx certbot python3-certbot-nginx
sudo usermod -aG docker numbercals
# Log out and back in for the docker group to take effect
```

### Step 4 — Deploy NumberCals

```bash
# Clone your repo (assumes it's on GitHub)
git clone https://github.com/YOUR_USERNAME/numbercalss.git
cd numbercals

# Build and run the container
docker build -t numbercals .
docker run -d --name numbercals --restart=always -p 127.0.0.1:8000:8000 numbercals

# Verify it's running
curl http://127.0.0.1:8000/healthz
# Expected: {"status":"ok","calculators_loaded":72}
```

### Step 5 — Configure nginx as reverse proxy

```bash
sudo nano /etc/nginx/sites-available/numbercals
```

Paste the config from `PRODUCTION_READINESS.md` (appendix), then:

```bash
sudo ln -s /etc/nginx/sites-available/numbercals /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t       # validate config
sudo systemctl reload nginx
```

### Step 6 — Point DNS at the VPS (in Cloudflare)

1. Cloudflare → DNS → add an `A` record:
   - Name: `@`
   - IPv4: your VPS's public IP
   - Proxy: **Proxied** (orange cloud)
2. Add another `A` record for `www` pointing to the same IP

Wait a few minutes for propagation.

### Step 7 — Issue HTTPS certificate

```bash
sudo certbot --nginx -d numbercals.com -d www.numbercals.com
# Follow the prompts; accept terms; provide a recovery email
```

Certbot automatically updates your nginx config to redirect HTTP → HTTPS and sets
up auto-renewal.

### Step 8 — Test

Visit https://numbercals.com — site should be live with HTTPS.

### Step 9 — Set up auto-deploy on git push (optional)

For an easy way to update the site, you can set up a webhook or just use SSH to
re-deploy:

```bash
ssh numbercals@YOUR_SERVER_IP "cd numbercals && git pull && docker build -t numbercals . && docker stop numbercals && docker rm numbercals && docker run -d --name numbercals --restart=always -p 127.0.0.1:8000:8000 numbercals"
```

Save that as `deploy.sh` on your laptop and run it whenever you want to push changes.

---

## Post-deployment checklist

After your site is live on either path:

- [ ] Submit the sitemap to Google Search Console: https://search.google.com/search-console
  - Property URL: `https://numbercals.com`
  - Verify via DNS TXT record (Cloudflare makes this easy)
  - Submit `https://numbercals.com/sitemap.xml`
- [ ] Add Google Analytics property at https://analytics.google.com
  - Get the GA ID (looks like `G-XXXXXXXXXX`)
  - Paste into `branding.py` → `GOOGLE_ANALYTICS_ID`
  - Commit + redeploy
- [ ] Wait 2–4 weeks of indexed content before applying to AdSense
- [ ] In the meantime, apply to Ezoic — they accept newer sites
- [ ] Set up uptime monitoring (UptimeRobot is free) against `https://numbercals.com/healthz`
- [ ] Bookmark `https://search.google.com/search-console` and check it weekly for crawl errors

---

## Costs at a glance

| Item | Cost | Frequency |
|---|---|---|
| Domain (`.net` or `.com`) | $10–15 | per year |
| **Render Free plan** | **$0** | per month |
| Render Standard (upgrade when traffic warrants) | $25 | per month |
| (or) Hetzner CX22 VPS | $5 | per month |
| (or) DigitalOcean Basic Droplet | $6 | per month |
| Cloudflare (DNS + CDN + SSL) | $0 | free tier |
| Google Analytics | $0 | free |
| AdSense | $0 (revenue share) | when approved |
| Ezoic | $0 (revenue share) | when approved |
| Sentry (error tracking) | $0 | free tier sufficient |
| UptimeRobot | $0 | free tier sufficient |

**Total to start:** **$0/month** on Render Free, plus $10–15/year for the domain.

**When to upgrade off Render Free:** Once you have consistent daily traffic (say, 100+ visits/day spread across the day), the cold-start delay becomes noticeable. At that point, switch to Render Standard ($25/mo) or move to a Hetzner VPS ($5/mo with more setup work).

---

## When things go wrong

**Site not loading after DNS change:**
DNS propagation can take up to 24 hours. Check with `dig numbercals.com` from
your terminal. Usually it's fast (~5 min) when using Cloudflare.

**HTTPS certificate fails:**
- On Render: wait 30 minutes; if still failing, check the Custom Domains page
  for the exact error message
- On VPS: run `sudo certbot certificates` to see status; if Cloudflare is
  proxying, you need to set SSL mode to "Full (strict)" in Cloudflare's SSL/TLS settings

**500 errors after deploy:**
- On Render: check logs in the dashboard
- On VPS: `docker logs numbercals`

**Page slow to load:**
- Tailwind CDN is the usual culprit. See `PRODUCTION_READINESS.md` for how to
  switch to a built bundle (saves ~200KB and a network round trip).

**Need to roll back:**
- On Render: dashboard → Manual Deploy → pick an older commit
- On VPS: `git checkout <commit>` then rebuild the container

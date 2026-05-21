"""API integration tests — every HTTP endpoint and every calculator via the API.

Verifies the FastAPI layer correctly:
  - Returns 200 for valid calculations
  - Returns 400 for invalid inputs (ValueError -> HTTP 400)
  - Returns 404 for unknown slugs
  - Renders every HTML page without server error
"""
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from main import app
import registry
from tests.smoke_test import SAMPLES


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_healthz_ok(client):
    r = client.get("/healthz")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert data["calculators_loaded"] == len(registry.ALL_MODULES)


def test_homepage_renders(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "NumberCals" in r.text
    # All categories appear in nav (HTML escapes & to &amp;)
    import html
    for cat in registry.CATEGORIES:
        assert html.escape(cat["name"]) in r.text, f"Category {cat['name']} missing from homepage"


def test_api_list_returns_all(client):
    r = client.get("/api/calculators")
    assert r.status_code == 200
    items = r.json()["calculators"]
    assert len(items) == len(registry.ALL_MODULES)


def test_api_categories(client):
    r = client.get("/api/categories")
    assert r.status_code == 200
    cats = r.json()["categories"]
    assert len(cats) == len(registry.CATEGORIES)


@pytest.mark.parametrize("slug", sorted(registry.REGISTRY.keys()))
def test_calculator_page_renders(client, slug):
    """Every calculator's HTML page renders successfully."""
    r = client.get(f"/calculator/{slug}")
    assert r.status_code == 200, f"/calculator/{slug} returned {r.status_code}"
    # The slug always appears in the canonical URL; calculator name may be HTML-escaped.
    assert slug in r.text, f"slug '{slug}' missing from /calculator/{slug}"


@pytest.mark.parametrize("category", [c["slug"] for c in registry.CATEGORIES])
def test_category_page_renders(client, category):
    r = client.get(f"/category/{category}")
    assert r.status_code == 200


def test_tools_pages_render(client):
    for path in ["/tools/standard-calculator", "/tools/scientific-calculator"]:
        r = client.get(path)
        assert r.status_code == 200, f"{path} returned {r.status_code}"


def test_sitemap_renders(client):
    r = client.get("/sitemap.xml")
    assert r.status_code == 200
    # Should be XML, contain every slug
    for slug in registry.REGISTRY:
        assert slug in r.text


@pytest.mark.parametrize("slug", sorted(registry.REGISTRY.keys()))
def test_api_calculate_each(client, slug):
    """Every calculator works via the JSON API."""
    r = client.post(f"/api/calculate/{slug}", json=SAMPLES[slug])
    assert r.status_code == 200, f"{slug}: {r.status_code} - {r.text}"
    body = r.json()
    assert body["slug"] == slug
    assert "result" in body
    assert isinstance(body["result"], dict)


def test_api_bad_input_returns_400(client):
    r = client.post("/api/calculate/bmi", json={"weight_kg": -1, "height_cm": 175})
    assert r.status_code == 400
    assert "weight_kg" in r.json()["detail"]


def test_api_unknown_slug_returns_404(client):
    r = client.post("/api/calculate/no-such-calculator", json={})
    assert r.status_code == 404


def test_api_non_json_body_returns_400(client):
    r = client.post("/api/calculate/bmi", content="not json",
                    headers={"Content-Type": "application/json"})
    assert r.status_code == 400


def test_api_non_dict_body_returns_400(client):
    # A list isn't a valid input object
    r = client.post("/api/calculate/bmi", json=[1, 2, 3])
    assert r.status_code == 400


def test_unknown_calculator_page_returns_404(client):
    r = client.get("/calculator/no-such-calculator")
    assert r.status_code == 404


def test_unknown_category_page_returns_404(client):
    r = client.get("/category/no-such-category")
    assert r.status_code == 404

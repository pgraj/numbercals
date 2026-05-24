"""
backend/tools/cable_network.py  (v2 — realistic planning)
=========================================================
Cable Network Planner v2 — closer-to-real design tool for cable-TV operators.

What this version models that v1 did NOT
----------------------------------------
1.  Road-following routes via OSRM (free) instead of straight lines.
    Falls back to Haversine if OSRM is unreachable.
2.  Terrain-adjusted cable length via Open-Elevation (free). A 100 m segment
    that climbs 30 m needs ~104 m of cable.
3.  Real RF attenuation: RG-11 hardline trunk @ 750 MHz design frequency.
    Amplifier inserted when cumulative loss exceeds a configurable budget
    (default 30 dB) — replaces v1's fixed-interval placement.
4.  Slope/difficulty grading per segment (easy / moderate / difficult /
    specialised) drives labour cost estimates.
5.  Bill of materials with per-currency cost estimates.

What this version STILL CANNOT do
---------------------------------
- Underground utility rights-of-way (needs paid data)
- Local installation codes (jurisdiction-specific, often paywalled)
- Building obstructions (needs 3D building data)
- RF interference (needs site survey with spectrum analyser)
- Soil/trenching conditions (needs geotechnical survey)

The disclaimer must remain in force. This tool produces a credible first-pass
design — not a final plan. Field verification by a licensed engineer is
still required before deployment.
"""

import math
import urllib.request
import urllib.parse
import json
import socket
from typing import List, Dict, Any, Tuple

import networkx as nx


# ===========================================================================
# METADATA
# ===========================================================================
META = {
    "slug":             "cable-network-planner",
    "title":            "Cable Network Planner",
    "category":         "Engineering",
    "icon":             "📡",
    "template":         "tools/cable_network.html",
    "disclaimer_class": "engineering",
    "description": (
        "Plan an optimal cable-TV distribution layout. Click the map or "
        "type addresses to place a Headend and Consumer Nodes; the tool "
        "computes the shortest cable route along roads, samples terrain "
        "elevation, calculates RF attenuation, places amplifiers where "
        "they're physically needed, and estimates the bill of materials."
    ),

    "seo": {
        "title": (
            "Cable Network Planner — Free Cable-TV Layout Design with Terrain "
            "& RF Attenuation | NumberCals"
        ),
        "description": (
            "Free cable-TV network design tool. Road-following routes, "
            "terrain-adjusted cable lengths, real RF attenuation modelling, "
            "automatic amplifier placement, and currency-aware bill of "
            "materials. For cable operators."
        ),
        "keywords": (
            "cable network planner, RG-11 trunk, cable TV design, RF "
            "attenuation, amplifier placement, MST routing, terrain-adjusted "
            "cable length, free cable design tool"
        ),
        "page_type": "SoftwareApplication",
        "category":  "Engineering",
    },

    "seo_content": {
        "how_it_works": [
            "The Cable Network Planner v2 is a free browser-based tool that "
            "helps cable-TV operators sketch a credible first-pass design "
            "for a coaxial distribution network. You define a service area "
            "(country, region, city, suburb), then drop a Headend Station "
            "and Consumer Nodes by clicking the map or typing street "
            "addresses.",

            "Behind the scenes the tool builds a fully-connected weighted "
            "graph and computes a Minimum Spanning Tree (MST) using "
            "Kruskal's algorithm — the shortest set of interconnections "
            "with no loops. For each MST edge it then asks OSRM (the free "
            "Open Source Routing Machine) for the actual driving route "
            "between the two points, replacing the straight-line distance "
            "with a road-following length much closer to the real cable "
            "run. If OSRM is unreachable the tool falls back to "
            "Haversine.",

            "Each route is then sampled for elevation using Open-Elevation "
            "(free SRTM-based service). Sampling ten points along the "
            "segment lets the tool compute the slope-adjusted cable "
            "length — the longer cable needed to follow undulating "
            "ground — and the maximum grade. Segments are flagged as "
            "easy, moderate, difficult, or specialised based on terrain.",

            "Amplifier placement is then computed from real RF physics. "
            "RG-11 hardline trunk attenuates roughly 6 dB per 100 m at "
            "750 MHz. The tool walks each segment metre by metre, "
            "tracking cumulative loss, and inserts an amplifier (line "
            "extender / bi-directional amp) wherever the cumulative loss "
            "exceeds the configurable budget (default 30 dB). This "
            "replaces fixed-interval placement with physics-based "
            "placement — amplifiers go where they're actually needed.",

            "Finally the bill of materials is computed in the currency you "
            "select. Cable, amplifiers, taps, connectors, power inserters, "
            "and labour are all priced — labour scales with terrain "
            "difficulty. The output is a complete first-pass design that "
            "a licensed engineer can validate against field conditions "
            "before deployment.",
        ],
        "use_cases": [
            "Cable-TV operators sketching new neighbourhood roll-outs with "
            "terrain-aware cable estimates",
            "Project managers preparing budgetary submissions before "
            "engaging a field survey crew",
            "Network design engineers exploring multiple route options "
            "quickly before committing to a detailed plan",
            "Investors and operators estimating capex for proposed "
            "deployments in costed currency",
            "Telecommunications students learning real-world RF "
            "attenuation, terrain effects, and MST optimization",
        ],
        "faqs": [
            {"q": "What does v2 add over v1?",
             "a": "v2 follows actual roads (via OSRM), samples terrain "
                  "elevation (via Open-Elevation), models real RF "
                  "attenuation per RG-11 specifications, places "
                  "amplifiers where they are physically needed, and "
                  "produces a costed bill of materials in your selected "
                  "currency. v1 used straight-line distances and "
                  "fixed-interval amplifier placement."},
            {"q": "Is this tool production-ready?",
             "a": "No. It produces a credible first-pass design but does "
                  "not account for underground utility rights-of-way, "
                  "local installation codes, building obstructions, RF "
                  "interference, or trenching conditions. A certified, "
                  "licensed engineer must validate every output against "
                  "field conditions before deployment."},
            {"q": "Why RG-11 hardline?",
             "a": "RG-11 (.500 inch hardline) is the standard trunk cable "
                  "for cable-TV operators in HFC networks. Its 6 dB / "
                  "100 m loss at 750 MHz is the basis for the amplifier "
                  "placement calculations. RG-6 is used for drops only."},
            {"q": "What is the design frequency?",
             "a": "750 MHz is used as the design frequency — typical for "
                  "modern cable-TV operations carrying HD/SD video plus "
                  "DOCSIS data. Loss scales with the square root of "
                  "frequency, so 1 GHz losses are ~15% higher than "
                  "750 MHz."},
            {"q": "Why might OSRM or Open-Elevation fail?",
             "a": "Both are free public services. They occasionally have "
                  "outages or rate-limit aggressive users. If OSRM fails "
                  "the tool falls back to Haversine straight-line "
                  "distance. If Open-Elevation fails the tool assumes "
                  "flat terrain. Both failures are visible in the segment "
                  "table so you know which data sources contributed."},
            {"q": "Can I trust the cost estimates?",
             "a": "They are order-of-magnitude estimates based on typical "
                  "industry prices. Local prices vary widely by country, "
                  "supplier, and project scale. Use the estimates for "
                  "early-stage budgeting only; obtain real quotes from "
                  "suppliers before financial commitment."},
        ],
    },
}


# ===========================================================================
# CONSTANTS — RG-11 hardline trunk @ 750 MHz design frequency
# ===========================================================================
_EARTH_RADIUS_M = 6_371_000.0
_DESIGN_FREQ_MHZ = 750.0
_RG11_LOSS_DB_PER_100M_AT_750MHZ = 6.0     # standard value
_AMP_GAIN_DB = 30.0                          # typical line extender gain
_DEFAULT_LOSS_BUDGET_DB = 30.0               # before next amplifier required
_DROP_RG6_DEFAULT_M = 30.0                   # per-home drop cable

# Cost model — order-of-magnitude USD per unit. Multiplied by currency rate.
_BASE_COSTS_USD = {
    "trunk_per_m":     2.50,    # RG-11 hardline
    "drop_per_m":      0.50,    # RG-6
    "amplifier":      350.00,   # RF line extender
    "tap":             15.00,
    "connector":        2.00,
    "psu":            150.00,
    "headend":     25_000.00,   # rough modulator rack
    "labour_easy_per_m":         3.00,
    "labour_moderate_per_m":     5.00,
    "labour_difficult_per_m":    9.00,
    "labour_specialised_per_m": 16.00,
}

# Currency conversion (approximate, illustrative). Real cable TV operators
# should obtain quotes from local suppliers — these are for early budgeting.
_CURRENCIES = {
    "USD": {"rate": 1.00,    "symbol": "$",   "name": "US Dollar"},
    "EUR": {"rate": 0.92,    "symbol": "€",   "name": "Euro"},
    "GBP": {"rate": 0.79,    "symbol": "£",   "name": "British Pound"},
    "INR": {"rate": 83.0,    "symbol": "₹",   "name": "Indian Rupee"},
    "AUD": {"rate": 1.52,    "symbol": "A$",  "name": "Australian Dollar"},
    "CAD": {"rate": 1.36,    "symbol": "C$",  "name": "Canadian Dollar"},
    "AED": {"rate": 3.67,    "symbol": "د.إ", "name": "UAE Dirham"},
    "SAR": {"rate": 3.75,    "symbol": "﷼",  "name": "Saudi Riyal"},
    "SGD": {"rate": 1.34,    "symbol": "S$",  "name": "Singapore Dollar"},
    "ZAR": {"rate": 18.5,    "symbol": "R",   "name": "South African Rand"},
    "BRL": {"rate": 5.00,    "symbol": "R$",  "name": "Brazilian Real"},
    "MXN": {"rate": 17.0,    "symbol": "Mex$", "name": "Mexican Peso"},
}


# ===========================================================================
# GEOSPATIAL MATH
# ===========================================================================
def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in metres."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = (math.sin(dphi / 2) ** 2
         + math.cos(phi1) * math.cos(phi2) * math.sin(dlmb / 2) ** 2)
    return _EARTH_RADIUS_M * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _interp(lat1, lon1, lat2, lon2, fr):
    return (lat1 + (lat2 - lat1) * fr, lon1 + (lon2 - lon1) * fr)


# ===========================================================================
# OSRM ROAD ROUTING (free public service)
# ===========================================================================
def osrm_route(lat1, lon1, lat2, lon2, timeout=4.0):
    """
    Ask OSRM for a road-following route between two lat/lng points.

    Returns dict with:
        distance_m: route length in metres
        geometry:   list of [lat, lng] points along the route
        source:     "osrm" on success, "haversine" on fallback

    OSRM is a free public service — be respectful of rate limits.
    """
    try:
        # OSRM expects lng,lat order (not lat,lng)
        url = (
            f"https://router.project-osrm.org/route/v1/driving/"
            f"{lon1},{lat1};{lon2},{lat2}"
            f"?overview=full&geometries=geojson"
        )
        req = urllib.request.Request(url, headers={"User-Agent": "numbercals/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        if data.get("code") != "Ok" or not data.get("routes"):
            raise RuntimeError("OSRM no route")
        route = data["routes"][0]
        coords = route["geometry"]["coordinates"]   # [[lng, lat], ...]
        geometry = [[c[1], c[0]] for c in coords]   # → [[lat, lng], ...]
        return {
            "distance_m": float(route["distance"]),
            "geometry":   geometry,
            "source":     "osrm",
        }
    except (urllib.error.URLError, socket.timeout, json.JSONDecodeError,
            RuntimeError, Exception):
        return {
            "distance_m": haversine_m(lat1, lon1, lat2, lon2),
            "geometry":   [[lat1, lon1], [lat2, lon2]],
            "source":     "haversine",
        }


# ===========================================================================
# OPEN-ELEVATION TERRAIN SAMPLING (free public service)
# ===========================================================================
def open_elevation_sample(geometry, max_samples=10, timeout=5.0):
    """
    Sample elevations along a route geometry (list of [lat, lng] points).

    Returns dict with:
        elevations:    list of metres above sea level
        max_grade_pct: steepest grade encountered
        adj_length_m:  3D length over undulating terrain
        sampled:       True if Open-Elevation responded, False if fallback
    """
    if not geometry or len(geometry) < 2:
        return {"elevations": [], "max_grade_pct": 0.0,
                "adj_length_m": 0.0, "sampled": False}

    # Pick evenly-spaced sample points along the route
    n = min(max_samples, len(geometry))
    step = max(1, len(geometry) // n)
    sample_pts = geometry[::step][:max_samples]

    locations = "|".join(f"{p[0]},{p[1]}" for p in sample_pts)
    try:
        url = "https://api.open-elevation.com/api/v1/lookup?locations=" + urllib.parse.quote(locations)
        req = urllib.request.Request(url, headers={"User-Agent": "numbercals/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        elevs = [r["elevation"] for r in data.get("results", [])]
        if not elevs:
            raise RuntimeError("no elevations")
        sampled = True
    except Exception:
        elevs = [0.0] * len(sample_pts)
        sampled = False

    # Compute 3D-adjusted length + max grade
    adj_len = 0.0
    max_grade = 0.0
    for i in range(1, len(sample_pts)):
        flat_d = haversine_m(sample_pts[i-1][0], sample_pts[i-1][1],
                             sample_pts[i][0],   sample_pts[i][1])
        dh = elevs[i] - elevs[i-1] if i < len(elevs) else 0.0
        seg3d = math.sqrt(flat_d ** 2 + dh ** 2)
        adj_len += seg3d
        if flat_d > 0:
            grade = abs(dh) / flat_d * 100.0
            if grade > max_grade:
                max_grade = grade

    return {
        "elevations":    elevs,
        "max_grade_pct": round(max_grade, 1),
        "adj_length_m":  adj_len,
        "sampled":       sampled,
    }


def classify_terrain(max_grade_pct):
    """Map slope grade → difficulty bucket → labour rate key."""
    if max_grade_pct < 5:
        return ("easy",         "labour_easy_per_m")
    if max_grade_pct < 15:
        return ("moderate",     "labour_moderate_per_m")
    if max_grade_pct < 25:
        return ("difficult",    "labour_difficult_per_m")
    return ("specialised", "labour_specialised_per_m")


# ===========================================================================
# RF ATTENUATION + AMPLIFIER PLACEMENT
# ===========================================================================
def place_amplifiers(geometry, cable_length_m, loss_per_100m, loss_budget_db):
    """
    Walk the segment in equal steps, accumulate loss, drop an amplifier when
    cumulative loss > budget. Returns list of {lat, lon, distance_from_start_m,
    cumulative_loss_db} for each amplifier needed on this segment.
    """
    if cable_length_m <= 0 or len(geometry) < 2:
        return []

    # Distance between consecutive geometry points (assume even spacing for
    # simplicity — accurate enough for amplifier placement)
    n_segs = len(geometry) - 1
    step_m = cable_length_m / n_segs

    amps = []
    cum_loss = 0.0
    cum_dist = 0.0
    for i in range(1, len(geometry)):
        step_loss = (step_m / 100.0) * loss_per_100m
        cum_loss += step_loss
        cum_dist += step_m
        if cum_loss >= loss_budget_db and cum_dist < cable_length_m - 5:
            amps.append({
                "lat": geometry[i][0],
                "lon": geometry[i][1],
                "distance_from_start_m": round(cum_dist, 1),
                "cumulative_loss_db":    round(cum_loss, 2),
            })
            cum_loss = 0.0   # post-amplifier the budget resets
    return amps


# ===========================================================================
# MAIN ENTRY POINT
# ===========================================================================
def optimize(headend: List[float],
             consumers: List[List[float]],
             loss_budget_db: float = _DEFAULT_LOSS_BUDGET_DB,
             drop_cable_per_node_m: float = _DROP_RG6_DEFAULT_M,
             currency: str = "USD",
             use_road_routing: bool = True,
             use_terrain: bool = True) -> Dict[str, Any]:
    """
    Compute optimised cable layout with road routing, terrain adjustment,
    RF-physics amplifier placement, and currency-aware bill of materials.
    """
    if not headend or not consumers:
        return {
            "ok": False,
            "error": "Need a headend and at least one consumer node.",
            "edges": [], "repeaters": [], "segments": [],
            "metrics": {}, "bom": [],
        }

    # Currency setup
    cur = _CURRENCIES.get(currency.upper(), _CURRENCIES["USD"])
    rate, symbol = cur["rate"], cur["symbol"]
    def cost(usd_amount):
        return round(usd_amount * rate, 2)

    # Node list
    nodes = [("Headend", tuple(headend))]
    for i, c in enumerate(consumers):
        nodes.append((f"Consumer {i + 1}", tuple(c)))

    # Build fully-connected graph (Haversine weights for MST selection — fast).
    # Then refine winning edges with OSRM + terrain (slow, only on MST edges).
    G = nx.Graph()
    for name, coord in nodes:
        G.add_node(name, pos=coord)
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            n1, p1 = nodes[i]
            n2, p2 = nodes[j]
            G.add_edge(n1, n2, weight=haversine_m(p1[0], p1[1], p2[0], p2[1]))
    mst = nx.minimum_spanning_tree(G, algorithm="kruskal", weight="weight")

    edges, repeaters, segments = [], [], []
    total_cable_m = 0.0
    total_amps = 0
    total_labour_usd = 0.0
    rep_counter = 0
    osrm_hits = 0
    elev_hits = 0
    osrm_misses = 0
    elev_misses = 0

    for u, v, _ in mst.edges(data=True):
        p1 = G.nodes[u]["pos"]
        p2 = G.nodes[v]["pos"]
        straight_m = haversine_m(p1[0], p1[1], p2[0], p2[1])

        # 1. Road-following route via OSRM (or fallback)
        if use_road_routing:
            route = osrm_route(p1[0], p1[1], p2[0], p2[1])
        else:
            route = {"distance_m": straight_m,
                     "geometry":   [[p1[0], p1[1]], [p2[0], p2[1]]],
                     "source":     "haversine"}
        if route["source"] == "osrm":
            osrm_hits += 1
        else:
            osrm_misses += 1

        road_m = route["distance_m"]
        geometry = route["geometry"]

        # 2. Terrain-adjusted length via Open-Elevation (or fallback)
        if use_terrain:
            terrain = open_elevation_sample(geometry)
        else:
            terrain = {"elevations": [], "max_grade_pct": 0.0,
                       "adj_length_m": road_m, "sampled": False}
        if terrain["sampled"]:
            elev_hits += 1
        else:
            elev_misses += 1

        # The longer of road and terrain-3D is the actual cable length.
        # Open-Elevation returns 3D length of *sampled subset*; scale to full
        # route by ratio.
        adj_factor = (terrain["adj_length_m"] / sum(
            haversine_m(geometry[i-1][0], geometry[i-1][1],
                        geometry[i][0],   geometry[i][1])
            for i in range(1, len(geometry))
        )) if (terrain["sampled"] and len(geometry) > 1) else 1.0
        cable_m = max(road_m * adj_factor, road_m)
        total_cable_m += cable_m

        # 3. Classify terrain → labour rate
        difficulty, labour_key = classify_terrain(terrain["max_grade_pct"])
        seg_labour_usd = cable_m * _BASE_COSTS_USD[labour_key]
        total_labour_usd += seg_labour_usd

        # 4. Amplifier placement based on real RF attenuation
        amps = place_amplifiers(geometry, cable_m,
                                _RG11_LOSS_DB_PER_100M_AT_750MHZ,
                                loss_budget_db)
        seg_amp_count = len(amps)
        seg_total_loss = (cable_m / 100.0) * _RG11_LOSS_DB_PER_100M_AT_750MHZ

        for amp in amps:
            rep_counter += 1
            repeaters.append({
                "id":      f"A{rep_counter}",
                "lat":     round(amp["lat"], 6),
                "lon":     round(amp["lon"], 6),
                "segment": f"{u} → {v}",
                "distance_from_start_m": amp["distance_from_start_m"],
                "cumulative_loss_db":    amp["cumulative_loss_db"],
                "suggested_hardware":
                    f"RF Line Extender, ~{_AMP_GAIN_DB:.0f} dB gain, "
                    f"{_DESIGN_FREQ_MHZ:.0f} MHz bandwidth",
            })
        total_amps += seg_amp_count

        edges.append({
            "from": u, "to": v,
            "geometry": geometry,
            "length_m": round(cable_m, 2),
        })
        segments.append({
            "from":               u,
            "to":                 v,
            "straight_m":         round(straight_m, 1),
            "road_m":             round(road_m, 1),
            "cable_m":            round(cable_m, 1),
            "route_source":       route["source"],
            "terrain_sampled":    terrain["sampled"],
            "max_grade_pct":      terrain["max_grade_pct"],
            "difficulty":         difficulty,
            "total_loss_db":      round(seg_total_loss, 2),
            "amplifiers":         seg_amp_count,
            "labour_cost":        cost(seg_labour_usd),
            "status": ("OK" if seg_amp_count == 0
                       else f"+{seg_amp_count} amplifier(s) required"),
        })

    # ----- Bill of materials -----
    n_consumers = len(consumers)
    drop_total = n_consumers * drop_cable_per_node_m

    trunk_cost = cost(total_cable_m * _BASE_COSTS_USD["trunk_per_m"])
    drop_cost  = cost(drop_total    * _BASE_COSTS_USD["drop_per_m"])
    amp_cost   = cost(total_amps    * _BASE_COSTS_USD["amplifier"])
    tap_cost   = cost(n_consumers   * _BASE_COSTS_USD["tap"])
    conn_cost  = cost(n_consumers * 4 * _BASE_COSTS_USD["connector"])
    psu_count  = max(1, math.ceil(total_amps / 10)) if total_amps else 0
    psu_cost   = cost(psu_count     * _BASE_COSTS_USD["psu"])
    head_cost  = cost(_BASE_COSTS_USD["headend"])
    labour_cost = cost(total_labour_usd)

    materials_subtotal = (trunk_cost + drop_cost + amp_cost
                          + tap_cost + conn_cost + psu_cost + head_cost)
    grand_total = materials_subtotal + labour_cost

    bom = [
        {"component": "Headend Station (modulator rack)",
         "quantity": "1 unit",
         "unit_cost":  cost(_BASE_COSTS_USD["headend"]),
         "total_cost": head_cost,
         "notes": "Central signal source"},
        {"component": "Trunk Cable — RG-11 (.500\" hardline)",
         "quantity":  f"{total_cable_m:,.1f} m",
         "unit_cost":  cost(_BASE_COSTS_USD["trunk_per_m"]),
         "total_cost": trunk_cost,
         "notes": "Terrain-adjusted backbone length"},
        {"component": "Drop Cable — RG-6",
         "quantity":  f"{drop_total:,.0f} m",
         "unit_cost":  cost(_BASE_COSTS_USD["drop_per_m"]),
         "total_cost": drop_cost,
         "notes": f"{n_consumers} homes × {drop_cable_per_node_m:.0f} m"},
        {"component": "RF Line Extender / Bi-directional Amp",
         "quantity":  f"{total_amps} unit(s)",
         "unit_cost":  cost(_BASE_COSTS_USD["amplifier"]),
         "total_cost": amp_cost,
         "notes": f"~{_AMP_GAIN_DB:.0f} dB gain each, RF physics placement"},
        {"component": "Directional Taps / Splitters",
         "quantity":  f"{n_consumers} unit(s)",
         "unit_cost":  cost(_BASE_COSTS_USD["tap"]),
         "total_cost": tap_cost,
         "notes": "1 per consumer drop"},
        {"component": "F-Connectors",
         "quantity":  f"~{n_consumers * 4} unit(s)",
         "unit_cost":  cost(_BASE_COSTS_USD["connector"]),
         "total_cost": conn_cost,
         "notes": "4 per home (typical)"},
        {"component": "Power Inserter / PSU",
         "quantity":  f"{psu_count} unit(s)",
         "unit_cost":  cost(_BASE_COSTS_USD["psu"]),
         "total_cost": psu_cost,
         "notes": "1 per ~10 amplifiers"},
        {"component": "Labour (terrain-adjusted)",
         "quantity":  f"{total_cable_m:,.1f} m total",
         "unit_cost":  "—",
         "total_cost": labour_cost,
         "notes": "Easy/moderate/difficult/specialised rates by terrain"},
    ]

    metrics = {
        "consumer_nodes":     n_consumers,
        "total_cable_m":      round(total_cable_m, 1),
        "total_cable_km":     round(total_cable_m / 1000, 3),
        "total_amplifiers":   total_amps,
        "drop_cable_total_m": round(drop_total, 1),
        "currency":           currency.upper(),
        "currency_symbol":    symbol,
        "materials_subtotal": materials_subtotal,
        "labour_total":       labour_cost,
        "grand_total":        grand_total,
        "design_freq_mhz":    _DESIGN_FREQ_MHZ,
        "cable_loss_db_100m": _RG11_LOSS_DB_PER_100M_AT_750MHZ,
        "osrm_routes_used":   osrm_hits,
        "osrm_fallbacks":     osrm_misses,
        "terrain_sampled":    elev_hits,
        "terrain_fallbacks":  elev_misses,
    }

    return {
        "ok": True,
        "edges": edges,
        "repeaters": repeaters,
        "segments": segments,
        "metrics": metrics,
        "bom": bom,
    }

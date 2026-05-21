"""Simple beam deflection — point load at centre of a simply-supported beam.

ESTIMATION ONLY. The formula assumes:
  - Simply-supported (pinned at both ends)
  - Linear elastic material
  - Small deflections
  - Concentrated point load at the midspan

For real engineering decisions, use full structural analysis. This calculator
is for educational and rough-estimation use only.
"""
from ._base import positive, require

META = {
    "slug": "beam-deflection-simple",
    "name": "Simple Beam Deflection Calculator (Point Load, Center)",
    "category": "engineering",
    "description": "Estimate deflection at the midspan of a simply-supported beam with a centred point load. Educational use — not for design.",
    "formula": "δ = P·L³ / (48·E·I)",
    "fields": [
        {"name": "load_n", "label": "Point Load P (N)", "type": "number", "min": 0, "required": True, "placeholder": "5000"},
        {"name": "length_m", "label": "Beam Length L (m)", "type": "number", "min": 0, "required": True, "placeholder": "4"},
        {"name": "elastic_modulus_pa", "label": "Elastic Modulus E (Pa)", "type": "number", "min": 0, "required": True, "placeholder": "200e9"},
        {"name": "moment_of_inertia_m4", "label": "Moment of Inertia I (m⁴)", "type": "number", "min": 0, "required": True, "placeholder": "8.33e-6"},
    ],
    "outputs": [
        {"key": "deflection_m", "label": "Deflection at Centre (m)", "format": "number"},
        {"key": "deflection_mm", "label": "Deflection (mm)", "format": "number"},
    ],
    "faq": [
        {"q": "Typical E values?", "a": "Steel: ~200 GPa (200×10⁹ Pa). Aluminum: ~70 GPa. Concrete: ~25–35 GPa. Pine timber: ~9 GPa. Always check material datasheets for your specific grade."},
        {"q": "What does this NOT account for?", "a": "Self-weight, distributed loads, end conditions other than simply-supported, dynamic effects, material non-linearity, large deformations, buckling. Real beams need full structural analysis."},
        {"q": "Is this safe to use for design?", "a": "No. For design, use full structural analysis software or work with a licensed structural engineer."},
    ],
}

def calculate(inputs):
    P, L, E, I = require(inputs, "load_n", "length_m", "elastic_modulus_pa", "moment_of_inertia_m4")
    positive(P, "load_n"); positive(L, "length_m"); positive(E, "elastic_modulus_pa"); positive(I, "moment_of_inertia_m4")
    delta = (P * L**3) / (48 * E * I)
    return {"deflection_m": round(delta, 9), "deflection_mm": round(delta * 1000, 6)}

"""Shared configuration for the KBC vs ING Google Trends benchmark."""

import os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "benchmark.db")
CSV_DIR = os.path.join(BASE_DIR, "data", "csv")
SCHEMA_PATH = os.path.join(BASE_DIR, "db", "schema.sql")

GEO = "BE"
TIMEFRAME = "today 5-y"

# Human-readable label for terms that are Knowledge Graph topic mids rather
# than plain search strings. A bare "CBC" string is heavily polluted on
# Google Trends (basal cell carcinoma, CBC News/Radio-Canada, blood count
# tests), even with geo=BE, so the CBC brand-level term below queries the
# disambiguated topic instead - confirmed via pytrends.suggestions() and an
# interest_over_time() coverage check (mean 54.2, 262/262 non-zero points,
# vs. a polluted mean of 71.6 for the bare string or near-zero for
# "CBC Banque et Assurance", which is too specific to have real volume).
TERM_DISPLAY_LABELS = {
    "/g/1z3t2x3c8": "CBC Banque & Assurance",
}

# Product sheets: source of truth for terms, banks and languages.
# Order here defines display order across the pipeline and the Streamlit app.
# Each sheet has at most 5 terms (pytrends hard limit per request).
PRODUCTS = [
    {
        "product_id": "compte_professionnel",
        "product_label": "Compte professionnel / indépendant",
        "terms": [
            {"term": "KBC zakelijke rekening", "bank": "KBC", "language": "nl"},
            {"term": "compte professionnel ING", "bank": "ING", "language": "fr"},
            {"term": "ING zakelijke rekening", "bank": "ING", "language": "nl"},
            {"term": "Business'Bank ING", "bank": "ING", "language": "en"},
            {"term": "KBC Business Pro", "bank": "KBC", "language": "en"},
        ],
    },
    {
        "product_id": "compte_a_vue",
        "product_label": "Compte à vue particulier",
        "terms": [
            {"term": "KBC zichtrekening", "bank": "KBC", "language": "nl"},
            {"term": "compte à vue ING", "bank": "ING", "language": "fr"},
            {"term": "ING zichtrekening", "bank": "ING", "language": "nl"},
            {"term": "ING Do Basic", "bank": "ING", "language": "en"},
            {"term": "Compte Plus KBC", "bank": "KBC", "language": "fr"},
        ],
    },
    {
        "product_id": "compte_epargne",
        "product_label": "Compte épargne particulier",
        "terms": [
            {"term": "KBC spaarrekening", "bank": "KBC", "language": "nl"},
            {"term": "compte épargne ING", "bank": "ING", "language": "fr"},
            {"term": "ING spaarrekening", "bank": "ING", "language": "nl"},
            {"term": "ING Orange Savings", "bank": "ING", "language": "en"},
            {"term": "KBC Start2Save", "bank": "KBC", "language": "en"},
        ],
    },
    {
        "product_id": "investissement_courtage",
        "product_label": "Investissement / courtage en ligne",
        "terms": [
            {"term": "Bolero", "bank": "KBC", "language": "en"},
            {"term": "ING Self Invest", "bank": "ING", "language": "en"},
        ],
    },
    {
        "product_id": "app_mobile",
        "product_label": "Application mobile bancaire",
        "terms": [
            {"term": "KBC Mobile", "bank": "KBC", "language": "en"},
            {"term": "ING Banking", "bank": "ING", "language": "en"},
            {"term": "ING Smart Banking", "bank": "ING", "language": "en"},
            {"term": "KBC Touch", "bank": "KBC", "language": "en"},
        ],
    },
    {
        "product_id": "carte_credit",
        "product_label": "Carte de crédit",
        "terms": [
            {"term": "KBC kredietkaart", "bank": "KBC", "language": "nl"},
            {"term": "carte de crédit ING", "bank": "ING", "language": "fr"},
            {"term": "ING kredietkaart", "bank": "ING", "language": "nl"},
            {"term": "ING Card", "bank": "ING", "language": "en"},
            {"term": "KBC Flex Budget", "bank": "KBC", "language": "en"},
        ],
    },
    {
        "product_id": "epargne_pension",
        "product_label": "Épargne-pension",
        "terms": [
            {"term": "KBC pensioensparen", "bank": "KBC", "language": "nl"},
            {"term": "épargne pension ING", "bank": "ING", "language": "fr"},
            {"term": "ING pensioensparen", "bank": "ING", "language": "nl"},
            {"term": "ING Star Fund", "bank": "ING", "language": "en"},
            {"term": "KBC Pension Savings Fund", "bank": "KBC", "language": "en"},
        ],
    },
    {
        "product_id": "assurance_habitation",
        "product_label": "Assurance habitation",
        "terms": [
            {"term": "KBC brandverzekering", "bank": "KBC", "language": "nl"},
            {"term": "assurance habitation ING", "bank": "ING", "language": "fr"},
            {"term": "ING Home Insurance", "bank": "ING", "language": "en"},
        ],
    },
    {
        "product_id": "pret_hypothecaire",
        "product_label": "Prêt hypothécaire",
        "terms": [
            {"term": "KBC hypothecair krediet", "bank": "KBC", "language": "nl"},
            {"term": "prêt hypothécaire ING", "bank": "ING", "language": "fr"},
            {"term": "ING hypothecair krediet", "bank": "ING", "language": "nl"},
        ],
    },
    # CBC is KBC Group's own commercial brand for Wallonia and French-speaking
    # Brussels - a distinct brand with its own search demand, not a separate
    # legal entity. Mirrors the 9 KBC-vs-ING sheets above, one per product,
    # querying CBC vs the same ING terms in a fresh request (Trends values are
    # only comparable within one request, so ING has to be re-queried here
    # rather than reusing the KBC-vs-ING data). No CBC-specific term exists
    # for investissement_courtage (Bolero is a shared KBC Group brokerage
    # platform, not region-branded), so that sheet has no CBC counterpart.
    {
        "product_id": "compte_professionnel_cbc",
        "product_label": "Compte professionnel / indépendant (CBC vs ING)",
        "terms": [
            {"term": "compte professionnel CBC", "bank": "CBC", "language": "fr"},
            {"term": "KBC Business Pro", "bank": "CBC", "language": "en"},
            {"term": "compte professionnel ING", "bank": "ING", "language": "fr"},
            {"term": "ING zakelijke rekening", "bank": "ING", "language": "nl"},
            {"term": "Business'Bank ING", "bank": "ING", "language": "en"},
        ],
    },
    {
        "product_id": "compte_a_vue_cbc",
        "product_label": "Compte à vue particulier (CBC vs ING)",
        "terms": [
            {"term": "compte à vue CBC", "bank": "CBC", "language": "fr"},
            {"term": "compte à vue ING", "bank": "ING", "language": "fr"},
            {"term": "ING zichtrekening", "bank": "ING", "language": "nl"},
            {"term": "ING Do Basic", "bank": "ING", "language": "en"},
        ],
    },
    {
        "product_id": "compte_epargne_cbc",
        "product_label": "Compte épargne particulier (CBC vs ING)",
        "terms": [
            {"term": "compte épargne CBC", "bank": "CBC", "language": "fr"},
            {"term": "compte épargne ING", "bank": "ING", "language": "fr"},
            {"term": "ING spaarrekening", "bank": "ING", "language": "nl"},
            {"term": "ING Orange Savings", "bank": "ING", "language": "en"},
        ],
    },
    {
        "product_id": "app_mobile_cbc",
        "product_label": "Application mobile bancaire (CBC vs ING)",
        "terms": [
            {"term": "CBC Mobile", "bank": "CBC", "language": "en"},
            {"term": "CBC Touch", "bank": "CBC", "language": "en"},
            {"term": "ING Banking", "bank": "ING", "language": "en"},
            {"term": "ING Smart Banking", "bank": "ING", "language": "en"},
        ],
    },
    {
        "product_id": "carte_credit_cbc",
        "product_label": "Carte de crédit (CBC vs ING)",
        "terms": [
            {"term": "carte de crédit CBC", "bank": "CBC", "language": "fr"},
            {"term": "carte de crédit ING", "bank": "ING", "language": "fr"},
            {"term": "ING kredietkaart", "bank": "ING", "language": "nl"},
            {"term": "ING Card", "bank": "ING", "language": "en"},
        ],
    },
    {
        "product_id": "epargne_pension_cbc",
        "product_label": "Épargne-pension (CBC vs ING)",
        "terms": [
            {"term": "épargne pension CBC", "bank": "CBC", "language": "fr"},
            {"term": "épargne pension ING", "bank": "ING", "language": "fr"},
            {"term": "ING pensioensparen", "bank": "ING", "language": "nl"},
            {"term": "ING Star Fund", "bank": "ING", "language": "en"},
        ],
    },
    {
        # CBC term is a generic "assurance" query (as given), not
        # home-insurance-specific like the KBC/ING terms elsewhere - the CBC
        # series here measures general insurance interest, not a like-for-like
        # home insurance comparison. Flagged as a known scope difference.
        "product_id": "assurance_habitation_cbc",
        "product_label": "Assurance habitation (CBC vs ING)",
        "terms": [
            {"term": "assurance CBC", "bank": "CBC", "language": "fr"},
            {"term": "assurance habitation ING", "bank": "ING", "language": "fr"},
            {"term": "ING Home Insurance", "bank": "ING", "language": "en"},
        ],
    },
    {
        "product_id": "pret_hypothecaire_cbc",
        "product_label": "Prêt hypothécaire (CBC vs ING)",
        "terms": [
            {"term": "prêt hypothécaire CBC", "bank": "CBC", "language": "fr"},
            {"term": "prêt hypothécaire ING", "bank": "ING", "language": "fr"},
            {"term": "ING hypothecair krediet", "bank": "ING", "language": "nl"},
        ],
    },
    {
        "product_id": "marque_generique",
        "product_label": "Marque (recherche générique)",
        "terms": [
            {"term": "KBC", "bank": "KBC", "language": "en"},
            {"term": "ING", "bank": "ING", "language": "en"},
            {"term": "/g/1z3t2x3c8", "bank": "CBC", "language": "en"},
        ],
    },
]

PRODUCT_BY_ID = {p["product_id"]: p for p in PRODUCTS}

# Anomaly detection: a point must clear both thresholds to be flagged.
Z_SCORE_THRESHOLD = 1.5
SEASONAL_RATIO_THRESHOLD = 1.3

ANOMALY_TYPE_LABELS = {
    "isolated_spike": "Pic isolé",
    "sustained_trend": "Tendance soutenue",
}

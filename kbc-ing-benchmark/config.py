"""Shared configuration for the KBC vs ING Google Trends benchmark."""

import os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "benchmark.db")
CSV_DIR = os.path.join(BASE_DIR, "data", "csv")
SCHEMA_PATH = os.path.join(BASE_DIR, "db", "schema.sql")

GEO = "BE"
TIMEFRAME = "today 5-y"

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
]

PRODUCT_BY_ID = {p["product_id"]: p for p in PRODUCTS}

# Anomaly detection: a point must clear both thresholds to be flagged.
Z_SCORE_THRESHOLD = 1.5
SEASONAL_RATIO_THRESHOLD = 1.3

ANOMALY_TYPE_LABELS = {
    "isolated_spike": "Pic isolé",
    "sustained_trend": "Tendance soutenue",
}

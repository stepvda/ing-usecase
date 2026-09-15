"""Shared logic for per-bank data exports (see export_kbc_data.py / export_ing_data.py).

Each export produces a Markdown document (methodology + product sheets +
anomalies) plus a CSV of the full raw Trends time series, which is too
large to inline readably. Meant as the data handoff for a downstream
pipeline that matches these anomalies against real ad/campaign activity.
"""

import csv
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (  # noqa: E402
    ANOMALY_TYPE_LABELS, DB_PATH, GEO, PRODUCTS, SEASONAL_RATIO_THRESHOLD,
    TIMEFRAME, Z_SCORE_THRESHOLD,
)

EXPORT_DIR = os.path.dirname(os.path.abspath(__file__))


def fetch_all(conn, query, params=()):
    cur = conn.execute(query, params)
    columns = [d[0] for d in cur.description]
    return columns, cur.fetchall()


def export_trends_csv(conn, bank, csv_path):
    columns, rows = fetch_all(
        conn,
        "SELECT product_id, product_label, term, bank, language, date, value "
        "FROM trends_data WHERE bank = ? ORDER BY product_id, term, date",
        (bank,),
    )
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)
    return len(rows)


def md_table(columns, rows):
    lines = ["| " + " | ".join(columns) + " |", "|" + "|".join(["---"] * len(columns)) + "|"]
    for row in rows:
        cells = ["" if v is None else str(v).replace("|", "-").replace("\n", " ") for v in row]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def build_markdown(conn, bank, csv_filename, trends_row_count):
    bank_products = [p for p in PRODUCTS if any(t["bank"] == bank for t in p["terms"])]

    _, trends_range = fetch_all(
        conn,
        "SELECT MIN(date), MAX(date), COUNT(DISTINCT term) FROM trends_data WHERE bank = ?",
        (bank,),
    )
    min_date, max_date, term_count = trends_range[0]

    anomaly_cols_fr = ["Fiche produit", "Terme", "Date", "Valeur", "Type d'anomalie", "Score de déviation"]
    _, anomaly_rows = fetch_all(
        conn,
        "SELECT product_id, term, date, value, anomaly_type, deviation_score "
        "FROM anomalies WHERE bank = ? ORDER BY date",
        (bank,),
    )
    anomaly_rows_fr = [
        (r[0], r[1], r[2], r[3], ANOMALY_TYPE_LABELS.get(r[4], r[4]), round(r[5], 3))
        for r in anomaly_rows
    ]

    lines = []
    lines.append(f"# Export des données {bank} — Benchmark marketing KBC vs ING")
    lines.append("")
    lines.append(
        f"Document généré automatiquement à partir de `benchmark.db`, destiné à servir "
        f"d'entrée à un autre pipeline (rapprochement avec les campagnes publicitaires "
        f"réelles). Toutes les données ci-dessous concernent uniquement la banque {bank}."
    )
    lines.append("")

    lines.append("## Méthodologie")
    lines.append("")
    lines.append(f"- **Source Google Trends** : bibliothèque `pytrends`, geo=`{GEO}`, timeframe=`{TIMEFRAME}`.")
    lines.append(
        "- **Granularité réelle** : hebdomadaire (Google Trends bascule automatiquement "
        "en hebdomadaire pour une fenêtre de 5 ans, pas mensuel)."
    )
    lines.append(
        f"- **Détection d'anomalies** (par terme) : moyenne d'intérêt calculée par mois "
        f"calendaire sur toutes les années disponibles (profil de saisonnalité de référence). "
        f"Un point est flagué s'il dépasse à la fois (a) la moyenne générale du terme de plus "
        f"de {Z_SCORE_THRESHOLD} écart-type (z-score ≥ {Z_SCORE_THRESHOLD}) et (b) "
        f"{SEASONAL_RATIO_THRESHOLD}× la moyenne saisonnière normale de son mois. Les points "
        "flagués consécutifs sont groupés : un seul point isolé est un **pic isolé** "
        "(`isolated_spike`), deux points consécutifs ou plus sont une **tendance soutenue** "
        "(`sustained_trend`)."
    )
    lines.append(
        "- **Hors périmètre** : ce projet ne collecte aucune donnée publicitaire "
        "(Meta Ad Library, Google Ads Transparency Center). Le rapprochement entre ces "
        "anomalies et des campagnes publicitaires réelles est fait dans un pipeline séparé, "
        "en utilisant cet export comme donnée d'entrée."
    )
    lines.append("")

    lines.append(f"## Fiches produits {bank}")
    lines.append("")
    lines.append(f"| Fiche produit | Termes de recherche {bank} |")
    lines.append("|---|---|")
    for p in bank_products:
        bank_terms = [t["term"] for t in p["terms"] if t["bank"] == bank]
        lines.append(f"| {p['product_label']} (`{p['product_id']}`) | {', '.join(bank_terms)} |")
    lines.append("")

    lines.append("## Données Google Trends brutes")
    lines.append("")
    lines.append(
        f"{trends_row_count} points hebdomadaires, {term_count} termes, "
        f"du {min_date} au {max_date}. Fournies séparément dans "
        f"**`{csv_filename}`** (colonnes : product_id, product_label, term, bank, "
        "language, date, value) — non incluses ici pour garder ce document lisible."
    )
    lines.append("")

    lines.append(f"## Anomalies détectées ({len(anomaly_rows_fr)})")
    lines.append("")
    lines.append(md_table(anomaly_cols_fr, anomaly_rows_fr))
    lines.append("")

    return "\n".join(lines)


def run_export(bank, csv_filename, md_filename):
    csv_path = os.path.join(EXPORT_DIR, csv_filename)
    md_path = os.path.join(EXPORT_DIR, md_filename)

    conn = sqlite3.connect(DB_PATH)
    trends_row_count = export_trends_csv(conn, bank, csv_path)
    markdown = build_markdown(conn, bank, csv_filename, trends_row_count)
    conn.close()

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"Wrote {md_path}")
    print(f"Wrote {csv_path} ({trends_row_count} rows)")

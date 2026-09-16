"""Streamlit app: one tab per campaign (metadata, matched anomalies, score
detail) plus a final ING vs KBC/CBC comparison tab.

Reads campaigns, campaign_anomaly_matches and campaign_scores from SQLite,
populated by campaigns/load_campaigns.py and campaigns/scoring.py. Reuses
the scoring/labeling logic from reports.py rather than duplicating it.
Read-only - run separately from the Trends benchmark app (app.py at the
project root), which already has 18 tabs of its own.
"""

import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from config import ANOMALY_TYPE_LABELS, DB_PATH  # noqa: E402
from reports import (  # noqa: E402
    BANK_ORDER, CAMPAIGN_TYPE_LABELS, NOT_SCORABLE_REASON_LABELS, aggregate_stats, camp,
    display_term, load_campaigns_with_scores, load_matches_for_campaign,
)

PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#c98500", "#e87ba4"]
BANK_COLOR = {"KBC": PALETTE[0], "CBC": PALETTE[2], "ING": PALETTE[1]}

st.set_page_config(page_title="Campagnes vs impact Trends", layout="wide")


@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    try:
        campaigns = load_campaigns_with_scores(conn)
        matches = {c["id"]: load_matches_for_campaign(conn, c["id"]) for c in campaigns}
    finally:
        conn.close()
    return campaigns, matches


def matches_dataframe(campaign_matches):
    df = pd.DataFrame(campaign_matches)
    df["Terme"] = df["term"].map(display_term)
    df["Type"] = df["anomaly_type"].map(lambda t: ANOMALY_TYPE_LABELS.get(t, t))
    df["Confusion saisonnière"] = df["possible_seasonal_confound"].map({True: "Oui", False: "Non"})
    df["Campagnes concurrentes"] = df["overlapping_campaign_ids"].apply(lambda x: len(x) if x else 0)
    df = df.rename(columns={
        "bank": "Banque", "date": "Date", "deviation_score": "Score déviation",
        "delay_days": "Délai (j)", "contribution": "Contribution",
    })
    return df[[
        "Terme", "Banque", "Date", "Type", "Score déviation", "Délai (j)",
        "Confusion saisonnière", "Campagnes concurrentes", "Contribution",
    ]]


def render_campaign_tab(c, campaign_matches):
    col1, col2, col3 = st.columns(3)
    col1.metric("Banque", c["bank"])
    period = c["start_date"] + (f" → {c['end_date']}" if c["end_date"] else "")
    col2.metric("Période", f"{period} ({c['date_confidence']})")
    col3.metric("Type", CAMPAIGN_TYPE_LABELS.get(c["campaign_type"], c["campaign_type"]))

    if c["target_fiches"]:
        st.caption("Fiches ciblées : " + ", ".join(c["target_fiches"]))
    if c["notes"]:
        st.caption(f"Notes : {c['notes']}")

    st.divider()

    if c["status"] == "not_scorable":
        reason = NOT_SCORABLE_REASON_LABELS.get(c["not_scorable_reason"], c["not_scorable_reason"])
        st.warning(f"Non notable — {reason}")
        return

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Score final", c["final_score"])
    m2.metric("Anomalies rapprochées", c["anomaly_count"])
    m3.metric("Fiches touchées", c["fiches_touched"])
    m4.metric("Sous confusion saisonnière", c["seasonal_confound_count"])
    st.caption(
        f"Détail : score brut {c['raw_score']} × bonus de largeur {c['breadth_multiplier']} "
        f"= score final {c['final_score']}."
    )

    if not campaign_matches:
        st.caption("Aucune anomalie rapprochée dans la fenêtre d'attribution.")
        return

    st.subheader("Anomalies rapprochées")
    st.dataframe(matches_dataframe(campaign_matches), hide_index=True, width="stretch")


def render_comparison_tab(campaigns):
    scorable = [c for c in campaigns if c["status"] == "scorable"]
    not_scorable = [c for c in campaigns if c["status"] == "not_scorable"]
    stats = aggregate_stats(scorable)

    st.caption(
        f"Calculé sur {len(scorable)} campagnes notables (sur {len(campaigns)} cataloguées ; "
        f"{len(not_scorable)} non notables listées en bas de page). KBC et CBC sont la même "
        "banque (marque néerlandophone vs francophone du même groupe), regroupées en un camp "
        "\"KBC/CBC\" face à ING."
    )

    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure(go.Bar(
            x=["ING", "KBC/CBC"], y=[stats["ING"]["total_score"], stats["KBC+CBC"]["total_score"]],
            marker_color=[BANK_COLOR["ING"], BANK_COLOR["KBC"]],
        ))
        fig.update_layout(title="Score total", height=360, margin=dict(t=40, b=10, l=10, r=10))
        st.plotly_chart(fig, width="stretch")
    with col2:
        fig = go.Figure(go.Bar(
            x=["ING", "KBC/CBC"], y=[stats["ING"]["avg_score"], stats["KBC+CBC"]["avg_score"]],
            marker_color=[BANK_COLOR["ING"], BANK_COLOR["KBC"]],
        ))
        fig.update_layout(title="Score moyen par campagne", height=360, margin=dict(t=40, b=10, l=10, r=10))
        st.plotly_chart(fig, width="stretch")

    st.subheader("Vue par camp")
    camp_rows = [{
        "Camp": g, "Campagnes notables": stats[g]["total"], "Score total": stats[g]["total_score"],
        "Score moyen": stats[g]["avg_score"], "Taux de succès": f"{stats[g]['success_rate']}%",
    } for g in ("KBC+CBC", "ING")]
    st.dataframe(pd.DataFrame(camp_rows), hide_index=True, width="stretch")

    st.subheader("Vue par banque (KBC et CBC détaillés séparément)")
    bank_rows = []
    for bank in BANK_ORDER:
        bank_campaigns = [c for c in scorable if c["bank"] == bank]
        total = len(bank_campaigns)
        total_score = round(sum(c["final_score"] for c in bank_campaigns), 3)
        with_match = sum(1 for c in bank_campaigns if c["anomaly_count"] > 0)
        bank_rows.append({
            "Banque": bank, "Campagnes notables": total, "Score total": total_score,
            "Score moyen": round(total_score / total, 3) if total else None,
            "Taux de succès": f"{round(with_match / total * 100, 1)}%" if total else "-",
        })
    st.dataframe(pd.DataFrame(bank_rows), hide_index=True, width="stretch")

    st.subheader("Répartition par type de campagne")
    type_rows = [{
        "Camp": g, **{CAMPAIGN_TYPE_LABELS[k]: stats[g]["type_counts"].get(k, 0) for k in CAMPAIGN_TYPE_LABELS}
    } for g in ("KBC+CBC", "ING")]
    st.dataframe(pd.DataFrame(type_rows), hide_index=True, width="stretch")

    st.subheader("Classement des campagnes (toutes banques, notables uniquement)")
    ranked = sorted(scorable, key=lambda c: c["final_score"], reverse=True)
    rank_rows = [{
        "#": i + 1, "Banque": c["bank"], "Campagne": c["name"],
        "Type": CAMPAIGN_TYPE_LABELS.get(c["campaign_type"], c["campaign_type"]),
        "Anomalies": c["anomaly_count"], "Fiches touchées": c["fiches_touched"], "Score": c["final_score"],
    } for i, c in enumerate(ranked)]
    st.dataframe(pd.DataFrame(rank_rows), hide_index=True, width="stretch")

    st.subheader(f"Campagnes non notables ({len(not_scorable)})")
    if not_scorable:
        ns_rows = [{
            "Banque": c["bank"], "Campagne": c["name"], "Date": c["start_date"],
            "Raison": NOT_SCORABLE_REASON_LABELS.get(c["not_scorable_reason"], c["not_scorable_reason"]),
        } for c in not_scorable]
        st.dataframe(pd.DataFrame(ns_rows), hide_index=True, width="stretch")
    else:
        st.caption("Aucune.")


def main():
    st.title("Campagnes publicitaires vs impact Google Trends")
    st.caption(
        "Un onglet par campagne cataloguée (KBC, CBC, ING), avec les anomalies Trends "
        "rapprochées et le score d'efficacité calculé. Dernier onglet : comparatif agrégé "
        "ING vs KBC/CBC."
    )

    campaigns, matches = load_data()
    if not campaigns:
        st.error(
            "Aucune campagne trouvée. Lancez d'abord `python campaigns/load_campaigns.py` "
            "puis `python campaigns/scoring.py`."
        )
        st.stop()

    bank_rank = {b: i for i, b in enumerate(BANK_ORDER)}
    campaigns = sorted(campaigns, key=lambda c: (bank_rank.get(c["bank"], 99), c["start_date"]))

    tab_labels = [f"{c['bank']} · {c['name']}" for c in campaigns] + ["Comparatif ING vs KBC/CBC"]
    tabs = st.tabs(tab_labels)

    for tab, c in zip(tabs[:-1], campaigns):
        with tab:
            render_campaign_tab(c, matches.get(c["id"], []))

    with tabs[-1]:
        render_comparison_tab(campaigns)


if __name__ == "__main__":
    main()

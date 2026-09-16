"""Streamlit app: ING vs KBC vs CBC Google Trends benchmark, one tab per product sheet.

Reads trends_data and anomalies from SQLite. Both tables are populated by
separate pipeline steps (collectors/trends_collector.py,
analysis/anomaly_detection.py) and are only read here, so the UI stays fast.
Ad/campaign verification against the flagged anomalies is handled by a
separate downstream pipeline, out of scope here.
"""

import sqlite3

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from config import ANOMALY_TYPE_LABELS, DB_PATH, PRODUCTS, TERM_DISPLAY_LABELS

PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#c98500", "#e87ba4"]
ANOMALY_SYMBOLS = {"isolated_spike": "diamond", "sustained_trend": "star"}
BANK_DASH = {"KBC": "solid", "ING": "dash", "CBC": "dashdot"}

st.set_page_config(page_title="Benchmark ING KBC CBC", layout="wide")


def display_term(term):
    return TERM_DISPLAY_LABELS.get(term, term)


@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    try:
        trends = pd.read_sql_query("SELECT * FROM trends_data", conn, parse_dates=["date"])
        anomalies = pd.read_sql_query("SELECT * FROM anomalies", conn, parse_dates=["date"])
    finally:
        conn.close()
    return trends, anomalies


def build_chart(product, trends_df, anomalies_df):
    fig = go.Figure()
    pid = product["product_id"]

    for i, t in enumerate(product["terms"]):
        term, bank, lang = t["term"], t["bank"], t["language"]
        label = display_term(term)
        color = PALETTE[i % len(PALETTE)]
        dash = BANK_DASH.get(bank, "solid")

        series = trends_df[(trends_df["product_id"] == pid) & (trends_df["term"] == term)].sort_values("date")
        fig.add_trace(go.Scatter(
            x=series["date"], y=series["value"], mode="lines",
            name=f"{label} ({bank} · {lang.upper()})",
            line=dict(color=color, width=2, dash=dash),
            hovertemplate=f"<b>{label}</b><br>{bank} · {lang.upper()}<br>%{{x|%b %Y}}: %{{y}}<extra></extra>",
        ))

        term_anomalies = anomalies_df[(anomalies_df["product_id"] == pid) & (anomalies_df["term"] == term)]
        for atype, symbol in ANOMALY_SYMBOLS.items():
            sub = term_anomalies[term_anomalies["anomaly_type"] == atype]
            if sub.empty:
                continue
            fig.add_trace(go.Scatter(
                x=sub["date"], y=sub["value"], mode="markers",
                marker=dict(symbol=symbol, size=12, color=color, line=dict(color="#1a1a1a", width=1.2)),
                showlegend=False,
                hovertemplate=(
                    f"<b>{label}</b><br>{ANOMALY_TYPE_LABELS[atype]}"
                    "<br>%{x|%b %Y}: %{y}<extra></extra>"
                ),
            ))

    # Legend proxies explaining the anomaly marker symbols.
    for atype, symbol in ANOMALY_SYMBOLS.items():
        fig.add_trace(go.Scatter(
            x=[None], y=[None], mode="markers",
            marker=dict(symbol=symbol, size=12, color="#8c8d8a", line=dict(color="#1a1a1a", width=1.2)),
            name=ANOMALY_TYPE_LABELS[atype],
        ))

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Intérêt de recherche (0-100)",
        legend=dict(orientation="h", yanchor="top", y=-0.18),
        height=440,
        margin=dict(t=20, b=10, l=10, r=10),
    )
    return fig


def render_anomalies_table(product, anomalies_df):
    pid = product["product_id"]
    subset = anomalies_df[anomalies_df["product_id"] == pid].sort_values("date").copy()
    if subset.empty:
        st.caption("Aucune anomalie détectée pour cette fiche.")
        return

    subset["date"] = subset["date"].dt.strftime("%Y-%m-%d")
    subset["anomaly_type"] = subset["anomaly_type"].map(ANOMALY_TYPE_LABELS)
    subset["term"] = subset["term"].map(display_term)
    subset = subset.rename(columns={
        "term": "Terme", "bank": "Banque", "date": "Date",
        "value": "Valeur", "anomaly_type": "Type d'anomalie",
        "deviation_score": "Score de déviation",
    })
    st.dataframe(
        subset[["Terme", "Banque", "Date", "Valeur", "Type d'anomalie", "Score de déviation"]],
        width="stretch", hide_index=True,
    )


def render_raw_data(product, trends_df):
    pid = product["product_id"]
    subset = trends_df[trends_df["product_id"] == pid].sort_values("date")
    if subset.empty:
        st.caption("Aucune donnée disponible pour cette fiche.")
        return

    term_options = [t["term"] for t in product["terms"]]
    selected_terms = st.multiselect(
        "Termes", term_options, default=term_options, format_func=display_term, key=f"terms_{pid}",
    )
    min_date, max_date = subset["date"].min().date(), subset["date"].max().date()
    date_range = st.date_input(
        "Période", value=(min_date, max_date), min_value=min_date, max_value=max_date, key=f"dates_{pid}",
    )

    filtered = subset[subset["term"].isin(selected_terms)]
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start, end = date_range
        filtered = filtered[(filtered["date"].dt.date >= start) & (filtered["date"].dt.date <= end)]

    display = filtered.copy()
    display["term"] = display["term"].map(display_term)
    display = display.rename(columns={
        "term": "Terme", "bank": "Banque", "language": "Langue",
        "date": "Date", "value": "Valeur",
    })
    display["Date"] = display["Date"].dt.strftime("%Y-%m-%d")
    st.dataframe(
        display[["Terme", "Banque", "Langue", "Date", "Valeur"]],
        width="stretch", hide_index=True,
    )


def render_product_tab(product, trends_df, anomalies_df):
    st.plotly_chart(build_chart(product, trends_df, anomalies_df), width="stretch")
    st.subheader("Anomalies détectées")
    render_anomalies_table(product, anomalies_df)
    st.subheader("Données brutes")
    render_raw_data(product, trends_df)


def main():
    st.title("Benchmark marketing ING · KBC · CBC")
    st.caption(
        "Intérêt de recherche Google Trends (Belgique, 5 dernières années) par fiche produit — "
        "les anomalies marquées ici sont les périodes où l'intérêt de recherche d'un produit a été "
        "anormalement élevé. La vérification de leur origine (publicité, campagne) se fait dans un "
        "autre pipeline, alimenté par les exports de ce projet."
    )

    trends_df, anomalies_df = load_data()
    if trends_df.empty:
        st.error(
            "Aucune donnée trouvée. Lancez d'abord `python collectors/trends_collector.py` "
            "puis `python analysis/anomaly_detection.py`."
        )
        st.stop()

    tabs = st.tabs([p["product_label"] for p in PRODUCTS])
    for tab, product in zip(tabs, PRODUCTS):
        with tab:
            render_product_tab(product, trends_df, anomalies_df)


if __name__ == "__main__":
    main()

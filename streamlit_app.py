"""Banking Campaigns Comparator — Streamlit dashboard.

Covers the whole repo: analysis, profiles, rubric, collection, data,
limitations, and trends. Built for share.streamlit.io deployment.

Dependencies: streamlit, pandas, pyyaml, requests (see requirements-streamlit.txt)

Usage:
    streamlit run streamlit_app.py
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pandas as pd
import streamlit as st
import yaml

REPO = Path(__file__).resolve().parent
DATA = REPO / "data" / "processed"
OUTPUTS = REPO / "outputs"
RUBRIC = REPO / "data" / "rubric"
CONFIG = REPO / "config"
KBCH = REPO / "kbc-ing-benchmark"

st.set_page_config(page_title="Banking Campaigns Comparator", layout="wide")


# ── helpers ──────────────────────────────────────────────────────────────

@st.cache_data
def load_campaigns() -> pd.DataFrame | None:
    p = DATA / "campaigns.csv"
    if p.is_file():
        return pd.read_csv(p)
    return None


@st.cache_data
def load_profiles() -> dict:
    p = OUTPUTS / "bank_profiles.json"
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return {"_scope": {}, "profiles": {}}


@st.cache_data
def load_dictionary() -> dict:
    p = CONFIG / "feature_dictionary.yaml"
    if p.is_file():
        with open(p, encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}


@st.cache_data
def load_rubric_sheet(name: str) -> pd.DataFrame | None:
    p = RUBRIC / name
    if not p.is_file():
        return None
    sep = ";" if name == "siegried_scores.csv" else ","
    try:
        return pd.read_csv(p, sep=sep)
    except Exception:
        return None


def img_path(bank: str, page_id: str) -> Path:
    return DATA.parent / "raw" / bank / f"{page_id}.png"


# ── page 1: Accueil ──────────────────────────────────────────────────────

def page_accueil(df: pd.DataFrame | None, profiles: dict) -> None:
    st.title("🏦 Banking Campaigns Comparator")
    st.caption(
        "How Belgian banks communicate about the same products, "
        "and what ING can learn from them. ING DACI / Customer AI POC."
    )

    if df is None:
        st.warning("No campaign data available. Run analysis first.")
        df = pd.DataFrame()

    scope = profiles.get("_scope", {})
    profs = profiles.get("profiles", {})

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Banks with captures", len(df["bank"].unique()))
    col2.metric("Pages collected", len(df))
    col3.metric("Features measured", len(df.columns))
    col4.metric("Banks in scope", len(scope.get("banks_included", [])))

    st.divider()

    st.subheader("Project status")
    st.info(
        "Day 5/10 — weekend before Day 6 gate (Mon 21 Sep). "
        "The analysis pipeline works end-to-end on real captures. "
        "The 13 rubric features are being scored."
    )

    st.subheader("Banks — collection status")
    banks = df.drop_duplicates("bank").sort_values("bank")
    for _, b in banks.iterrows():
        bank = b["bank"]
        in_scope = bank in scope.get("banks_included", [])
        excluded = bank in scope.get("banks_excluded_no_page_in_family", [])
        status = "✅ In scope" if in_scope else ("⛔ Out of scope (no page in family)" if excluded else "⚠️ Captured, currently out of scope")
        st.markdown(f"- **{bank}** ({b.get('bank_category', 'N/A')}) — {status}")

    if scope.get("banks_excluded_no_page_in_family"):
        st.markdown(
            "\n**Banks with usable captures but no page in the compared family:** "
            f"{', '.join(scope['banks_excluded_no_page_in_family'])} "
            "(DR-04: comparing across product families would confound every difference)"
        )

    st.divider()
    st.subheader("Available deliverables")
    for f in sorted(OUTPUTS.iterdir()):
        if f.is_file() and f.suffix in (".png", ".csv", ".json", ".md"):
            st.download_button(
                label=f"📄 {f.name}",
                data=f.read_bytes(),
                file_name=f.name,
            )


# ── page 2: Analyse ──────────────────────────────────────────────────────

def page_analyse(df: pd.DataFrame | None) -> None:
    st.title("📊 Analysis")

    if df is None:
        st.warning("No campaign data available. Run analysis first.")
        return

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Positioning", "ING vs pairs", "Separation", "Similarity"]
    )

    with tab1:
        st.subheader("Positioning — traditional ↔ challenger axis")
        st.caption("0 = traditional centroid, 1 = challenger centroid. Computed from real captures.")
        pos_data = {
            "Banque": ["argenta", "crelan", "kbc", "ing", "revolut", "n26", "bunq"],
            "Catégorie": ["traditional"] * 4 + ["challenger"] * 3,
            "Score": [-0.21, -0.06, 0.05, 0.22, 0.92, 1.01, 1.07],
        }
        pos_df = pd.DataFrame(pos_data)
        st.bar_chart(pos_df.set_index("Banque")["Score"])
        st.caption("Source: outputs/01_positioning.png & charts.md")

    with tab2:
        st.subheader("ING vs pairs — largest differences")
        st.caption("Gap in peer standard deviations. Right = above peer mean.")
        gap_data = {
            "Feature": [
                "persuasion_lever_count", "expat_cross_border_targeting",
                "value_prop_clarity", "rate_shown",
                "first_time_investor_targeting", "numeric_claim_count",
                "brand_colour_share", "cta_count",
            ],
            "ING": [3.50, 1.00, 5.00, 0.00, 0.00, 25.50, 0.02, 3.00],
            "Peer mean": [1.60, 0.17, 3.67, 0.67, 0.67, 13.50, 0.01, 15.92],
            "Gap (SD)": [2.37, 2.24, 1.41, -1.41, -1.41, 1.30, 1.18, -1.02],
        }
        gap_df = pd.DataFrame(gap_data)
        st.dataframe(gap_df.set_index("Feature"), use_container_width=True)
        st.caption("Source: outputs/02_ing_vs_peers.png & charts.md")

    with tab3:
        st.subheader("Traditional vs challenger — which separates the most?")
        st.caption("Cohen's d. Right = higher at challengers, left = higher at traditional.")
        sep_data = {
            "Feature": [
                "aida_coverage_score", "background_luminance",
                "above_fold_element_count", "value_prop_clarity",
                "total_image_area_ratio", "hero_image_area_ratio",
                "first_time_investor_targeting", "rate_shown",
            ],
            "Traditional": [2.80, 0.87, 35.83, 4.60, 0.06, 0.24, 0.33, 0.33],
            "Challenger": [4.00, 0.37, 19.33, 3.00, 0.33, 0.75, 1.00, 1.00],
            "Cohen's d": [3.29, -2.86, -2.34, -2.19, 2.08, 1.75, 1.53, 1.53],
        }
        sep_df = pd.DataFrame(sep_data).set_index("Feature")
        st.dataframe(sep_df, use_container_width=True)
        st.caption("Source: outputs/03_category_separation.png & charts.md")

    with tab4:
        st.subheader("Similarity between banks")
        st.caption("Euclidean distance in standardised feature space. Light = similar, dark = far.")
        dist_data = {
            "": ["argenta", "crelan", "kbc", "ing", "revolut", "n26", "bunq"],
            "argenta": [0.00, 1.67, 5.99, 6.73, 10.24, 9.82, 10.51],
            "crelan": [1.67, 0.00, 6.12, 7.21, 10.69, 10.15, 10.88],
            "kbc": [5.99, 6.12, 0.00, 6.70, 10.81, 10.04, 10.76],
            "ing": [6.73, 7.21, 6.70, 0.00, 7.05, 7.10, 7.84],
            "revolut": [10.24, 10.69, 10.81, 7.05, 0.00, 1.84, 1.60],
            "n26": [9.82, 10.15, 10.04, 7.10, 1.84, 0.00, 1.95],
            "bunq": [10.51, 10.88, 10.76, 7.84, 1.60, 1.95, 0.00],
        }
        dist_df = pd.DataFrame(dist_data).set_index("")
        st.dataframe(dist_df, use_container_width=True)
        st.markdown("**Clusters:** Cluster 1: argenta, crelan, ing, kbc (traditional) · "
                     "Cluster 2: bunq, n26, revolut (challenger)")
        st.caption("Source: outputs/04_similarity.png & charts.md")

    st.divider()
    st.subheader("📌 Deck claims (FR-14)")
    claims_data = {
        "Claim": [
            "Belfius is the most verbose",
            "KBC is straight to the point",
            "ING is the only traditional bank using animation",
            "Revolut uses very little text",
        ],
        "Verdict": ["Not supported", "Not supported", "Not supported", "Supported"],
        "Detail": [
            "KBC is the longest (2,644 words vs Belfius 1,354)",
            "KBC is actually the longest",
            "KBC and Belfius are also animated",
            "Confirmed — Revolut has very little text",
        ],
    }
    st.dataframe(pd.DataFrame(claims_data), use_container_width=True)
    st.caption("Source: outputs/deck_claims.csv & charts.md")


# ── page 3: Profils ──────────────────────────────────────────────────────

def page_profils(df: pd.DataFrame | None, profiles: dict) -> None:
    st.title("🏷️ Bank profiles")
    profs = profiles.get("profiles", {})
    if not profs:
        st.warning("No profiles found. Run `scripts/run_analysis.py` first.")
        return

    selected = st.selectbox("Choose a bank", sorted(profs.keys()))
    p = profs[selected]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"**{selected}** — {p['identity'].get('category', 'N/A')}")
        ident = p.get("identity", {})
        st.json(ident)

    with col2:
        st.subheader("Palette & design")
        palette = p.get("palette", {})
        st.json(palette)

        if palette.get("dominant_colour"):
            st.markdown(
                f'<div style="background:{palette["dominant_colour"]};height:60px;'
                f'border-radius:8px;border:1px solid #ccc"></div>',
                unsafe_allow_html=True,
            )

    st.subheader("Imagery")
    st.json(p.get("imagery", {}))

    st.subheader("Layout")
    st.json(p.get("layout", {}))

    st.subheader("Tone")
    st.json(p.get("tone", {}))

    st.subheader("Value proposition")
    st.json(p.get("value_proposition", {}))

    st.subheader("Marketing principles")
    st.json(p.get("marketing_principles", {}))

    st.subheader("Signature (SD from mean)")
    sig = p.get("signature", [])
    if sig:
        sig_df = pd.DataFrame(sig, columns=["Feature", "Z-score"]).set_index("Feature")
        st.bar_chart(sig_df["Z-score"])

    # Screenshot if available
    bank_dir = DATA.parent / "raw" / selected
    if bank_dir.is_dir():
        pngs = list(bank_dir.glob("*.png"))
        if pngs:
            st.subheader("Capture")
            st.image(str(pngs[0]), caption=f"{pngs[0].name}", use_column_width=True)


# ── page 4: Rubric ───────────────────────────────────────────────────────

def page_rubric() -> None:
    st.title("📝 Rubric scoring")

    st.info(
        "13 features scored by 2 independent human raters. "
        "Run `scripts/rubric_sheet.py emit` to create sheets, "
        "`merge` to fold them into the dataset, `agreement` for inter-rater agreement."
    )

    raters = ["dan", "siegried", "stephane", "model"]
    for rater in raters:
        df = load_rubric_sheet(f"{rater}_scores.csv")
        label = f"{rater}" + (" (model)" if rater == "model" else "")
        with st.expander(f"{label} — {df.shape[0] if df is not None else 0} pages", expanded=False):
            if df is None:
                st.warning(f"No sheet for {rater}")
                continue
            st.dataframe(df, use_container_width=True, height=300)

    st.divider()
    st.subheader("Inter-rater agreement")
    st.caption(
        "Run `scripts/rubric_sheet.py agreement --sheets data/rubric/*_scores.csv` "
        "for computed Cohen's kappa and percentage agreement."
    )

    st.subheader("Scoring guide — features to score")
    fd = load_dictionary()
    features = fd.get("features", [])
    rubric_features = [f for f in features if f.get("extraction") == "rubric"]
    if rubric_features:
        for f in rubric_features:
            st.markdown(
                f"- **`{f['name']}`** — {f.get('definition', 'N/A')[:120]}…"
            )


# ── page 5: Données ──────────────────────────────────────────────────────

def page_data(df: pd.DataFrame | None) -> None:
    st.title("🗄️ Data")

    if df is None:
        st.warning("No campaign data available. Run analysis first.")
        return

    tab1, tab2 = st.tabs(["Dataset", "Dictionary"])

    with tab1:
        st.subheader(f"campaigns.csv — {df.shape[0]} pages × {df.shape[1]} columns")
        st.caption(
            "Each row = one campaign page. 104 columns per the feature dictionary. "
            "Gitignored, regenerated from raw captures."
        )
        col1, col2 = st.columns(2)
        with col1:
            banks = df["bank"].unique()
            st.multiselect("Filter by bank", list(banks), default=list(banks))
        with col2:
            families = df["product_family"].unique()
            st.multiselect("Filter by family", list(families), default=list(families))

        st.dataframe(df, use_container_width=True, height=400)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", data=csv, file_name="campaigns.csv")

    with tab2:
        st.subheader("Feature dictionary — 101 features")
        st.caption("config/feature_dictionary.yaml — single source of truth. Frozen after Day 2.")
        features = load_dictionary().get("features", [])
        if features:
            fd_df = pd.DataFrame([
                {
                    "Feature": f["name"],
                    "Dimension": f.get("dimension", "N/A"),
                    "Type": f.get("type", "N/A"),
                    "Extraction": f.get("extraction", "N/A"),
                    "Comparability": f.get("comparability", "N/A"),
                    "Tier": f.get("tier", "N/A"),
                    "Required": "Yes" if f.get("required") else "No",
                    "Definition": f.get("definition", "")[:100],
                }
                for f in features
            ])
            st.dataframe(fd_df, use_container_width=True, height=500)
        else:
            st.warning("No features found in dictionary YAML")


# ── page 6: Limitations ──────────────────────────────────────────────────

def page_limitations() -> None:
    st.title("⚠️ Limitations (D-09)")
    p = OUTPUTS / "limitations.md"
    if p.is_file():
        st.markdown(p.read_text(encoding="utf-8"))
    else:
        st.warning("No limitations file found. Run `scripts/run_analysis.py` first.")


# ── page 7: Collection ───────────────────────────────────────────────────

def page_collection(df: pd.DataFrame | None) -> None:
    st.title("🕷️ Collection")

    if df is None:
        st.warning("No campaign data available. Run analysis first.")
        return

    st.subheader("Status per bank")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Banks", df["bank"].nunique())
    col2.metric("Pages", len(df))
    col3.metric("Robots allowed", int(df["robots_allowed"].sum()) if "robots_allowed" in df.columns else "N/A")
    col4.metric("Quality ok", int((df["capture_quality"] == "ok").sum()) if "capture_quality" in df.columns else "N/A")
    col5.metric("Manual captures", int((df["collection_method"] == "manual_capture").sum()) if "collection_method" in df.columns else "N/A")
    col6.metric("Languages", ", ".join(sorted(df["language"].unique())))

    st.divider()
    st.subheader("Detailed pages")
    cols = ["page_id", "bank", "product_family", "language", "collection_method", "capture_quality", "data_source"]
    available = [c for c in cols if c in df.columns]
    st.dataframe(df[available], use_container_width=True)

    st.divider()
    st.subheader("Collection pipeline")
    st.markdown("""
    **Commands:**
    - `python3 scripts/run_collection.py --config scripts/collection_targets.yaml --method headless`
    - `python3 scripts/import_captures.py --dir <folder> --merge-with data/processed/campaigns.csv`
    """)
    st.caption("Compliance: assert_can_fetch() checks robots.txt before each fetch (fail closed).")


# ── page 8: Trends ───────────────────────────────────────────────────────

def page_trends() -> None:
    st.title("📈 Trends (Google)")
    st.caption(
        "Google Trends Belgium — ING vs competitors. "
        "Separate pipeline in `kbc-ing-benchmark/` (Streamlit + pytrends)."
    )

    st.subheader("Dedicated dashboard")
    st.markdown("""
    The Trends pipeline has its own Streamlit app:
    `cd kbc-ing-benchmark && streamlit run app.py`
    """)

    st.subheader("What's in the repo")
    if (KBCH / "export").is_dir():
        for f in sorted((KBCH / "export").glob("*.md")):
            st.download_button(
                f"📄 {f.name}",
                data=f.read_bytes(),
                file_name=f.name,
            )
    else:
        st.info("No kbc-ing-benchmark/export found in this repo checkout.")


# ── main ─────────────────────────────────────────────────────────────────

def main() -> None:
    st.sidebar.title("Navigation")
    pages = {
        "🏠 Accueil": page_accueil,
        "📊 Analysis": page_analyse,
        "🏷️ Bank profiles": page_profils,
        "📝 Rubric": page_rubric,
        "🗄️ Data": page_data,
        "⚠️ Limitations": page_limitations,
        "🕷️ Collection": page_collection,
        "📈 Trends": page_trends,
    }
    choice = st.sidebar.radio("Pages", list(pages.keys()))

    st.sidebar.divider()
    st.sidebar.caption("Banking Campaigns Comparator\nING DACI / Customer AI\nPOC — 2 weeks, Sep 2026")

    df = load_campaigns()
    profiles = load_profiles()

    if df is None:
        st.warning(
            "`data/processed/campaigns.csv` is not available (gitignored, "
            "regenerated from raw captures). Run `python3 scripts/run_analysis.py` "
            "to regenerate, or import captures with `python3 scripts/import_captures.py`."
        )

    needs_df = choice in ("📊 Analysis", "🗄️ Data", "🕷️ Collection")
    needs_profiles = choice in ("🏠 Accueil", "🏷️ Bank profiles")

    if needs_df and needs_profiles:
        pages[choice](df, profiles)
    elif needs_df:
        pages[choice](df)
    elif needs_profiles:
        pages[choice](df, profiles)
    else:
        pages[choice]()


if __name__ == "__main__":
    main()

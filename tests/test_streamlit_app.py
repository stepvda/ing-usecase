"""The two figures the dashboard got wrong, pinned.

streamlit is an optional dependency (requirements-streamlit.txt, not
requirements.txt), so these skip cleanly in CI the same way test_geo_trends.py
does for pytrends.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

pytest.importorskip("streamlit")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

import streamlit_app  # noqa: E402

FAMILY = "current_account_pack"


@pytest.fixture(scope="module")
def dataset():
    df = streamlit_app.load_campaigns()
    if df is None:
        pytest.skip("no dataset in the working tree")
    return df


def test_no_data_reports_nothing_rather_than_zero():
    """A missing dataset is not a dataset with no features in it."""
    assert streamlit_app.features_compared(None, FAMILY) is None


def test_the_headline_figure_is_the_one_every_other_artefact_quotes(dataset):
    """Regression: this read 89 - the width of the unscored CSV.

    outputs/charts.md prints "104 features in the dictionary" and
    "= 33 features used in this comparison" from the same feature_accounting()
    call. The dashboard must not invent a third number for the same run.
    """
    declared, used = streamlit_app.features_compared(dataset, FAMILY)
    assert declared == 104
    assert used == 33
    assert used != len(dataset.columns), "the metric is counting CSV columns again"


def test_the_count_is_scoped_to_one_product_family(dataset):
    """DR-04: a comparison is only valid inside one family, and the count
    follows it. Pooled across all six the figure is different, and quoting the
    pooled one beside a scoped chart is how two numbers start disagreeing."""
    _, scoped = streamlit_app.features_compared(dataset, FAMILY)
    _, pooled = streamlit_app.features_compared(dataset, None)
    assert scoped != pooled
    assert scoped == 33


def test_it_never_reports_more_features_than_the_dictionary_declares(dataset):
    declared, used = streamlit_app.features_compared(dataset, FAMILY)
    assert used <= declared


def test_load_campaigns_prefers_the_rubric_merged_dataset(tmp_path, monkeypatch):
    """campaigns.csv lacks the 13 judged features; campaigns_scored.csv has them.

    Reading the unscored file is what hid every rubric-derived figure from this
    dashboard while the React UI showed it.
    """
    pd.DataFrame({"page_id": ["scored"]}).to_csv(tmp_path / "campaigns_scored.csv", index=False)
    pd.DataFrame({"page_id": ["unscored"]}).to_csv(tmp_path / "campaigns.csv", index=False)
    monkeypatch.setattr(streamlit_app, "DATA", tmp_path)
    streamlit_app.load_campaigns.clear()

    assert streamlit_app.load_campaigns()["page_id"].iat[0] == "scored"


def test_load_campaigns_falls_back_when_only_the_unscored_file_exists(tmp_path, monkeypatch):
    """A tree part-way through the pipeline still shows what it has."""
    pd.DataFrame({"page_id": ["unscored"]}).to_csv(tmp_path / "campaigns.csv", index=False)
    monkeypatch.setattr(streamlit_app, "DATA", tmp_path)
    streamlit_app.load_campaigns.clear()

    assert streamlit_app.load_campaigns()["page_id"].iat[0] == "unscored"


def test_load_campaigns_returns_none_when_there_is_nothing(tmp_path, monkeypatch):
    monkeypatch.setattr(streamlit_app, "DATA", tmp_path)
    streamlit_app.load_campaigns.clear()

    assert streamlit_app.load_campaigns() is None

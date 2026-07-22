"""Dashboard — raw quarter tables + calculated variances, toggle between Q1 and Q2."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

# Make the backend services package importable.
ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from services.data import get_store  # noqa: E402


# ---------------------------------------------------------------- helpers
def _usd(n) -> str:
    return f"${float(n):,.0f}"


def _pct(n) -> str:
    v = float(n)
    return f"{'+' if v > 0 else ''}{v:.1f}%"


def _tone(v) -> str:
    return "bad" if float(v) > 0 else "good"


def _kpi_cards(totals: dict) -> None:
    st.markdown(
        f"""
<div class="kpi-row">
  <div class="kpi">
    <div class="kpi-label">Total budget</div>
    <div class="kpi-value">{_usd(totals['budget'])}</div>
    <div class="kpi-sub">Planned spend</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Total actual</div>
    <div class="kpi-value">{_usd(totals['actual'])}</div>
    <div class="kpi-sub">Recorded spend</div>
  </div>
  <div class="kpi {_tone(totals['variance'])}">
    <div class="kpi-label">Total variance</div>
    <div class="kpi-value">{_usd(totals['variance'])}</div>
    <div class="kpi-sub">{_pct(totals['variance_pct'])} vs budget</div>
  </div>
</div>
        """,
        unsafe_allow_html=True,
    )


def _category_table(store, quarter: str) -> None:
    rows = ""
    for c in store.aggregate_by_category(quarter):
        rows += (
            f'<tr><td>{c["category"]}</td>'
            f'<td>{_usd(c["budget"])}</td>'
            f'<td>{_usd(c["actual"])}</td>'
            f'<td class="{_tone(c["variance"])}">{_usd(c["variance"])} ({_pct(c["variance_pct"])})</td></tr>'
        )
    st.markdown(
        '<table class="dg-table"><thead><tr>'
        '<th>Category</th><th>Budget</th><th>Actual</th><th>Variance</th>'
        f'</tr></thead><tbody>{rows}</tbody></table>',
        unsafe_allow_html=True,
    )


def _line_item_table(store, quarter: str) -> None:
    records = sorted(store.filter(quarter=quarter), key=lambda r: r.variance, reverse=True)
    rows = ""
    for r in records:
        rows += (
            f'<tr><td>{r.department}</td><td>{r.category}</td>'
            f'<td>{_usd(r.budget)}</td><td>{_usd(r.actual)}</td>'
            f'<td class="{_tone(r.variance)}">{_usd(r.variance)} ({_pct(r.variance_pct)})</td></tr>'
        )
    st.markdown(
        f'<div style="max-height:460px;overflow:auto;">'
        '<table class="dg-table"><thead><tr>'
        '<th>Department</th><th>Category</th><th>Budget</th><th>Actual</th><th>Variance</th>'
        f'</tr></thead><tbody>{rows}</tbody></table></div>'
        f'<div class="source-tag">{len(records)} line items · source: {quarter.lower()}.csv</div>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------- page
def render_dashboard() -> None:
    store = get_store()
    quarters = store.quarters()

    st.markdown(
        """
<div class="demo-head">
  <div class="demo-eyebrow">Finance Data</div>
  <div class="demo-title">The <em>dashboard</em> the analyst reads</div>
  <div class="demo-sub">
    The raw budget-vs-actual tables and the variances computed from them.
    Toggle between quarters to compare.
  </div>
</div>
        """,
        unsafe_allow_html=True,
    )

    if "dash_quarter" not in st.session_state or st.session_state.dash_quarter not in quarters:
        st.session_state.dash_quarter = quarters[-1] if quarters else "Q2"

    quarter = st.radio(
        "Quarter",
        options=quarters,
        index=quarters.index(st.session_state.dash_quarter),
        horizontal=True,
        label_visibility="collapsed",
        key="dash_quarter",
    )

    totals = store.quarter_totals(quarter)
    _kpi_cards(totals)

    st.markdown('<div class="console-label">Variance by category</div>', unsafe_allow_html=True)
    _category_table(store, quarter)

    st.markdown('<div class="console-label">Line-item detail</div>', unsafe_allow_html=True)
    _line_item_table(store, quarter)

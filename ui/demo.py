"""Demo — FastAPI-style console → pipeline → result, wired to backend services.

Flow mirrors the FastAPI frontend:
  prompt/chip → animated agent pipeline → KPI cards + department table
  + slide outline → downloadable .pptx (built by services.pptx_builder.build_pptx).
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import streamlit as st

# Make the FastAPI backend services importable.
ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from services.data import get_store  # noqa: E402
from services.narrative import build_narrative  # noqa: E402
from services.pptx_builder import build_pptx  # noqa: E402
from services.prompt_parser import parse_prompt  # noqa: E402

PPTX_MIME = "application/vnd.openxmlformats-officedocument.presentationml.presentation"

# (chip label, full prompt sent to the agent)
SUGGESTIONS = [
    ("Q2 infrastructure overrun", "Generate a 4-slide deck explaining our Q2 software infrastructure overrun for HQ"),
    ("Cloud compute spike", "Create an executive deck on our Q2 cloud compute cost spike"),
    ("Q1 vs Q2 review", "Summarize Q1 vs Q2 budget vs actual performance for leadership"),
]

PIPELINE = [
    "Parsing your request",
    "Querying enterprise finance database",
    "Calculating budget vs. actual variances",
    "Running financial strategy analysis",
    "Synthesizing executive narrative",
    "Generating PowerPoint deck",
]


# ---------------------------------------------------------------- helpers
def _usd(n) -> str:
    return f"${float(n):,.0f}"


def _pct(n) -> str:
    v = float(n)
    return f"{'+' if v > 0 else ''}{v:.1f}%"


def _tone(v) -> str:
    return "bad" if float(v) > 0 else "good"


def _init_state() -> None:
    defaults = {
        "demo_phase": "idle",   # idle | working | done
        "pending_prompt": None,
        "demo_result": None,
        "demo_pptx": None,
        "demo_filename": None,
        "demo_error": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _animate_pipeline(holder) -> None:
    for i in range(len(PIPELINE) + 1):
        rows = ""
        for j, label in enumerate(PIPELINE):
            if j < i:
                cls, ico, tail = "agent-step done", "✓", ""
            elif j == i:
                cls, ico, tail = "agent-step active", "●", "…"
            else:
                cls, ico, tail = "agent-step", "○", ""
            rows += f'<div class="{cls}"><span class="ico">{ico}</span>{label}{tail}</div>'
        done = i >= len(PIPELINE)
        head = (
            'Analysis complete.'
            if done
            else '<span class="spinner"></span>DeckGen agent is working…'
        )
        holder.markdown(
            f'<div class="agent-panel"><div class="agent-head">{head}</div>{rows}</div>',
            unsafe_allow_html=True,
        )
        time.sleep(0.25 if i == 0 else 0.42)


def _run_agent(prompt: str):
    store = get_store()
    parsed = parse_prompt(prompt, store)
    narrative = build_narrative(store, parsed)
    result = {
        "quarter": parsed.quarter,
        "category": parsed.category,
        "source": narrative["meta"]["source"],
        "slides": narrative["slides"],
        "totals": store.quarter_totals(parsed.quarter),
        "detail": store.category_detail(parsed.quarter, parsed.category),
    }
    pptx_bytes = build_pptx(narrative, store, parsed.quarter)
    filename = f"deckgen-{parsed.quarter.lower()}-{parsed.category.lower().replace(' ', '-')}.pptx"
    return result, pptx_bytes, filename


def _render_result(r: dict, pptx_bytes: bytes, filename: str) -> None:
    t, f = r["totals"], r["detail"]

    st.markdown(
        f'<div class="result-bar"><span class="result-badge">Deck ready</span>'
        f'<span class="deck-title-label">{r["quarter"]} · {r["category"]}</span></div>',
        unsafe_allow_html=True,
    )

    a1, a2, _ = st.columns([1.3, 1, 2])
    with a1:
        st.download_button(
            "⬇ Download .pptx",
            data=pptx_bytes,
            file_name=filename,
            mime=PPTX_MIME,
            type="primary",
            use_container_width=True,
        )
    with a2:
        if st.button("↺ New request", use_container_width=True):
            st.session_state.demo_phase = "idle"
            st.session_state.demo_result = None
            st.session_state.demo_pptx = None
            st.session_state.demo_filename = None
            st.rerun()

    # KPI cards
    st.markdown(
        f"""
<div class="kpi-row">
  <div class="kpi">
    <div class="kpi-label">Portfolio actual</div>
    <div class="kpi-value">{_usd(t['actual'])}</div>
    <div class="kpi-sub">vs {_usd(t['budget'])} budget</div>
  </div>
  <div class="kpi {_tone(t['variance'])}">
    <div class="kpi-label">Portfolio variance</div>
    <div class="kpi-value">{_usd(t['variance'])}</div>
    <div class="kpi-sub">{_pct(t['variance_pct'])}</div>
  </div>
  <div class="kpi {_tone(f['variance'])}">
    <div class="kpi-label">{r['category']}</div>
    <div class="kpi-value">{_usd(f['variance'])}</div>
    <div class="kpi-sub">{_pct(f['variance_pct'])} vs budget</div>
  </div>
</div>
        """,
        unsafe_allow_html=True,
    )

    # Department drill-down table
    rows = ""
    for d in f["by_department"][:5]:
        rows += (
            f'<tr><td>{d["department"]}</td><td>{_usd(d["budget"])}</td>'
            f'<td>{_usd(d["actual"])}</td>'
            f'<td class="{_tone(d["variance"])}">{_usd(d["variance"])} ({_pct(d["variance_pct"])})</td></tr>'
        )
    st.markdown(
        '<table class="dg-table"><thead><tr><th>Department</th><th>Budget</th>'
        f'<th>Actual</th><th>Variance</th></tr></thead><tbody>{rows}</tbody></table>',
        unsafe_allow_html=True,
    )

    # Slide outline
    items = ""
    for s in r["slides"]:
        sub = f'<span class="slide-sub">{s.get("subtitle", "")}</span>' if s.get("subtitle") else ""
        items += f'<li><strong>{s.get("title", "")}</strong>{sub}</li>'
    st.markdown(
        f'<div class="slide-outline"><h4>Generated deck · {len(r["slides"])} slides</h4>'
        f'<ol>{items}</ol></div>',
        unsafe_allow_html=True,
    )

    src = "AI-generated narrative" if r["source"] == "openai" else "Template narrative"
    st.markdown(f'<div class="source-tag">Narrative source: {src}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------- page
def render_demo() -> None:
    _init_state()

    st.markdown(
        """
<div class="demo-head">
  <div class="demo-eyebrow">Live Demo</div>
  <div class="demo-title">Ask for a deck. Get a <em>PowerPoint</em>.</div>
  <div class="demo-sub">
    Type a plain-English request. DeckGen AI queries the finance data, computes the
    variances, writes the narrative, and generates a downloadable .pptx.
  </div>
</div>
        """,
        unsafe_allow_html=True,
    )

    # --- Prompt console ---
    st.markdown('<div class="console-label">Your request</div>', unsafe_allow_html=True)
    st.text_area(
        "prompt",
        key="demo_prompt_box",
        height=90,
        label_visibility="collapsed",
        placeholder="e.g. Generate a 4-slide deck explaining our Q2 software infrastructure overrun for HQ",
    )

    gen_col, _ = st.columns([1, 2.4])
    with gen_col:
        if st.button("Generate Deck", type="primary", use_container_width=True):
            p = (st.session_state.demo_prompt_box or "").strip()
            if len(p) >= 8:
                st.session_state.pending_prompt = p
                st.session_state.demo_phase = "working"
                st.rerun()
            else:
                st.session_state.demo_error = "Please enter a more descriptive request (at least 8 characters)."

    st.markdown('<div class="chips-hint">Try one of these:</div>', unsafe_allow_html=True)
    chip_cols = st.columns(len(SUGGESTIONS))
    for i, (label, text) in enumerate(SUGGESTIONS):
        with chip_cols[i]:
            if st.button(label, key=f"chip_{i}", use_container_width=True):
                st.session_state.pending_prompt = text
                st.session_state.demo_phase = "working"
                st.rerun()

    if st.session_state.demo_error:
        st.error(st.session_state.demo_error)
        st.session_state.demo_error = None

    # --- Working: animate pipeline, then compute ---
    if st.session_state.demo_phase == "working":
        prompt = st.session_state.pending_prompt or ""
        holder = st.empty()
        _animate_pipeline(holder)
        try:
            result, pptx_bytes, filename = _run_agent(prompt)
            st.session_state.demo_result = result
            st.session_state.demo_pptx = pptx_bytes
            st.session_state.demo_filename = filename
            st.session_state.demo_phase = "done"
        except Exception as exc:  # noqa: BLE001
            st.session_state.demo_phase = "idle"
            st.session_state.demo_error = f"Something went wrong: {exc}"
        holder.empty()
        st.rerun()

    # --- Done: render result ---
    if st.session_state.demo_phase == "done" and st.session_state.demo_result:
        _render_result(
            st.session_state.demo_result,
            st.session_state.demo_pptx,
            st.session_state.demo_filename,
        )

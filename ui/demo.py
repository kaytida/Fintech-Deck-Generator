"""Demo — agent reviews the data first, then generates the deck on click.

Flow:
  prompt/chip → animated agent pipeline (queries the data via tool-calling) →
  on-screen REVIEW summary (headline + findings + KPIs + table + slide outline) →
  user clicks "Generate PowerPoint" → downloadable 5-6 slide .pptx.

The agent (services.agent) uses an OpenAI-compatible LLM (LLMFoundry) when a token
is configured; otherwise everything falls back to the deterministic template so the
deployed app never breaks.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import streamlit as st

# Make the backend services package importable.
ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from services.agent import llm_available, run_agent  # noqa: E402
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
        "demo_phase": "idle",   # idle | working | review | done
        "pending_prompt": None,
        "demo_review": None,
        "demo_pptx": None,
        "demo_filename": None,
        "demo_error": None,
        "demo_agent_note": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _ensure_llm_env() -> None:
    """Copy the LLM token/config from st.secrets into env at call time.

    This runs on every request so a token added to secrets.toml (or the Cloud
    Secrets UI) is picked up without depending on import order or app restart.
    """
    for k in ("LLMFOUNDRY_TOKEN", "LLMFOUNDRY_BASE_URL", "LLMFOUNDRY_MODEL", "OPENAI_API_KEY"):
        try:
            val = st.secrets.get(k)
        except Exception:
            val = None
        if val:
            os.environ[k] = str(val)


def _reset() -> None:
    st.session_state.demo_phase = "idle"
    st.session_state.demo_review = None
    st.session_state.demo_pptx = None
    st.session_state.demo_filename = None
    st.session_state.demo_agent_note = None


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
            'Reviewing the data…'
            if done
            else '<span class="spinner"></span>DeckGen agent is working…'
        )
        holder.markdown(
            f'<div class="agent-panel"><div class="agent-head">{head}</div>{rows}</div>',
            unsafe_allow_html=True,
        )
        time.sleep(0.25 if i == 0 else 0.4)


def _fallback_review(store, parsed) -> dict:
    """Deterministic review + slides when no LLM token is available."""
    narrative = build_narrative(store, parsed)
    totals = store.quarter_totals(parsed.quarter)
    focus = store.category_detail(parsed.quarter, parsed.category)
    review = [
        f"Portfolio actual {_usd(totals['actual'])} vs {_usd(totals['budget'])} budget "
        f"({_pct(totals['variance_pct'])}).",
        f"{parsed.category}: {_usd(focus['variance'])} variance ({_pct(focus['variance_pct'])}) vs plan.",
    ]
    top = store.top_overrun(parsed.quarter)
    if top:
        review.append(
            f"Largest overrun category: {top['category']} at {_usd(top['variance'])} "
            f"({_pct(top['variance_pct'])})."
        )
    return {
        "headline": f"{parsed.quarter} · {parsed.category}: {_usd(focus['variance'])} variance vs plan",
        "review": review,
        "quarter": parsed.quarter,
        "category": parsed.category,
        "slides": narrative["slides"],
        "source": narrative["meta"]["source"],
    }


def _run_review(prompt: str) -> dict:
    """Phase 1: agent (or fallback) queries data and produces a review summary."""
    store = get_store()
    parsed = parse_prompt(prompt, store)

    _ensure_llm_env()
    st.session_state.demo_agent_note = None

    payload = None
    if llm_available():
        try:
            payload = run_agent(prompt, store)
            payload["source"] = "agent"
        except Exception as exc:  # noqa: BLE001
            st.session_state.demo_agent_note = (
                f"Live agent failed → using template. Reason: {type(exc).__name__}: {str(exc)[:300]}"
            )
            payload = None
    else:
        st.session_state.demo_agent_note = (
            "No LLM token detected → using template. Add LLMFOUNDRY_TOKEN to "
            ".streamlit/secrets.toml (or the Cloud Secrets UI) and reload."
        )
    if payload is None:
        payload = _fallback_review(store, parsed)

    # Validate quarter/category against real data for the KPI cards + table.
    quarter = payload.get("quarter") if payload.get("quarter") in store.quarters() else parsed.quarter
    category = payload.get("category") if payload.get("category") in store.categories() else parsed.category

    payload["quarter"] = quarter
    payload["category"] = category
    payload["totals"] = store.quarter_totals(quarter)
    payload["detail"] = store.category_detail(quarter, category)
    payload.setdefault("headline", f"{quarter} · {category}")
    payload.setdefault("review", [])
    return payload


def _build_deck(review: dict):
    """Phase 2: turn the reviewed slides into a downloadable .pptx."""
    pptx_bytes = build_pptx({"slides": review["slides"]})
    q = review["quarter"].lower()
    c = review["category"].lower().replace(" ", "-").replace("&", "and")
    return pptx_bytes, f"deckgen-{q}-{c}.pptx"


# ---------------------------------------------------------------- render pieces
def _render_summary(r: dict) -> None:
    t, f = r["totals"], r["detail"]

    # Headline / review findings
    findings = "".join(f"<li>{b}</li>" for b in r.get("review", []))
    st.markdown(
        f'<div class="slide-outline"><h4>{r.get("headline", "")}</h4>'
        f'<ul style="margin:0;padding-left:1.2rem;color:#B4C2D6;">{findings}</ul></div>',
        unsafe_allow_html=True,
    )

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
    if rows:
        st.markdown(
            '<table class="dg-table"><thead><tr><th>Department</th><th>Budget</th>'
            f'<th>Actual</th><th>Variance</th></tr></thead><tbody>{rows}</tbody></table>',
            unsafe_allow_html=True,
        )

    # Slide outline (what the deck will contain)
    items = ""
    for s in r["slides"]:
        sub = f'<span class="slide-sub">{s.get("subtitle", "")}</span>' if s.get("subtitle") else ""
        items += f'<li><strong>{s.get("title", "")}</strong>{sub}</li>'
    st.markdown(
        f'<div class="slide-outline"><h4>Proposed deck · {len(r["slides"])} slides</h4>'
        f'<ol>{items}</ol></div>',
        unsafe_allow_html=True,
    )

    src = {"agent": "AI agent (live data)", "openai": "AI-generated narrative"}.get(
        r.get("source"), "Template narrative"
    )
    st.markdown(f'<div class="source-tag">Narrative source: {src}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------- page
def render_demo() -> None:
    _init_state()

    st.markdown(
        """
<div class="demo-head">
  <div class="demo-eyebrow">Live Demo</div>
  <div class="demo-title">Ask a question. Review it. Get a <em>PowerPoint</em>.</div>
  <div class="demo-sub">
    The agent queries the finance data and shows you a summary first. Like what you
    see? Generate a 5-6 slide, fully editable .pptx with one click.
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
        placeholder="e.g. Generate a deck explaining our Q2 software infrastructure overrun for HQ",
    )

    gen_col, _ = st.columns([1, 2.4])
    with gen_col:
        if st.button("Review the data →", type="primary", use_container_width=True):
            p = (st.session_state.demo_prompt_box or "").strip()
            if len(p) >= 8:
                st.session_state.pending_prompt = p
                _reset()
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
                _reset()
                st.session_state.demo_phase = "working"
                st.rerun()

    if st.session_state.demo_error:
        st.error(st.session_state.demo_error)
        st.session_state.demo_error = None

    # Show WHY the template was used (missing token / agent failure) on every result phase.
    if st.session_state.demo_agent_note and st.session_state.demo_phase in ("review", "done"):
        st.warning(st.session_state.demo_agent_note)

    # --- Working: animate pipeline, then run the review agent ---
    if st.session_state.demo_phase == "working":
        prompt = st.session_state.pending_prompt or ""
        holder = st.empty()
        _animate_pipeline(holder)
        try:
            with st.spinner("Agent is reviewing the finance data…"):
                st.session_state.demo_review = _run_review(prompt)
            st.session_state.demo_phase = "review"
        except Exception as exc:  # noqa: BLE001
            st.session_state.demo_phase = "idle"
            st.session_state.demo_error = f"Something went wrong: {exc}"
        holder.empty()
        st.rerun()

    # --- Review: show the summary, offer to generate the deck ---
    if st.session_state.demo_phase == "review" and st.session_state.demo_review:
        r = st.session_state.demo_review
        st.markdown(
            f'<div class="result-bar"><span class="result-badge" '
            f'style="background:rgba(56,189,248,0.14);color:#38BDF8;border-color:rgba(56,189,248,0.4);">'
            f'Review ready</span>'
            f'<span class="deck-title-label">{r["quarter"]} · {r["category"]}</span></div>',
            unsafe_allow_html=True,
        )
        _render_summary(r)

        b1, b2, _ = st.columns([1.5, 1, 1.6])
        with b1:
            if st.button(f"⬛ Generate PowerPoint · {len(r['slides'])} slides",
                         type="primary", use_container_width=True):
                try:
                    with st.spinner("Building your PowerPoint…"):
                        pptx_bytes, filename = _build_deck(r)
                    st.session_state.demo_pptx = pptx_bytes
                    st.session_state.demo_filename = filename
                    st.session_state.demo_phase = "done"
                except Exception as exc:  # noqa: BLE001
                    st.session_state.demo_error = f"Could not build the deck: {exc}"
                st.rerun()
        with b2:
            if st.button("↺ New request", use_container_width=True):
                _reset()
                st.rerun()

    # --- Done: deck built, offer download ---
    if st.session_state.demo_phase == "done" and st.session_state.demo_review:
        r = st.session_state.demo_review
        st.markdown(
            f'<div class="result-bar"><span class="result-badge">Deck ready</span>'
            f'<span class="deck-title-label">{r["quarter"]} · {r["category"]}</span></div>',
            unsafe_allow_html=True,
        )

        d1, d2, _ = st.columns([1.3, 1, 2])
        with d1:
            st.download_button(
                "⬇ Download .pptx",
                data=st.session_state.demo_pptx,
                file_name=st.session_state.demo_filename,
                mime=PPTX_MIME,
                type="primary",
                use_container_width=True,
            )
        with d2:
            if st.button("↺ New request", use_container_width=True):
                _reset()
                st.rerun()

        _render_summary(r)

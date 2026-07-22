"""Demo — chat UI with exploring animation, FAQ responses, upload, and 6-slide PPT."""

from __future__ import annotations

import base64
import sys
import time
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from ui.content import (
    FAQ_ITEMS,
    extract_upload_meta,
    get_exploring_lines,
    get_response,
    load_upload,
    summarize_upload,
)
from ui.deck_profiles import get_deck_context

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from services.pptx_builder import build_executive_deck  # noqa: E402

GREETING = "How can I help you with planning a deck?"
CHAT_PLACEHOLDER = "Ask about spend, variances, or request a deck…"
UPLOAD_PREFIX = "__upload__:"

PPT_STEPS = [
    "Building executive summary slide…",
    "Adding cost breakdown and waterfall…",
    "Packaging 6-slide PowerPoint…",
]


def _init_state() -> None:
    defaults = {
        "messages": [],
        "processing": False,
        "processing_mode": None,
        "active_prompt": None,
        "active_msg_idx": None,
        "auto_download": None,
        "show_upload": False,
        "upload_summary": None,
        "upload_meta": None,
        "scroll_chat": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _start_query(question: str) -> None:
    st.session_state.messages.append({"role": "user", "content": question})
    st.session_state.active_prompt = question
    st.session_state.processing = True
    st.session_state.processing_mode = "summary"
    st.session_state.scroll_chat = True


def _scroll_to_chat() -> None:
    components.html(
        """
        <script>
        (function () {
            const doc = window.parent.document;
            const anchor = doc.getElementById('chat-bottom-anchor');
            if (anchor) anchor.scrollIntoView({ behavior: 'smooth', block: 'end' });
        })();
        </script>
        """,
        height=0,
    )


def _render_exploring(prompt: str, container) -> None:
    lines = get_exploring_lines(prompt)
    revealed: list[str] = []
    body = container.empty()
    for i, line in enumerate(lines):
        revealed.append(line)
        body_html = "".join(f'<p class="exploring-line">{ln}</p>' for ln in revealed)
        body.markdown(
            f'<div class="exploring-box">'
            f'<div class="exploring-header"><span class="exploring-pulse"></span> Exploring</div>'
            f'<div class="exploring-body">{body_html}</div></div>',
            unsafe_allow_html=True,
        )
        time.sleep(0.5 if i < len(lines) - 1 else 0.35)


def _render_steps(steps: list[str], step_box) -> None:
    for i in range(len(steps)):
        lines = "".join(
            f'<div class="step-status done">✓ {steps[j][:-1]}</div>' if j < i
            else f'<div class="step-status active">⏳ {steps[j]}</div>' if j == i
            else f'<div class="step-status">{steps[j]}</div>'
            for j in range(len(steps))
        )
        step_box.markdown(lines, unsafe_allow_html=True)
        time.sleep(0.22)
    step_box.markdown(
        "".join(f'<div class="step-status done">✓ {s[:-1]}</div>' for s in steps),
        unsafe_allow_html=True,
    )


def _auto_download_file(data: bytes, filename: str) -> None:
    b64 = base64.b64encode(data).decode()
    components.html(
        f"""
        <script>
        (function() {{
            const link = document.createElement("a");
            link.href = "data:application/vnd.openxmlformats-officedocument.presentationml.presentation;base64,{b64}";
            link.download = "{filename}";
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }})();
        </script>
        """,
        height=0,
    )


def _resolve_summary(prompt: str) -> str:
    if prompt.startswith(UPLOAD_PREFIX):
        return st.session_state.upload_summary or "**Upload processed.**"
    return get_response(prompt, st.session_state.upload_summary)


def _render_action_buttons(msg_idx: int, prompt: str) -> None:
    col1, col2, _ = st.columns([1, 1, 2])
    with col1:
        if st.button("Generate PPT", key=f"gen_ppt_{msg_idx}", type="primary"):
            st.session_state.active_prompt = prompt
            st.session_state.active_msg_idx = msg_idx
            st.session_state.processing = True
            st.session_state.processing_mode = "ppt"
            st.rerun()
    with col2:
        if st.button("New question", key=f"new_q_{msg_idx}"):
            st.session_state.messages = []
            st.session_state.active_prompt = None
            st.session_state.active_msg_idx = None
            st.session_state.upload_summary = None
            st.session_state.upload_meta = None
            st.session_state.show_upload = False
            st.rerun()


def _render_faq_bar() -> None:
    st.markdown(f'<div class="chat-greeting">{GREETING}</div>', unsafe_allow_html=True)
    st.markdown('<div class="quick-faq-label">Quick questions</div>', unsafe_allow_html=True)

    row1 = st.columns(4)
    for i, (label, question) in enumerate(FAQ_ITEMS[:4]):
        with row1[i]:
            if st.button(label, key=f"faq_{i}", use_container_width=True):
                _start_query(question)
                st.rerun()

    row2 = st.columns(4)
    for i, (label, question) in enumerate(FAQ_ITEMS[4:], start=4):
        with row2[i - 4]:
            if st.button(label, key=f"faq_{i}", use_container_width=True):
                _start_query(question)
                st.rerun()

    up_col, _ = st.columns([1, 3])
    with up_col:
        if st.button("📎 Upload data", key="upload_toggle", use_container_width=True):
            st.session_state.show_upload = not st.session_state.show_upload
            st.rerun()

    if st.session_state.show_upload:
        uploaded = st.file_uploader(
            "Upload CSV or Excel",
            type=["csv", "xlsx", "xls"],
            key="data_upload",
            label_visibility="collapsed",
        )
        if uploaded is not None:
            try:
                df = load_upload(uploaded)
                st.session_state.upload_summary = summarize_upload(df, uploaded.name)
                st.session_state.upload_meta = extract_upload_meta(df, uploaded.name)
                st.session_state.messages.append({"role": "user", "content": f"Uploaded: {uploaded.name}"})
                st.session_state.active_prompt = f"{UPLOAD_PREFIX}{uploaded.name}"
                st.session_state.processing = True
                st.session_state.processing_mode = "summary"
                st.session_state.show_upload = False
                st.session_state.scroll_chat = True
                st.rerun()
            except Exception as exc:
                st.error(str(exc))


def render_demo() -> None:
    _init_state()

    st.markdown(
        """
<div class="chat-panel">
  <div class="chat-panel-header">
    <div class="kimi-avatar">✦</div>
    <div>
      <div class="kimi-chat-title">DeckGen AI Assistant</div>
      <div class="kimi-chat-subtitle">Connected to Enterprise Finance DB · Real-time</div>
    </div>
  </div>
</div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.auto_download:
        dl = st.session_state.auto_download
        _auto_download_file(dl["bytes"], dl["filename"])
        st.session_state.auto_download = None

    has_chat = bool(st.session_state.messages) or st.session_state.processing

    # FAQs stay at top when idle; compact bar when chat is active
    if not has_chat:
        _render_faq_bar()
    else:
        with st.expander("Quick questions & upload", expanded=False):
            _render_faq_bar()

    st.markdown('<div class="chat-scroll-area">', unsafe_allow_html=True)
    st.markdown('<div id="chat-top-anchor"></div>', unsafe_allow_html=True)

    if not st.session_state.messages and not st.session_state.processing:
        st.markdown(
            '<p class="chat-empty-hint">Pick a question above or type below to start.</p>',
            unsafe_allow_html=True,
        )

    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(f'<div class="response-body">{msg["content"]}</div>', unsafe_allow_html=True)
            if msg.get("prompt") and msg["role"] == "assistant" and not msg.get("ppt_generated"):
                _render_action_buttons(idx, msg["prompt"])
            if msg.get("ppt_generated"):
                st.markdown(
                    '<div class="ppt-ready-badge">✓ PowerPoint generated &amp; downloaded</div>',
                    unsafe_allow_html=True,
                )
                st.download_button(
                    label="Download again (6 slides)",
                    data=msg["download"]["bytes"],
                    file_name=msg["download"]["filename"],
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    key=f"dl_{idx}",
                )

    if st.session_state.processing:
        mode = st.session_state.processing_mode
        prompt = st.session_state.active_prompt

        if mode == "summary" and prompt:
            with st.chat_message("assistant"):
                explore_box = st.empty()
                if not prompt.startswith(UPLOAD_PREFIX):
                    _render_exploring(prompt, explore_box)
                else:
                    explore_box.markdown(
                        '<div class="exploring-box">'
                        '<div class="exploring-header"><span class="exploring-pulse"></span> Exploring</div>'
                        '<div class="exploring-body">'
                        '<p class="exploring-line">Loading uploaded dataset…</p>'
                        '<p class="exploring-line">Parsing columns and computing totals…</p>'
                        "</div></div>",
                        unsafe_allow_html=True,
                    )
                    time.sleep(0.8)
                summary = _resolve_summary(prompt)
                explore_box.empty()
                st.markdown(f'<div class="response-body">{summary}</div>', unsafe_allow_html=True)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": summary,
                    "prompt": prompt,
                    "ppt_generated": False,
                }
            )
            st.session_state.processing = False
            st.session_state.processing_mode = None
            st.session_state.active_prompt = None
            st.session_state.scroll_chat = True
            st.rerun()

        elif mode == "ppt" and prompt is not None:
            msg_idx = st.session_state.active_msg_idx
            deck_ctx = get_deck_context(prompt, st.session_state.upload_meta)
            status = st.status("Generating PowerPoint…", expanded=True)
            with status:
                step_box = st.empty()
                _render_steps(PPT_STEPS, step_box)
                pptx_bytes = build_executive_deck(deck_ctx)
            status.update(label="PowerPoint ready — downloading…", state="complete")

            ppt = {"bytes": pptx_bytes, "filename": deck_ctx.get("filename", "DeckGen_Executive_Summary.pptx")}
            if msg_idx is not None and msg_idx < len(st.session_state.messages):
                st.session_state.messages[msg_idx]["ppt_generated"] = True
                st.session_state.messages[msg_idx]["download"] = ppt

            st.session_state.auto_download = ppt
            st.session_state.processing = False
            st.session_state.processing_mode = None
            st.session_state.active_msg_idx = None
            st.session_state.active_prompt = None
            st.session_state.scroll_chat = True
            st.rerun()

    st.markdown('<div id="chat-bottom-anchor"></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.scroll_chat:
        _scroll_to_chat()
        st.session_state.scroll_chat = False

    if prompt := st.chat_input(CHAT_PLACEHOLDER):
        _start_query(prompt)
        st.rerun()

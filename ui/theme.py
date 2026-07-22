"""DeckGen AI — shared theme and top navigation."""

from __future__ import annotations

import streamlit as st


def inject_global_css() -> None:
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: #000000;
    background-image: radial-gradient(ellipse 70% 50% at 50% -5%, rgba(37,99,235,0.18), transparent);
}

#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { display: none; }

.block-container {
    padding-top: 0.5rem;
    padding-bottom: 3rem;
    max-width: 820px;
}

/* Top nav */
.top-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 0 1.5rem;
    border-bottom: 1px solid rgba(59,130,246,0.15);
    margin-bottom: 2.5rem;
}
.nav-logo {
    font-size: 1.05rem;
    font-weight: 800;
    color: #F8FAFC;
    letter-spacing: -0.02em;
}
.nav-logo span { color: #60A5FA; }

/* Hero */
.site-badge {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #93C5FD;
    margin-bottom: 1.25rem;
}
.site-hero h1 {
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 800;
    line-height: 1.15;
    color: #F8FAFC;
    margin: 0 0 1.25rem 0;
    letter-spacing: -0.03em;
}
.site-hero h1 em {
    font-style: normal;
    color: #60A5FA;
}
.site-hero .lead {
    font-size: 1.05rem;
    line-height: 1.7;
    color: #94A3B8;
    max-width: 640px;
    margin-bottom: 2rem;
}

/* Sections */
.site-section { margin-bottom: 3.5rem; }
.site-section h2 {
    font-size: 1.35rem;
    font-weight: 700;
    color: #F1F5F9;
    margin: 0 0 1rem 0;
}
.site-section p, .site-section li {
    color: #94A3B8;
    font-size: 0.95rem;
    line-height: 1.75;
}
.site-section ul { padding-left: 1.25rem; }
.site-section li { margin-bottom: 0.5rem; }
.site-section strong { color: #E2E8F0; }

.problem-list li { list-style: none; padding-left: 0; margin-bottom: 0.85rem; }
.problem-list li::before { content: "· "; color: #60A5FA; font-weight: bold; }

/* Blue cards on black */
.steps-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-top: 1.5rem;
}
@media (max-width: 800px) { .steps-grid { grid-template-columns: repeat(2, 1fr); } }

.step-card {
    background: linear-gradient(160deg, #0a1628 0%, #061018 100%);
    border: 1px solid rgba(59,130,246,0.25);
    border-radius: 12px;
    padding: 1.25rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
}
.step-num {
    font-size: 0.75rem;
    font-weight: 700;
    color: #60A5FA;
    margin-bottom: 0.6rem;
}
.step-card h3 {
    font-size: 0.9rem;
    font-weight: 600;
    color: #F1F5F9;
    margin: 0 0 0.4rem 0;
}
.step-card p {
    font-size: 0.82rem;
    color: #64748B;
    line-height: 1.55;
    margin: 0;
}

.example-quote {
    color: #93C5FD;
    font-style: italic;
    margin: 0.75rem 0;
}

/* Demo chat panel */
.chat-panel {
    background: linear-gradient(160deg, #0a1628 0%, #040810 100%);
    border: 1px solid rgba(59,130,246,0.22);
    border-radius: 14px;
    padding: 1rem 1.25rem;
    margin-bottom: 1rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
}
.chat-panel-header {
    display: flex;
    align-items: center;
    gap: 0.85rem;
}
.kimi-avatar {
    width: 38px;
    height: 38px;
    border-radius: 10px;
    background: linear-gradient(135deg, #2563EB 0%, #60A5FA 100%);
    color: #000;
    font-weight: 800;
    font-size: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.kimi-chat-title {
    font-size: 0.92rem;
    font-weight: 700;
    color: #F1F5F9;
    line-height: 1.3;
}
.kimi-chat-subtitle {
    font-size: 0.76rem;
    color: #64748B;
    margin-top: 0.1rem;
}

.chat-greeting {
    font-size: 1.05rem;
    font-weight: 600;
    color: #E2E8F0;
    margin: 0.5rem 0 0.75rem;
    line-height: 1.45;
}
.quick-faq-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 0.35rem;
}

.chat-scroll-area {
    background: linear-gradient(180deg, #050a12 0%, #020408 100%);
    border: 1px solid rgba(59,130,246,0.15);
    border-radius: 14px;
    padding: 0.75rem 0.85rem;
    margin: 0.75rem 0 0.5rem;
    min-height: 180px;
    max-height: 520px;
    overflow-y: auto;
}
.chat-empty-hint {
    font-size: 0.75rem;
    color: #64748B;
    text-align: center;
    padding: 2rem 1rem;
    margin: 0;
}

div[data-testid="stExpander"] {
    background: transparent !important;
    border: 1px solid rgba(59,130,246,0.12) !important;
    border-radius: 10px !important;
    margin-bottom: 0.5rem !important;
}
div[data-testid="stExpander"] summary {
    font-size: 0.72rem !important;
    color: #93C5FD !important;
}

/* FAQ pill chips */
div[data-testid="stPills"] {
    gap: 0.35rem !important;
    flex-wrap: wrap !important;
    padding: 0 0 0.25rem !important;
}
div[data-testid="stPills"] button {
    background: #0a1628 !important;
    color: #94A3B8 !important;
    border: 1px solid rgba(59,130,246,0.2) !important;
    border-radius: 8px !important;
    font-size: 0.68rem !important;
    font-weight: 500 !important;
    padding: 0.3rem 0.6rem !important;
    min-height: 1.65rem !important;
    line-height: 1.2 !important;
    transition: all 0.15s ease !important;
}
div[data-testid="stPills"] button:hover {
    border-color: rgba(96,165,250,0.5) !important;
    color: #BFDBFE !important;
    background: #0f2040 !important;
}
div[data-testid="stPills"] button[kind="pillsActive"],
div[data-testid="stPills"] button[aria-pressed="true"] {
    background: linear-gradient(135deg, rgba(37,99,235,0.25) 0%, rgba(59,130,246,0.15) 100%) !important;
    border-color: rgba(96,165,250,0.55) !important;
    color: #93C5FD !important;
}

/* Exploring animation */
.exploring-box {
    background: #0a1628;
    border: 1px solid rgba(59,130,246,0.2);
    border-radius: 10px;
    padding: 0.85rem 1rem;
    margin: 0.5rem 0 0.85rem;
}
.exploring-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.82rem;
    font-weight: 600;
    color: #60A5FA;
    margin-bottom: 0.65rem;
}
.exploring-pulse {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #60A5FA;
    animation: pulse 1.2s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.85); }
}
.exploring-body { min-height: 1rem; }
.exploring-line {
    font-size: 0.68rem;
    color: #64748B;
    line-height: 1.55;
    margin: 0.25rem 0;
}

/* Smaller assistant responses */
.response-body, .response-body p, .response-body li {
    font-size: 0.72rem !important;
    line-height: 1.55 !important;
    color: #94A3B8 !important;
}
.response-body strong { color: #93C5FD !important; font-size: 0.72rem !important; }
.response-body h1, .response-body h2, .response-body h3 {
    font-size: 0.82rem !important;
    color: #E2E8F0 !important;
    margin: 0.35rem 0 !important;
}
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li {
    font-size: 0.72rem !important;
    line-height: 1.55 !important;
    color: #94A3B8 !important;
}
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] strong {
    color: #93C5FD !important;
    font-size: 0.72rem !important;
}
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h1,
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h2,
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h3 {
    font-size: 0.82rem !important;
    color: #E2E8F0 !important;
}

.input-section { margin: 0.35rem 0 0.75rem; }

/* FAQ + upload buttons */
div[data-testid="stVerticalBlock"]:has(.quick-faq-label) ~ div div[data-testid="stButton"] > button {
    background: #0a1628 !important;
    color: #93C5FD !important;
    border: 1px solid rgba(59,130,246,0.25) !important;
    border-radius: 8px !important;
    font-size: 0.65rem !important;
    padding: 0.35rem 0.5rem !important;
    min-height: 1.65rem !important;
    line-height: 1.2 !important;
}
div[data-testid="stVerticalBlock"]:has(.quick-faq-label) ~ div div[data-testid="stButton"] > button:hover {
    background: rgba(37,99,235,0.15) !important;
    border-color: rgba(96,165,250,0.5) !important;
}

.stTextInput > div > div > input {
    background: #0a1628 !important;
    border: 1px solid rgba(59,130,246,0.2) !important;
    color: #F1F5F9 !important;
    border-radius: 10px !important;
    font-size: 0.78rem !important;
    padding: 0.55rem 0.85rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.2) !important;
}

div[data-testid="stFileUploader"] section {
    background: #0a1628 !important;
    border: 1px dashed rgba(59,130,246,0.3) !important;
    border-radius: 10px !important;
    padding: 0.5rem !important;
}
div[data-testid="stFileUploader"] span, div[data-testid="stFileUploader"] small {
    font-size: 0.72rem !important;
    color: #94A3B8 !important;
}
.exploring-detail {
    color: #93C5FD;
    font-weight: 600;
    background: rgba(37,99,235,0.15);
    padding: 0.05rem 0.35rem;
    border-radius: 4px;
}
@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* Chat messages */
div[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0.35rem 0 !important;
}
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p {
    color: #CBD5E1;
    line-height: 1.65;
}
div[data-testid="stChatMessage"]:has([data-testid="chat-avatar-user"]) {
    background: #0a1628 !important;
    border: 1px solid rgba(59,130,246,0.12) !important;
    border-radius: 12px !important;
    padding: 0.75rem 1rem !important;
}
div[data-testid="stChatMessage"]:has([data-testid="chat-avatar-assistant"]) {
    background: linear-gradient(160deg, #0c1a30 0%, #081018 100%) !important;
    border: 1px solid rgba(59,130,246,0.18) !important;
    border-radius: 12px !important;
    padding: 0.75rem 1rem !important;
}

.stChatFloatingInputContainer {
    background: #000000 !important;
    border-top: 1px solid rgba(59,130,246,0.12) !important;
}
.stChatInputContainer textarea {
    background: #0a1628 !important;
    border: 1px solid rgba(59,130,246,0.2) !important;
    color: #F1F5F9 !important;
    border-radius: 12px !important;
}

.step-status {
    color: #64748B;
    font-size: 0.82rem;
    margin: 0.2rem 0;
}
.step-status.done { color: #4ADE80; }
.step-status.active { color: #60A5FA; }

.ppt-ready-badge {
    display: inline-block;
    background: rgba(74, 222, 128, 0.1);
    border: 1px solid rgba(74, 222, 128, 0.25);
    color: #4ADE80;
    font-size: 0.82rem;
    font-weight: 600;
    padding: 0.35rem 0.75rem;
    border-radius: 999px;
    margin: 0.5rem 0;
}

div[data-testid="stChatMessage"] div[data-testid="stButton"] > button[kind="primary"] {
    font-size: 0.82rem !important;
    padding: 0.4rem 0.85rem !important;
    min-height: 2.1rem !important;
    border-radius: 8px !important;
}
div[data-testid="stChatMessage"] div[data-testid="stButton"] > button[kind="secondary"] {
    font-size: 0.82rem !important;
    padding: 0.4rem 0.85rem !important;
    min-height: 2.1rem !important;
    border-radius: 8px !important;
    background: #0a1628 !important;
    color: #94A3B8 !important;
    border: 1px solid rgba(59,130,246,0.15) !important;
}

div[data-testid="stDownloadButton"] button,
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #2563EB 0%, #3B82F6 100%) !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 8px !important;
}
div[data-testid="stButton"] > button[kind="secondary"] {
    background: #0a1628 !important;
    color: #94A3B8 !important;
    border: 1px solid rgba(59,130,246,0.2) !important;
}
</style>
        """,
        unsafe_allow_html=True,
    )


def render_top_nav() -> str:
    if "page" not in st.session_state:
        st.session_state.page = "Home"

    if st.session_state.page not in ("Home", "Demo"):
        st.session_state.page = "Demo" if "Demo" in st.session_state.page or "Generate" in st.session_state.page else "Home"

    logo_col, home_col, demo_col = st.columns([4, 1, 1])

    with logo_col:
        st.markdown(
            '<div class="top-nav" style="border:none;margin:0;padding:0.5rem 0;">'
            '<div class="nav-logo">▚ DeckGen <span>AI</span></div></div>',
            unsafe_allow_html=True,
        )

    current = st.session_state.page
    with home_col:
        if st.button("Home", type="primary" if current == "Home" else "secondary", use_container_width=True):
            st.session_state.page = "Home"
            st.rerun()
    with demo_col:
        if st.button("Demo", type="primary" if current == "Demo" else "secondary", use_container_width=True):
            st.session_state.page = "Demo"
            st.rerun()

    return st.session_state.page

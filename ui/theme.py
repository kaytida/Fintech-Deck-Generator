"""DeckGen AI — shared theme and top navigation."""

from __future__ import annotations

import streamlit as st


def inject_global_css() -> None:
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {
    --dg-cyan: #38BDF8;
    --dg-blue: #60A5FA;
    --dg-violet: #8B5CF6;
    --dg-text: #F1F5F9;
    --dg-muted: #94A3B8;
    --dg-card: linear-gradient(160deg, #111d33 0%, #0a1322 100%);
    --dg-border: rgba(96,165,250,0.18);
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background:
        radial-gradient(1000px 520px at 82% -8%, rgba(56,189,248,0.16), transparent 60%),
        radial-gradient(820px 460px at -8% 8%, rgba(139,92,246,0.14), transparent 55%),
        #070c17;
}

#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { display: none; }

.block-container {
    padding-top: 0.5rem;
    padding-bottom: 3rem;
    max-width: 860px;
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
    font-size: 1.15rem;
    font-weight: 900;
    color: #F8FAFC;
    letter-spacing: -0.02em;
}
.nav-logo span {
    background: linear-gradient(120deg, var(--dg-cyan), var(--dg-violet));
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Hero */
.site-badge {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #93C5FD;
    background: rgba(56,189,248,0.08);
    border: 1px solid rgba(56,189,248,0.22);
    padding: 0.4rem 0.9rem;
    border-radius: 999px;
    margin-bottom: 1.35rem;
}
.site-hero h1 {
    font-size: clamp(2.1rem, 5.5vw, 3.3rem);
    font-weight: 900;
    line-height: 1.12;
    color: #F8FAFC;
    margin: 0 0 1.25rem 0;
    letter-spacing: -0.035em;
}
.site-hero h1 em {
    font-style: normal;
    background: linear-gradient(120deg, var(--dg-cyan), var(--dg-violet));
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}
.site-hero .lead {
    font-size: 1.08rem;
    line-height: 1.7;
    color: #A7B5C9;
    max-width: 660px;
    margin-bottom: 2rem;
}

/* Impact stats strip */
.stat-strip {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin: 0.5rem 0 1rem;
}
@media (max-width: 640px) { .stat-strip { grid-template-columns: 1fr; } }
.stat-card {
    background: var(--dg-card);
    border: 1px solid var(--dg-border);
    border-radius: 14px;
    padding: 1.1rem 1.25rem;
}
.stat-value {
    font-size: 1.7rem;
    font-weight: 900;
    letter-spacing: -0.02em;
    background: linear-gradient(120deg, var(--dg-cyan), var(--dg-violet));
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}
.stat-label { font-size: 0.8rem; color: var(--dg-muted); margin-top: 0.15rem; }

/* Sections */
.site-section { margin-bottom: 3.5rem; }
.site-section h2 {
    font-size: 1.5rem;
    font-weight: 800;
    color: #F1F5F9;
    margin: 0 0 1rem 0;
    letter-spacing: -0.02em;
}
.site-section p, .site-section li {
    color: #A7B5C9;
    font-size: 0.98rem;
    line-height: 1.75;
}
.site-section ul { padding-left: 1.25rem; }
.site-section li { margin-bottom: 0.5rem; }
.site-section strong { color: #E2E8F0; }

.problem-list li {
    list-style: none;
    padding-left: 1.4rem;
    position: relative;
    margin-bottom: 0.9rem;
}
.problem-list li::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0.62em;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--dg-cyan);
    box-shadow: 0 0 0 4px rgba(56,189,248,0.14);
}

/* Solution cards */
.steps-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-top: 1.5rem;
}
@media (max-width: 800px) { .steps-grid { grid-template-columns: repeat(2, 1fr); } }

.step-card {
    position: relative;
    background: var(--dg-card);
    border: 1px solid var(--dg-border);
    border-radius: 14px;
    padding: 1.35rem 1.2rem;
    box-shadow: 0 8px 28px rgba(0,0,0,0.45);
    overflow: hidden;
    transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
}
.step-card::before {
    content: "";
    position: absolute;
    inset: 0 0 auto 0;
    height: 3px;
    background: linear-gradient(90deg, var(--dg-cyan), var(--dg-violet));
    opacity: 0.85;
}
.step-card:hover {
    transform: translateY(-3px);
    border-color: rgba(56,189,248,0.45);
    box-shadow: 0 14px 36px rgba(56,189,248,0.14);
}
.step-num {
    display: inline-grid;
    place-items: center;
    width: 30px; height: 30px;
    border-radius: 9px;
    background: linear-gradient(135deg, var(--dg-cyan), var(--dg-violet));
    color: #06121f;
    font-size: 0.9rem;
    font-weight: 900;
    margin-bottom: 0.7rem;
}
.step-card h3 {
    font-size: 0.95rem;
    font-weight: 700;
    color: #F1F5F9;
    margin: 0 0 0.4rem 0;
}
.step-card p {
    font-size: 0.83rem;
    color: #8496AD;
    line-height: 1.55;
    margin: 0;
}

.example-quote {
    color: #BFDBFE;
    font-style: italic;
    background: rgba(56,189,248,0.06);
    border-left: 3px solid var(--dg-cyan);
    padding: 0.6rem 0.9rem;
    border-radius: 8px;
    margin: 0.75rem 0;
}

/* Demo chat panel */
.chat-panel {
    background: linear-gradient(160deg, #111d33 0%, #0a1322 100%);
    border: 1px solid rgba(96,165,250,0.2);
    border-radius: 16px;
    padding: 1.05rem 1.3rem;
    margin-bottom: 1rem;
    box-shadow: 0 12px 40px rgba(0,0,0,0.5);
}
.chat-panel-header {
    display: flex;
    align-items: center;
    gap: 0.85rem;
}
.kimi-avatar {
    width: 40px;
    height: 40px;
    border-radius: 11px;
    background: linear-gradient(135deg, #38BDF8 0%, #8B5CF6 100%);
    color: #06121f;
    font-weight: 900;
    font-size: 1.1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    box-shadow: 0 6px 18px rgba(56,189,248,0.3);
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

/* Assistant responses — readable, compact */
.response-body, .response-body p, .response-body li {
    font-size: 0.85rem !important;
    line-height: 1.65 !important;
    color: #B4C2D6 !important;
}
.response-body strong { color: #93C5FD !important; font-size: 0.85rem !important; }
.response-body h1, .response-body h2, .response-body h3 {
    font-size: 0.95rem !important;
    color: #E2E8F0 !important;
    margin: 0.4rem 0 !important;
}
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li {
    font-size: 0.85rem !important;
    line-height: 1.65 !important;
    color: #B4C2D6 !important;
}
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] strong {
    color: #93C5FD !important;
    font-size: 0.85rem !important;
}
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h1,
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h2,
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h3 {
    font-size: 0.95rem !important;
    color: #E2E8F0 !important;
}
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] table {
    font-size: 0.8rem !important;
    border-collapse: collapse !important;
}
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] th,
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] td {
    border: 1px solid rgba(96,165,250,0.15) !important;
    padding: 0.3rem 0.55rem !important;
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
    background: linear-gradient(135deg, #38BDF8 0%, #8B5CF6 100%) !important;
    color: #06121f !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    box-shadow: 0 8px 22px rgba(56,189,248,0.28) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}
div[data-testid="stDownloadButton"] button:hover,
div[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 12px 28px rgba(56,189,248,0.4) !important;
}
div[data-testid="stButton"] > button[kind="secondary"] {
    background: rgba(17,29,51,0.7) !important;
    color: #A7B5C9 !important;
    border: 1px solid rgba(96,165,250,0.2) !important;
    border-radius: 10px !important;
    transition: border-color 0.15s ease, color 0.15s ease !important;
}
div[data-testid="stButton"] > button[kind="secondary"]:hover {
    border-color: rgba(56,189,248,0.5) !important;
    color: #E2E8F0 !important;
}

/* ============================================================
   Demo page — FastAPI-style console → pipeline → result
   ============================================================ */
.demo-head { text-align: center; max-width: 640px; margin: 0 auto 1.75rem; }
.demo-eyebrow {
    text-transform: uppercase;
    letter-spacing: 0.16em;
    font-size: 0.7rem;
    font-weight: 800;
    color: var(--dg-cyan);
    margin-bottom: 0.5rem;
}
.demo-title {
    font-size: clamp(1.7rem, 4vw, 2.4rem);
    font-weight: 900;
    letter-spacing: -0.03em;
    color: #F8FAFC;
    margin: 0 0 0.6rem;
}
.demo-title em {
    font-style: normal;
    background: linear-gradient(120deg, var(--dg-cyan), var(--dg-violet));
    -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
}
.demo-sub { color: var(--dg-muted); font-size: 0.95rem; line-height: 1.6; }

/* Console card wrapper (visual only) */
.console-card {
    background: var(--dg-card);
    border: 1px solid var(--dg-border);
    border-radius: 16px;
    padding: 1.25rem 1.35rem 0.5rem;
    box-shadow: 0 12px 40px rgba(0,0,0,0.5);
    margin-bottom: 1rem;
}
.console-label {
    font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.12em;
    color: var(--dg-muted); font-weight: 700; margin-bottom: 0.5rem;
}

/* Prompt textarea */
.stTextArea textarea {
    background: #070d1a !important;
    border: 1px solid rgba(96,165,250,0.2) !important;
    color: #F1F5F9 !important;
    border-radius: 12px !important;
    font-size: 0.92rem !important;
}
.stTextArea textarea:focus {
    border-color: var(--dg-cyan) !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.18) !important;
}

.chips-hint { color: var(--dg-muted); font-size: 0.8rem; margin: 0.25rem 0 0.4rem; }

/* Agent pipeline panel */
.agent-panel {
    background: var(--dg-card);
    border: 1px solid var(--dg-border);
    border-radius: 16px;
    padding: 1.15rem 1.35rem;
    box-shadow: 0 12px 40px rgba(0,0,0,0.5);
    margin-bottom: 1rem;
}
.agent-head {
    display: flex; align-items: center; gap: 0.6rem;
    font-weight: 700; color: #E2E8F0; margin-bottom: 0.85rem; font-size: 0.95rem;
}
.spinner {
    width: 16px; height: 16px;
    border: 2.5px solid rgba(56,189,248,0.25);
    border-top-color: var(--dg-cyan);
    border-radius: 50%;
    display: inline-block;
    animation: dg-spin 0.8s linear infinite;
}
@keyframes dg-spin { to { transform: rotate(360deg); } }
.agent-step {
    display: flex; align-items: center; gap: 0.55rem;
    padding: 0.32rem 0; color: var(--dg-muted); font-size: 0.9rem;
}
.agent-step .ico { width: 16px; text-align: center; }
.agent-step.active { color: var(--dg-cyan); font-weight: 600; }
.agent-step.done { color: #4ADE80; }

/* Result panel */
.result-bar {
    display: flex; align-items: center; gap: 0.7rem; flex-wrap: wrap;
    padding-bottom: 0.9rem; margin-bottom: 1.1rem;
    border-bottom: 1px solid var(--dg-border);
}
.result-badge {
    background: rgba(74,222,128,0.14); color: #4ADE80;
    border: 1px solid rgba(74,222,128,0.4);
    padding: 0.25rem 0.7rem; border-radius: 999px;
    font-size: 0.75rem; font-weight: 800;
}
.deck-title-label { color: var(--dg-muted); font-size: 0.88rem; }

.kpi-row {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.85rem; margin-bottom: 1.2rem;
}
@media (max-width: 640px) { .kpi-row { grid-template-columns: 1fr; } }
.kpi {
    background: #070d1a; border: 1px solid var(--dg-border);
    border-radius: 12px; padding: 0.85rem 1rem;
}
.kpi-label { font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--dg-muted); }
.kpi-value { font-size: 1.4rem; font-weight: 900; color: #F1F5F9; margin-top: 0.15rem; }
.kpi-sub { font-size: 0.78rem; color: var(--dg-muted); }
.kpi.bad .kpi-value { color: #F87171; }
.kpi.good .kpi-value { color: #4ADE80; }

.dg-table { width: 100%; border-collapse: collapse; margin-bottom: 1.2rem; font-size: 0.85rem; }
.dg-table th, .dg-table td { text-align: left; padding: 0.5rem 0.65rem; border-bottom: 1px solid var(--dg-border); }
.dg-table th { color: var(--dg-muted); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em; }
.dg-table td.bad { color: #F87171; font-weight: 600; }
.dg-table td.good { color: #4ADE80; font-weight: 600; }

.slide-outline h4 { margin: 0 0 0.6rem; color: #F1F5F9; font-size: 0.95rem; }
.slide-outline ol { margin: 0; padding-left: 1.2rem; color: #B4C2D6; }
.slide-outline li { margin-bottom: 0.5rem; font-size: 0.88rem; }
.slide-sub { display: block; color: var(--dg-muted); font-size: 0.8rem; }

.source-tag { margin: 0.9rem 0 0.2rem; font-size: 0.78rem; color: var(--dg-muted); font-style: italic; }
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

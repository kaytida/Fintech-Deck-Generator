"""DeckGen AI — From Plain English to Boardroom Decks."""

from __future__ import annotations

import os

import streamlit as st

from ui.dashboard import render_dashboard
from ui.demo import render_demo
from ui.home import render_home
from ui.theme import inject_global_css, render_top_nav

st.set_page_config(
    page_title="DeckGen AI — From Plain English to Boardroom Decks",
    page_icon="▚",
    layout="centered",
    initial_sidebar_state="collapsed",
)


def _bridge_secrets_to_env() -> None:
    """Expose Streamlit secrets (Cloud dashboard or local secrets.toml) as env vars
    so backend services can read the LLM token without importing Streamlit."""
    try:
        for key, value in st.secrets.items():
            if isinstance(value, str):
                os.environ.setdefault(key, value)
    except Exception:
        # No secrets file locally — fine; the app falls back to the template narrative.
        pass


_bridge_secrets_to_env()

inject_global_css()

page = render_top_nav()

if page == "Home":
    render_home()
elif page == "Dashboard":
    render_dashboard()
else:
    render_demo()

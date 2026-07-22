"""Home page — matches fintech-deck-generator.vercel.app."""

from __future__ import annotations

import streamlit as st


def render_home() -> None:
    st.markdown(
        """
<div class="site-hero">
  <div class="site-badge">Autonomous Presentation Engine for Finance &amp; GCC Leadership</div>
  <h1>From plain English to a boardroom-ready deck in <em>15 seconds.</em></h1>
  <p class="lead">
    DeckGen AI connects directly to your enterprise database, understands a plain-English request,
    computes the numbers, writes the narrative, and generates a fully editable PowerPoint — instantly.
  </p>
</div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Try the Live Demo →", type="primary"):
        st.session_state.page = "Demo"
        st.rerun()

    st.markdown(
        """
<div class="stat-strip">
  <div class="stat-card">
    <div class="stat-value">~15 sec</div>
    <div class="stat-label">From plain-English prompt to a finished deck</div>
  </div>
  <div class="stat-card">
    <div class="stat-value">10–15 hrs</div>
    <div class="stat-label">Manual deck-building saved per month</div>
  </div>
  <div class="stat-card">
    <div class="stat-value">100%</div>
    <div class="stat-label">Fully editable, data-driven PowerPoint</div>
  </div>
</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="site-section">
  <h2>Introduction</h2>
  <p>
    Global Capability Center (GCC) leadership teams, CFOs, and finance directors are flooded with
    rich BI dashboards and AI query chatbots. Yet when an operational crisis or budget spike hits,
    the insight is trapped — locked inside dense dashboards and un-shareable chat replies.
  </p>
  <p>
    <strong>DeckGen AI</strong> is an autonomous presentation engine that turns a single plain-English
    request into a downloadable, data-driven executive deck — closing the gap between enterprise
    data and the boardroom.
  </p>
</div>

<div class="site-section">
  <h2>Problem Statement</h2>
  <p>Leadership faces a severe <strong>"Last-Mile Communication Friction."</strong></p>
  <ul class="problem-list">
    <li><strong>Dashboards are too dense</strong> for executive decision-making during high-stakes leadership reviews.</li>
    <li><strong>Chatbot answers are non-shareable</strong> — trapped in text boxes that can't be presented to offshore HQ executives.</li>
    <li><strong>Manual slide creation wastes 10–15 hours a month</strong> — screenshotting charts, copying numbers, and rebuilding decks.</li>
  </ul>
</div>

<div class="site-section">
  <h2>Our Solution</h2>
  <p>A user types a request such as</p>
  <p class="example-quote">"Generate a 4-slide deck explaining our Q2 software infrastructure overrun for HQ."</p>
  <p>DeckGen AI then autonomously:</p>
  <div class="steps-grid">
    <div class="step-card">
      <div class="step-num">1</div>
      <h3>Queries the database</h3>
      <p>Pulls budget vs. actuals straight from the enterprise finance data.</p>
    </div>
    <div class="step-card">
      <div class="step-num">2</div>
      <h3>Calculates variances</h3>
      <p>Computes budget-vs-actual gaps and quarter-over-quarter trends.</p>
    </div>
    <div class="step-card">
      <div class="step-num">3</div>
      <h3>Synthesizes insight</h3>
      <p>Writes executive bullet points and a headline narrative.</p>
    </div>
    <div class="step-card">
      <div class="step-num">4</div>
      <h3>Generates the deck</h3>
      <p>Outputs an editable .pptx with data-driven charts.</p>
    </div>
  </div>
</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    if st.button("Go to Demo →", type="primary"):
        st.session_state.page = "Demo"
        st.rerun()

    st.caption("DeckGen AI · Hackathon Prototype")

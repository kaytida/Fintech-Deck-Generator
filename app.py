"""
DeckGen AI — Streamlit Version
Autonomous Presentation Engine for Finance & GCC Leadership
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

# ============================================================
# PAGE CONFIG & STYLING
# ============================================================
st.set_page_config(
    page_title="DeckGen AI",
    page_icon="▚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    :root {
        --bg: #0f172a;
        --card: #1e293b;
        --blue: #38bdf8;
        --amber: #fbbf24;
        --green: #4ade80;
        --violet: #8b5cf6;
    }
    
    .main {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.1), rgba(139, 92, 246, 0.1));
    }
    
    .hero-title {
        font-size: 2.5em;
        font-weight: 700;
        margin-bottom: 1em;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 1.1em;
        color: #94a3b8;
        margin-bottom: 1.5em;
        line-height: 1.6;
    }
    
    .highlight-blue {
        color: #38bdf8;
        font-weight: 600;
    }
    
    .highlight-green {
        color: #4ade80;
        font-weight: 600;
    }
    
    .highlight-amber {
        color: #fbbf24;
        font-weight: 600;
    }
    
    .problem-list {
        margin: 1.5em 0;
    }
    
    .step-box {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(51, 65, 85, 0.5);
        border-radius: 12px;
        padding: 1.5em;
        margin: 1em 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA LOADING
# ============================================================
@st.cache_data
def load_data():
    """Load and combine all quarterly CSV files."""
    data_dir = Path("data")
    all_data = []
    
    for csv_file in sorted(data_dir.glob("*.csv")):
        df = pd.read_csv(csv_file)
        all_data.append(df)
    
    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        # Enrich with calculated fields
        combined['variance'] = combined['actual_usd'] - combined['budget_usd']
        combined['variance_pct'] = (combined['variance'] / combined['budget_usd'] * 100).round(1)
        combined['is_overrun'] = combined['variance'] > 0
        return combined
    return pd.DataFrame()

# ============================================================
# TAB NAVIGATION
# ============================================================
tab1, tab2 = st.tabs(["🏠 Home", "📊 Demo"])

# ============================================================
# HOME PAGE
# ============================================================
with tab1:
    # Hero Section
    st.markdown("""
    <p style="color: #38bdf8; font-weight: 600; font-size: 0.9em; letter-spacing: 0.5px; margin-bottom: 0.5em;">
        AUTONOMOUS PRESENTATION ENGINE FOR FINANCE & GCC LEADERSHIP
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <h1 class="hero-title">
        From plain English to a boardroom-ready deck in <span class="highlight-blue">15 seconds</span>.
    </h1>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <p class="hero-subtitle">
    DeckGen AI connects directly to your enterprise database, understands a plain-English request, 
    computes the numbers, writes the narrative, and generates a fully editable PowerPoint — instantly.
    </p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("→ Try the Live Demo", use_container_width=True, type="primary"):
            st.switch_to_query_params({"tab": "demo"})
    
    st.divider()
    
    # Introduction
    st.markdown("#### 🎯 Introduction")
    st.markdown("""
    Global Capability Center (GCC) leadership teams, CFOs, and finance directors are flooded with rich BI 
    dashboards and AI query chatbots. Yet when an operational crisis or budget spike hits, the insight is 
    trapped — locked inside dense dashboards and un-shareable chat replies.
    
    **DeckGen AI** is an autonomous presentation engine that turns a single plain-English request into a 
    downloadable, data-driven executive deck — closing the gap between enterprise data and the boardroom.
    """)
    
    st.divider()
    
    # Problem Statement
    st.markdown("#### ⚠️ The Problem")
    st.markdown('<p class="hero-subtitle">Leadership faces a severe <span class="highlight-amber">Last-Mile Communication Friction</span></p>', 
                unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="step-box">
        <h4>📊 Dashboards Too Dense</h4>
        <p>Executive decision-making during high-stakes leadership reviews requires clarity, not complexity.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="step-box">
        <h4>💬 Chatbot Answers Non-Shareable</h4>
        <p>AI responses trapped in text boxes can't be presented to offshore HQ executives.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="step-box">
        <h4>⏱️ Manual Slide Creation Wastes 10–15 Hours/Month</h4>
        <p>Screenshotting charts, copying numbers, and rebuilding decks manually.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Solution
    st.markdown("#### ✨ Our Solution")
    st.markdown("""
    A user types a request such as **"Generate a 4-slide deck explaining our Q2 software infrastructure 
    overrun for HQ."** DeckGen AI then autonomously:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="step-box">
        <h3 style="margin-top: 0; color: #38bdf8;">1️⃣ Queries the Database</h3>
        <p>Pulls budget vs. actuals straight from the enterprise finance data.</p>
        </div>
        
        <div class="step-box">
        <h3 style="margin-top: 0; color: #4ade80;">2️⃣ Calculates Variances</h3>
        <p>Computes budget-vs-actual gaps and quarter-over-quarter trends.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="step-box">
        <h3 style="margin-top: 0; color: #fbbf24;">3️⃣ Synthesizes Insight</h3>
        <p>Writes executive bullet points and a headline narrative.</p>
        </div>
        
        <div class="step-box">
        <h3 style="margin-top: 0; color: #8b5cf6;">4️⃣ Generates the Deck</h3>
        <p>Outputs an editable <code>.pptx</code> with data-driven charts.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Key Benefits
    st.markdown("#### 🚀 Key Benefits")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Time Saved", "12 hrs/month", "vs. manual slide creation")
    
    with col2:
        st.metric("Deck Generation", "15 seconds", "from request to download")
    
    with col3:
        st.metric("Data Accuracy", "100%", "automated from live databases")

# ============================================================
# DEMO PAGE
# ============================================================
with tab2:
    st.markdown("#### 📊 Interactive Financial Data Explorer")
    st.markdown("Explore quarterly budget vs. actual spending across departments and categories.")
    
    # Load data
    df = load_data()
    
    if df.empty:
        st.warning("No data files found. Please ensure CSV files are in the `data/` directory.")
    else:
        # ---- FILTERS ----
        col1, col2, col3 = st.columns(3)
        
        with col1:
            quarters = sorted(df['quarter'].unique())
            selected_quarter = st.selectbox("Select Quarter", quarters, key="quarter_filter")
        
        with col2:
            departments = sorted(df['department'].unique())
            selected_dept = st.selectbox("Select Department", ["All"] + list(departments), key="dept_filter")
        
        with col3:
            categories = sorted(df['category'].unique())
            selected_category = st.selectbox("Select Category", ["All"] + list(categories), key="cat_filter")
        
        # Filter data
        filtered_df = df[df['quarter'] == selected_quarter].copy()
        
        if selected_dept != "All":
            filtered_df = filtered_df[filtered_df['department'] == selected_dept]
        
        if selected_category != "All":
            filtered_df = filtered_df[filtered_df['category'] == selected_category]
        
        # ---- SUMMARY METRICS ----
        st.divider()
        
        total_budget = filtered_df['budget_usd'].sum()
        total_actual = filtered_df['actual_usd'].sum()
        total_variance = total_actual - total_budget
        variance_pct = (total_variance / total_budget * 100) if total_budget > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Budget", f"${total_budget:,.0f}")
        
        with col2:
            st.metric("Total Actual", f"${total_actual:,.0f}")
        
        with col3:
            variance_color = "🔴" if total_variance > 0 else "🟢"
            st.metric("Variance", f"{variance_color} ${abs(total_variance):,.0f}", f"{variance_pct:+.1f}%")
        
        with col4:
            overrun_count = len(filtered_df[filtered_df['is_overrun']])
            st.metric("Overrun Items", overrun_count, f"of {len(filtered_df)}")
        
        st.divider()
        
        # ---- VISUALIZATIONS ----
        viz_col1, viz_col2 = st.columns(2)
        
        # Budget vs Actual by Category
        with viz_col1:
            if selected_category == "All":
                chart_data = filtered_df.groupby('category')[['budget_usd', 'actual_usd']].sum().reset_index()
            else:
                chart_data = filtered_df.groupby('category')[['budget_usd', 'actual_usd']].sum().reset_index()
            
            if not chart_data.empty:
                fig = go.Figure(data=[
                    go.Bar(name='Budget', x=chart_data['category'], y=chart_data['budget_usd'], 
                           marker_color='#38bdf8'),
                    go.Bar(name='Actual', x=chart_data['category'], y=chart_data['actual_usd'],
                           marker_color='#ff6b6b')
                ])
                fig.update_layout(
                    title="Budget vs Actual by Category",
                    barmode='group',
                    height=400,
                    template='plotly_dark',
                    showlegend=True,
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Variance Distribution
        with viz_col2:
            variance_data = filtered_df.copy()
            variance_data = variance_data.sort_values('variance', ascending=True)
            
            colors = ['#4ade80' if x < 0 else '#ff6b6b' for x in variance_data['variance']]
            fig = go.Figure(data=[
                go.Bar(y=variance_data['category'], x=variance_data['variance'], 
                       orientation='h', marker_color=colors)
            ])
            fig.update_layout(
                title="Variance by Category (Negative=Savings, Positive=Overrun)",
                height=400,
                template='plotly_dark',
                showlegend=False,
                hovermode='y'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # ---- DATA TABLE ----
        st.markdown("#### 📋 Detailed Data")
        
        display_df = filtered_df[['department', 'category', 'budget_usd', 'actual_usd', 'variance', 'variance_pct']].copy()
        display_df.columns = ['Department', 'Category', 'Budget', 'Actual', 'Variance', 'Variance %']
        display_df['Budget'] = display_df['Budget'].apply(lambda x: f"${x:,.0f}")
        display_df['Actual'] = display_df['Actual'].apply(lambda x: f"${x:,.0f}")
        display_df['Variance'] = display_df['Variance'].apply(lambda x: f"${x:,.0f}")
        display_df = display_df.sort_values('Variance', key=abs, ascending=False)
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Export option
        st.markdown("#### ⬇️ Export Data")
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name=f"deckgen_data_{selected_quarter}.csv",
            mime="text/csv"
        )

# ============================================================
# FOOTER
# ============================================================
st.divider()
st.markdown("""
<p style="text-align: center; color: #94a3b8; font-size: 0.9em;">
    DeckGen AI · Autonomous Presentation Engine · Hackathon Prototype
</p>
""", unsafe_allow_html=True)

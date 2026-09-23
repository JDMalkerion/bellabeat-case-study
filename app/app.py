"""
Bellabeat Fitness Tracker Data Analysis App.
Main landing page and entry point for the Streamlit multipage application.
"""

import streamlit as st
from utils import apply_custom_css, get_db_connection, run_query

st.set_page_config(
    page_title="Bellabeat Fitness Analytics",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_custom_css()

# Sidebar Navigation Intro
with st.sidebar:
    st.markdown("## ✨ Bellabeat Analytics")
    st.caption("Smart Wellness Tracker Consumer Insights")
    st.markdown("---")
    st.markdown(
        """
        **Pages:**
        - **1. Overview**: Executive KPIs & Segmentation
        - **2. Activity**: Weekday steps, intensity, calories
        - **3. Sleep & Wear**: Sleep patterns, engagement & heatmap
        - **4. SQL Analysis**: Live views, source SQL & query console
        - **5. Recommendations**: Strategic business growth playbook
        """
    )
    st.markdown("---")
    st.info("Database: `sql/bellabeat.db` (Read-Only Mode: `mode=ro`)")
    st.caption("Fitbit Consumer Tracker Dataset (30+ Participants)")

# Hero Header
st.title("✨ Bellabeat Consumer Wellness Analysis")
st.markdown(
    """
    **Welcome to the Bellabeat Case Study Analytics Portal.**  
    Bellabeat develops beautifully designed, health-focused smart products tailored specifically for women.
    This interactive dashboard analyzes smart device usage data (Fitbit dataset) to uncover behavioral insights,
    daily habit patterns, sleep efficiency, and tracker engagement to empower Bellabeat's global marketing strategy.
    """
)

st.markdown("---")

# Quick Stats Ribbon
try:
    user_count = run_query("SELECT COUNT(DISTINCT Id) FROM clean_dailyActivity").iloc[0, 0]
    total_records = run_query("SELECT COUNT(*) FROM clean_dailyActivity").iloc[0, 0]
    sleep_records = run_query("SELECT COUNT(*) FROM clean_sleepDay").iloc[0, 0]
    nonwear_days = run_query("SELECT COUNT(*) FROM clean_dailyActivity WHERE is_likely_nonwear = 1").iloc[0, 0]
except Exception as e:
    st.error(f"Error loading initial metrics from database: {e}")
    user_count, total_records, sleep_records, nonwear_days = 33, 940, 410, 79

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Tracked Participants</div>
            <div class="metric-value">{user_count}</div>
            <div class="metric-sub">Daily activity users</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Daily Activity Logs</div>
            <div class="metric-value">{total_records:,}</div>
            <div class="metric-sub">Total tracked days</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Sleep Records</div>
            <div class="metric-value">{sleep_records:,}</div>
            <div class="metric-sub">Deduplicated nights logged</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Non-Wear Days Flagged</div>
            <div class="metric-value">{nonwear_days}</div>
            <div class="metric-sub">24h inactive periods</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# Overview Columns
col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("🎯 Business Problem & Purpose")
    st.markdown(
        """
        - **Company Background**: Bellabeat was founded by Urška Sršen and Sando Mur to create tech-enabled wellness trackers
          (e.g., *Leaf*, *Time*, *Spring*, *Bellabeat App*) that monitor activity, sleep, stress, and reproductive health.
        - **Executive Goal**: Analyze public fitness tracker trends to identify customer usage patterns, uncover retention bottlenecks,
          and recommend growth opportunities for Bellabeat's product ecosystem.
        - **Data Pipeline Architecture**:
          1. **Database**: SQLite database ([`sql/bellabeat.db`](file:///home/JDCypher/Projects/bellabeat-case-study/sql/bellabeat.db)) storing 10 normalized tables.
          2. **Cleaning Layer**: Standardized ISO 8601 timestamps, explicit deduplication, and non-wear identification.
          3. **Analytical Views**: 8 aggregated views modeling habits, user segments, diurnal energy burn, and sleep cycles.
          4. **Application**: Interactive multipage Streamlit analytics suite.
        """
    )

with col_right:
    st.subheader("🧭 Guided Exploration")
    st.markdown(
        """
        Navigate through the sidebar pages to explore:
        
        1. **[Overview](1_Overview)**: Executive KPIs, high-level dataset health, and user segmentation breakdown.
        2. **[Activity](2_Activity)**: Steps across the week, activity intensity distributions, and diurnal calorie curves.
        3. **[Sleep & Wear](3_Sleep_and_Wear)**: Participant sleep efficiency, wear adherence, and sedentary heatmap.
        4. **[SQL Analysis](4_SQL_Analysis)**: Live SQL view inspector, underlying queries, and a custom read-only query terminal.
        5. **[Recommendations](5_Recommendations)**: Strategic marketing proposals and product features for Bellabeat.
        """
    )

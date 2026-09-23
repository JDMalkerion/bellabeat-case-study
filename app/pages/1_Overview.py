"""
Overview Page for Bellabeat Fitness Analytics.
Displays executive KPI cards and summary visual insights.
"""

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import sys
from pathlib import Path

# Add app root to path for imports
app_dir = Path(__file__).resolve().parent.parent
if str(app_dir) not in sys.path:
    sys.path.insert(0, str(app_dir))

from utils import (
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    COLOR_ACCENT,
    COLOR_DARK,
    apply_custom_css,
    run_query,
)

st.set_page_config(page_title="Overview | Bellabeat Analytics", page_icon="📊", layout="wide")
apply_custom_css()

st.title("📊 Executive Overview & Key Performance Indicators")
st.markdown(
    "High-level metrics and user segmentation evaluating consumer activity and tracking adherence across the 31-day study."
)
st.markdown("---")

# Query KPIs
try:
    kpi_query = """
    SELECT
        COUNT(DISTINCT Id) AS total_users,
        MIN(ActivityDate) AS start_date,
        MAX(ActivityDate) AS end_date,
        CAST(julianday(MAX(ActivityDate)) - julianday(MIN(ActivityDate)) + 1 AS INTEGER) AS study_days,
        ROUND(AVG(TotalSteps), 0) AS avg_daily_steps,
        ROUND(SUM(CASE WHEN TotalSteps >= 10000 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS pct_meeting_10k
    FROM clean_dailyActivity
    WHERE is_likely_nonwear = 0;
    """
    kpis = run_query(kpi_query).iloc[0]

    sleep_query = "SELECT ROUND(AVG(TotalMinutesAsleep) / 60.0, 2) AS avg_sleep_hours FROM clean_sleepDay;"
    avg_sleep = run_query(sleep_query).iloc[0, 0]
except Exception as e:
    st.error(f"Error querying overview metrics: {e}")
    st.stop()

# 5-card KPI row
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Total Users</div>
            <div class="metric-value">{int(kpis['total_users'])}</div>
            <div class="metric-sub">Active study cohort</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with k2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Date Range</div>
            <div class="metric-value" style="font-size: 1.3rem; padding-top: 6px;">{kpis['start_date']} &rarr; {kpis['end_date']}</div>
            <div class="metric-sub">{kpis['study_days']} total calendar days</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with k3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Avg Daily Steps</div>
            <div class="metric-value">{int(kpis['avg_daily_steps']):,}</div>
            <div class="metric-sub">Valid wear days</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with k4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Avg Sleep Duration</div>
            <div class="metric-value">{avg_sleep:.2f} hrs</div>
            <div class="metric-sub">410 nights tracked</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with k5:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">10k Goal Attainment</div>
            <div class="metric-value">{kpis['pct_meeting_10k']}%</div>
            <div class="metric-sub">CDC recommended step goal</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# Summary Charts Section
col_chart1, col_chart2 = st.columns([1, 1])

# User Segmentation Summary Chart
with col_chart1:
    st.subheader("👥 User Activity Segmentation")
    st.caption("Categorized by average daily steps on valid wear days (CDC benchmark: 10,000 steps/day)")
    
    seg_df = run_query("SELECT * FROM analysis_user_segments")
    seg_summary = (
        seg_df.groupby("activity_segment")
        .agg(user_count=("Id", "count"), mean_steps=("avg_daily_steps", "mean"))
        .reindex(["Heavy", "Moderate", "Light"])
        .reset_index()
    )

    fig_seg = px.pie(
        seg_summary,
        names="activity_segment",
        values="user_count",
        color="activity_segment",
        color_discrete_map={
            "Heavy": COLOR_PRIMARY,
            "Moderate": COLOR_SECONDARY,
            "Light": COLOR_ACCENT,
        },
        hole=0.45,
    )
    fig_seg.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hoverinfo="label+value+percent",
        marker=dict(line=dict(color="#ffffff", width=2)),
    )
    fig_seg.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        margin=dict(l=20, r=20, t=20, b=30),
    )
    st.plotly_chart(fig_seg, use_container_width=True)

# Daily Cohort Step Trend
with col_chart2:
    st.subheader("📈 Cohort Daily Steps Over Time")
    st.caption("31-day longitudinal step progression across all active participants")

    timeline_query = """
    SELECT
        ActivityDate,
        ROUND(AVG(TotalSteps), 0) AS avg_steps,
        COUNT(*) AS active_users
    FROM clean_dailyActivity
    WHERE is_likely_nonwear = 0
    GROUP BY ActivityDate
    ORDER BY ActivityDate;
    """
    time_df = run_query(timeline_query)

    fig_time = go.Figure()
    fig_time.add_trace(
        go.Scatter(
            x=time_df["ActivityDate"],
            y=time_df["avg_steps"],
            mode="lines+markers",
            line=dict(color=COLOR_PRIMARY, width=3),
            marker=dict(size=6, color=COLOR_DARK),
            name="Cohort Avg Steps",
        )
    )
    # Add 10,000 CDC reference line
    fig_time.add_hline(
        y=10000,
        line_dash="dot",
        line_color="#10B981",
        annotation_text="CDC 10k Goal",
        annotation_position="bottom right",
    )
    fig_time.update_layout(
        template="plotly_white",
        xaxis_title="Date",
        yaxis_title="Average Daily Steps",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig_time, use_container_width=True)

# Strategic Takeaways Box
st.markdown("---")
st.subheader("💡 Key Executive Insights")
st.markdown(
    """
    - **Adherence & Goal Achievement**: While participants average **8,280 steps/day**, users achieve the CDC 10,000 steps milestone on only **35.0%** of days. 
    - **Participant Diversity**: 57.6% of users (19/33) fall into the **Moderate** band (5,000–9,999 steps), representing Bellabeat's primary target for habit-forming motivational nudges.
    - **Healthy Sleep Baselines**: The cohort records an average of **6.99 hours** of sleep per night, right on the threshold of the CDC's recommended 7–9 hour healthy sleep window.
    """
)

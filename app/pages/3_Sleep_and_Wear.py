"""
Sleep and Wear Engagement Page for Bellabeat Fitness Analytics.
Features sleep duration distribution, tracker compliance rates,
and participant-level sedentary heatmaps.
"""

import sys
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Add app root to path for imports
app_dir = Path(__file__).resolve().parent.parent
if str(app_dir) not in sys.path:
    sys.path.insert(0, str(app_dir))

from utils import (
    COLOR_DARK,
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    apply_custom_css,
    run_query,
)

st.set_page_config(page_title="Sleep & Wear | Bellabeat Analytics", page_icon="🌙", layout="wide")
apply_custom_css()

st.title("🌙 Sleep Quality & Device Wear Engagement")
st.markdown(
    "Evaluation of nocturnal sleep patterns, tracker wear compliance, and participant-level sedentary time heatmaps."
)
st.markdown("---")

# 1. Sleep Analysis Section
st.subheader("💤 Sleep Duration Distribution")
st.caption("Derived from clean_sleepDay across 410 deduplicated nights logged by 24 participants")

col_sleep_chart, col_sleep_summary = st.columns([3, 1])

with col_sleep_chart:
    sleep_nights = run_query(
        """
        SELECT 
            Id,
            SleepDay,
            ROUND(TotalMinutesAsleep / 60.0, 2) AS sleep_hours,
            ROUND(TotalTimeInBed / 60.0, 2) AS bed_hours,
            (TotalTimeInBed - TotalMinutesAsleep) AS awake_in_bed_minutes
        FROM clean_sleepDay;
        """
    )

    fig_sleep = go.Figure()
    fig_sleep.add_trace(
        go.Histogram(
            x=sleep_nights["sleep_hours"],
            nbinsx=25,
            marker_color=COLOR_SECONDARY,
            opacity=0.8,
            name="Logged Nights",
            hovertemplate="Sleep: %{x:.1f} hrs<br>Count: %{y} nights<extra></extra>",
        )
    )
    # Add shaded rectangle for recommended 7-9 hours sleep range
    fig_sleep.add_vrect(
        x0=7.0,
        x1=9.0,
        fillcolor="rgba(16, 185, 129, 0.15)",
        layer="below",
        line_width=1,
        line_dash="dot",
        line_color="#10B981",
        annotation_text="Healthy 7–9h Sleep Window",
        annotation_position="top left",
    )
    fig_sleep.update_layout(
        template="plotly_white",
        xaxis_title="Hours Slept per Night",
        yaxis_title="Number of Nights",
        margin=dict(l=20, r=20, t=30, b=20),
    )
    st.plotly_chart(fig_sleep, use_container_width=True)

with col_sleep_summary:
    sleep_agg = run_query(
        """
        SELECT 
            ROUND(AVG(TotalMinutesAsleep) / 60.0, 2) AS avg_sleep,
            ROUND(AVG(TotalTimeInBed) / 60.0, 2) AS avg_bed,
            ROUND(AVG(TotalTimeInBed - TotalMinutesAsleep), 0) AS avg_awake
        FROM clean_sleepDay;
        """
    ).iloc[0]

    st.markdown(
        f"""
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:18px;">
            <h4 style="margin-top:0;">Sleep Health Snapshot</h4>
            <p><b>Average Sleep:</b> {sleep_agg['avg_sleep']:.2f} hrs/night</p>
            <p><b>Average Time in Bed:</b> {sleep_agg['avg_bed']:.2f} hrs/night</p>
            <p><b>Time Spent Awake:</b> {int(sleep_agg['avg_awake'])} min/night</p>
            <p><b>Sleep Efficiency:</b> {(sleep_agg['avg_sleep'] / sleep_agg['avg_bed'] * 100):.1f}%</p>
            <hr style="margin:10px 0;">
            <p style="font-size:0.85rem; color:#64748b;">
                Users spend on average 39 minutes awake in bed each night. Bellabeat can offer evening wind-down meditations to improve sleep latency.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# 2. Wear Engagement Section
st.subheader("⌚ Tracker Wear Compliance (Adherence %)")
st.caption("Percentage of days each participant logged valid activity during the 31-day study period")

wear_df = run_query("SELECT * FROM analysis_wear_engagement ORDER BY wear_pct DESC, valid_wear_days DESC")

fig_wear = go.Figure()
fig_wear.add_trace(
    go.Bar(
        x=[str(i) for i in wear_df["Id"]],
        y=wear_df["wear_pct"],
        marker_color=[
            COLOR_SECONDARY if pct >= 80 else (COLOR_PRIMARY if pct < 50 else COLOR_DARK)
            for pct in wear_df["wear_pct"]
        ],
        text=[f"{pct:.0f}%" for pct in wear_df["wear_pct"]],
        textposition="outside",
        hovertemplate="<b>Participant:</b> %{x}<br>Compliance: %{y:.1f}%<br>Days Worn: %{customdata[0]}/31<br>Non-Wear Days: %{customdata[1]}<extra></extra>",
        customdata=list(zip(wear_df["valid_wear_days"], wear_df["nonwear_days"])),
    )
)
fig_wear.add_hline(
    y=80,
    line_dash="dot",
    line_color="#10B981",
    annotation_text="High Adherence (>=80%)",
    annotation_position="bottom right",
)
fig_wear.update_layout(
    template="plotly_white",
    xaxis=dict(title="Participant ID", tickangle=-45),
    yaxis=dict(title="Wear Compliance (%)", range=[0, 115]),
    margin=dict(l=20, r=20, t=30, b=50),
)
st.plotly_chart(fig_wear, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# 3. Sedentary Heatmap by Participant
st.subheader("🔥 Participant Sedentary Time Heatmap")
st.caption("Average sedentary minutes per user across each weekday and overall grand total (built from analysis_sedentary_by_participant)")

sed_df = run_query("SELECT * FROM analysis_sedentary_by_participant")
weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Overall"]

# Pivot matrix: Index = Id, Columns = day_of_week
pivot_df = sed_df.pivot(index="Id", columns="day_of_week", values="avg_sedentary_minutes")[weekday_order]
pivot_df = pivot_df.sort_values(by="Overall", ascending=True)

fig_heat = go.Figure(
    data=go.Heatmap(
        z=pivot_df.values,
        x=weekday_order,
        y=[str(i) for i in pivot_df.index],
        colorscale="YlOrRd",
        colorbar=dict(title="Sedentary Min"),
        hovertemplate="<b>User:</b> %{y}<br><b>Day:</b> %{x}<br><b>Avg Sedentary:</b> %{z:.0f} min (~%{customdata:.1f} hrs)<extra></extra>",
        customdata=pivot_df.values / 60.0,
    )
)
fig_heat.update_layout(
    template="plotly_white",
    xaxis_title="Day of Week",
    yaxis_title="Participant ID (Sorted by Overall Sedentary Time)",
    height=750,
    margin=dict(l=20, r=20, t=30, b=30),
)
st.plotly_chart(fig_heat, use_container_width=True)

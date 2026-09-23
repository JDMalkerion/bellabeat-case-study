"""
Activity Analysis Page for Bellabeat Fitness Analytics.
Features Plotly visualizations for weekday steps, activity intensity minutes,
and hourly calorie expenditure, all sourced from analysis_ views.
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
    COLOR_ACCENT,
    COLOR_DARK,
    COLOR_FAIRLY_ACTIVE,
    COLOR_LIGHTLY_ACTIVE,
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    COLOR_SEDENTARY,
    COLOR_VERY_ACTIVE,
    apply_custom_css,
    run_query,
)

st.set_page_config(page_title="Activity | Bellabeat Analytics", page_icon="🏃", layout="wide")
apply_custom_css()

st.title("🏃 Physical Activity & Calorie Expenditure")
st.markdown(
    "Exploration of consumer movement patterns, active vs. sedentary intensity splits, and hourly metabolic curves."
)
st.markdown("---")

# 1. Weekday Steps & Calories
st.subheader("📅 Activity Trends by Day of Week")
st.caption("Derived from clean_dailyActivity on valid wear days (excluding non-wear)")

col_steps, col_cals = st.columns([1, 1])

with col_steps:
    steps_df = run_query("SELECT * FROM analysis_weekday_steps ORDER BY day_of_week_num")
    
    # Highlight highest step days (Tuesday and Saturday)
    colors = [
        COLOR_PRIMARY if day in ["Tuesday", "Saturday"] else "#CBD5E1"
        for day in steps_df["day_of_week"]
    ]

    fig_steps = go.Figure()
    fig_steps.add_trace(
        go.Bar(
            x=steps_df["day_of_week"],
            y=steps_df["avg_total_steps"],
            marker_color=colors,
            text=[f"{v:,.0f}" for v in steps_df["avg_total_steps"]],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Avg Steps: %{y:,.0f}<br>Logs: %{customdata}<extra></extra>",
            customdata=steps_df["record_count"],
        )
    )
    # Add CDC 10k guideline line
    fig_steps.add_hline(
        y=10000,
        line_dash="dash",
        line_color="#10B981",
        annotation_text="CDC 10,000 Step Benchmark",
        annotation_position="top right",
    )
    fig_steps.update_layout(
        title="Average Daily Steps by Weekday",
        template="plotly_white",
        yaxis=dict(title="Steps", range=[0, 11000]),
        xaxis_title="Day of Week",
        margin=dict(l=20, r=20, t=50, b=20),
    )
    st.plotly_chart(fig_steps, use_container_width=True)

with col_cals:
    cals_df = run_query("SELECT * FROM analysis_calories_by_weekday ORDER BY day_of_week_num")

    fig_cals = go.Figure()
    fig_cals.add_trace(
        go.Bar(
            x=cals_df["day_of_week"],
            y=cals_df["avg_calories"],
            marker_color=COLOR_SECONDARY,
            text=[f"{v:,.0f}" for v in cals_df["avg_calories"]],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Avg Calories: %{y:,.0f} kcal<br>Logs: %{customdata}<extra></extra>",
            customdata=cals_df["record_count"],
        )
    )
    fig_cals.update_layout(
        title="Average Calorie Expenditure by Weekday",
        template="plotly_white",
        yaxis=dict(title="Calories (kcal)", range=[1800, 2650]),
        xaxis_title="Day of Week",
        margin=dict(l=20, r=20, t=50, b=20),
    )
    st.plotly_chart(fig_cals, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# 2. Activity Minutes Breakdown
st.subheader("⏱️ Daily Intensity Composition (Minutes per Day)")
st.caption("Distribution across Very Active, Fairly Active, Lightly Active, and Sedentary categories")

mins_df = run_query("SELECT * FROM analysis_activity_minutes ORDER BY day_of_week_num")

col_mins_chart, col_mins_insight = st.columns([3, 1])

with col_mins_chart:
    fig_mins = go.Figure()
    fig_mins.add_trace(
        go.Bar(
            name="Very Active",
            x=mins_df["day_of_week"],
            y=mins_df["avg_very_active_minutes"],
            marker_color=COLOR_VERY_ACTIVE,
        )
    )
    fig_mins.add_trace(
        go.Bar(
            name="Fairly Active",
            x=mins_df["day_of_week"],
            y=mins_df["avg_fairly_active_minutes"],
            marker_color=COLOR_FAIRLY_ACTIVE,
        )
    )
    fig_mins.add_trace(
        go.Bar(
            name="Lightly Active",
            x=mins_df["day_of_week"],
            y=mins_df["avg_lightly_active_minutes"],
            marker_color=COLOR_LIGHTLY_ACTIVE,
        )
    )
    fig_mins.add_trace(
        go.Bar(
            name="Sedentary",
            x=mins_df["day_of_week"],
            y=mins_df["avg_sedentary_minutes"],
            marker_color=COLOR_SEDENTARY,
        )
    )
    fig_mins.update_layout(
        barmode="stack",
        template="plotly_white",
        yaxis_title="Minutes / Day (Total 1,440)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=40, b=20),
    )
    st.plotly_chart(fig_mins, use_container_width=True)

with col_mins_insight:
    avg_sed = mins_df["avg_sedentary_minutes"].mean()
    avg_light = mins_df["avg_lightly_active_minutes"].mean()
    avg_mod_very = mins_df["avg_fairly_active_minutes"].mean() + mins_df["avg_very_active_minutes"].mean()
    st.markdown(
        f"""
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:16px;">
            <h4 style="margin-top:0;">Intensity Split</h4>
            <p><b>Sedentary:</b> {avg_sed:.0f} min/day (~{avg_sed/60:.1f} hrs / 81.3%)</p>
            <p><b>Light Activity:</b> {avg_light:.0f} min/day (~{avg_light/60:.1f} hrs / 15.8%)</p>
            <p><b>Fairly + Very Active:</b> {avg_mod_very:.0f} min/day (~2.9%)</p>
            <hr style="margin:10px 0;">
            <p style="font-size:0.85rem; color:#64748b;">
                Participants spend over 16 hours a day sedentary, highlighting a massive opportunity for Bellabeat's periodic inactivity alerts.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# 3. Hourly Calories
st.subheader("🔥 Diurnal Metabolic Pattern (Calories by Hour of Day)")
st.caption("Sourced from analysis_hourly_calories across 22,099 hourly tracker records")

hour_df = run_query("SELECT * FROM analysis_hourly_calories ORDER BY hour_of_day")
hour_labels = [f"{h:02d}:00" for h in hour_df["hour_of_day"]]

fig_hour = go.Figure()
fig_hour.add_trace(
    go.Scatter(
        x=hour_labels,
        y=hour_df["avg_calories"],
        mode="lines+markers",
        fill="tozeroy",
        fillcolor="rgba(231, 111, 81, 0.15)",
        line=dict(color=COLOR_PRIMARY, width=3),
        marker=dict(size=6, color=COLOR_DARK),
        name="Avg Calories",
        hovertemplate="<b>%{x}</b><br>Burn: %{y:.1f} kcal<extra></extra>",
    )
)
# Annotate key peaks and resting troughs
fig_hour.add_annotation(
    x="12:00",
    y=hour_df.loc[hour_df["hour_of_day"] == 12, "avg_calories"].values[0],
    text="Lunch Peak (117 kcal)",
    showarrow=True,
    arrowhead=2,
    arrowcolor=COLOR_DARK,
    yshift=10,
)
fig_hour.add_annotation(
    x="18:00",
    y=hour_df.loc[hour_df["hour_of_day"] == 18, "avg_calories"].values[0],
    text="Evening Peak (123 kcal)",
    showarrow=True,
    arrowhead=2,
    arrowcolor=COLOR_DARK,
    yshift=10,
)
fig_hour.add_annotation(
    x="03:00",
    y=hour_df.loc[hour_df["hour_of_day"] == 3, "avg_calories"].values[0],
    text="Basal Resting (68 kcal)",
    showarrow=True,
    arrowhead=2,
    arrowcolor=COLOR_DARK,
    yshift=-15,
)
fig_hour.update_layout(
    template="plotly_white",
    xaxis_title="Hour of Day (24h clock)",
    yaxis_title="Average Calories Burned (kcal/hr)",
    margin=dict(l=20, r=20, t=30, b=20),
)
st.plotly_chart(fig_hour, use_container_width=True)

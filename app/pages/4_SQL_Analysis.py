"""
SQL Analysis & View Explorer for Bellabeat Fitness Analytics.
Inspects all 8 analytical views, displays their live SQL definitions parsed from 03_analysis.sql,
shows interactive dataframes and charts, and provides an interactive read-only SQL workbench.
"""

import sys
import time
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
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    apply_custom_css,
    get_db_connection,
    get_sql_definition,
    run_query,
)

st.set_page_config(page_title="SQL Analysis | Bellabeat Analytics", page_icon="🔍", layout="wide")
apply_custom_css()

st.title("🔍 SQL Analytical Views & Interactive Console")
st.markdown(
    "Explore the 8 analytical SQL views backing this portal. Inspect the underlying SQL definitions, view data tables, and run custom read-only SQL queries."
)
st.markdown("---")

VIEW_LIST = [
    ("Weekday Steps", "analysis_weekday_steps"),
    ("Activity Intensity Minutes", "analysis_activity_minutes"),
    ("Calories by Weekday", "analysis_calories_by_weekday"),
    ("Sedentary by Participant", "analysis_sedentary_by_participant"),
    ("Hourly Calories", "analysis_hourly_calories"),
    ("Sleep Duration", "analysis_sleep_duration"),
    ("Wear Engagement", "analysis_wear_engagement"),
    ("User Segmentation", "analysis_user_segments"),
]

st.subheader("📋 Analytical Views Inspector")

selected_view_tuple = st.selectbox(
    "Select an Analytical View to Inspect:",
    VIEW_LIST,
    format_func=lambda x: f"{x[0]} ({x[1]})",
)
view_label, view_name = selected_view_tuple

# Display Tabs for SQL Code, Data Table, and Chart
tab_sql, tab_data, tab_chart = st.tabs(["📝 SQL Definition", "📄 Data Table", "📊 Interactive Chart"])

sql_text = get_sql_definition(view_name)
view_df = run_query(f"SELECT * FROM {view_name}")

with tab_sql:
    st.caption(f"Source: sql/03_analysis.sql &rarr; View: {view_name}")
    st.code(sql_text, language="sql")

with tab_data:
    st.caption(f"Rows returned: {len(view_df):,} | Columns: {len(view_df.columns)}")
    st.dataframe(view_df, use_container_width=True)

with tab_chart:
    st.caption(f"Visual representation of {view_name}")
    if view_name == "analysis_weekday_steps":
        fig = px.bar(
            view_df,
            x="day_of_week",
            y="avg_total_steps",
            color="avg_total_steps",
            color_continuous_scale="Blues",
            title="Avg Steps by Weekday",
        )
        st.plotly_chart(fig, use_container_width=True)
    elif view_name == "analysis_activity_minutes":
        fig = px.bar(
            view_df,
            x="day_of_week",
            y=[
                "avg_very_active_minutes",
                "avg_fairly_active_minutes",
                "avg_lightly_active_minutes",
                "avg_sedentary_minutes",
            ],
            barmode="stack",
            title="Activity Minutes Distribution",
        )
        st.plotly_chart(fig, use_container_width=True)
    elif view_name == "analysis_calories_by_weekday":
        fig = px.bar(
            view_df,
            x="day_of_week",
            y="avg_calories",
            color_discrete_sequence=[COLOR_PRIMARY],
            title="Avg Calories by Weekday",
        )
        st.plotly_chart(fig, use_container_width=True)
    elif view_name == "analysis_sedentary_by_participant":
        overall_only = view_df[view_df["day_of_week"] == "Overall"].sort_values(
            "avg_sedentary_minutes", ascending=True
        )
        fig = px.bar(
            overall_only,
            x=[str(i) for i in overall_only["Id"]],
            y="avg_sedentary_minutes",
            color="avg_sedentary_minutes",
            color_continuous_scale="Reds",
            title="Overall Average Sedentary Minutes per Participant",
        )
        fig.update_layout(xaxis_title="Participant ID", xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    elif view_name == "analysis_hourly_calories":
        fig = px.line(
            view_df,
            x="hour_of_day",
            y="avg_calories",
            markers=True,
            title="Diurnal Metabolic Curve (Calories by Hour)",
        )
        fig.update_traces(line_color=COLOR_PRIMARY)
        st.plotly_chart(fig, use_container_width=True)
    elif view_name == "analysis_sleep_duration":
        part_only = view_df[view_df["Id"] != "Overall"].sort_values(
            "avg_sleep_hours", ascending=True
        )
        fig = px.bar(
            part_only,
            x="Id",
            y="avg_sleep_hours",
            color="avg_sleep_hours",
            color_continuous_scale="Teal",
            title="Average Sleep Duration (Hours) by Participant",
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    elif view_name == "analysis_wear_engagement":
        fig = px.bar(
            view_df,
            x=[str(i) for i in view_df["Id"]],
            y="wear_pct",
            color="wear_pct",
            color_continuous_scale="Viridis",
            title="Device Wear Compliance (%) Across 31 Days",
        )
        fig.update_layout(xaxis_title="Participant ID", xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    elif view_name == "analysis_user_segments":
        fig = px.pie(
            view_df,
            names="activity_segment",
            title="User Segmentation Share",
            color="activity_segment",
            color_discrete_map={
                "Heavy": COLOR_PRIMARY,
                "Moderate": COLOR_SECONDARY,
                "Light": COLOR_ACCENT,
            },
        )
        st.plotly_chart(fig, use_container_width=True)

st.markdown("<br><hr>", unsafe_allow_html=True)

# Bottom Section: Read-Only Custom Query Console
st.subheader("💻 Interactive Read-Only SQL Workbench")
st.caption(
    "Execute custom SQL queries directly against sql/bellabeat.db in read-only mode (`mode=ro`). Modifications and DDL are strictly blocked by SQLite."
)

default_query = """SELECT 
    Id, 
    avg_daily_steps, 
    valid_days_tracked, 
    activity_segment 
FROM analysis_user_segments 
ORDER BY avg_daily_steps DESC 
LIMIT 10;"""

user_query = st.text_area("Custom SQL Query (SELECT only):", value=default_query, height=120)

col_run, col_clear = st.columns([1, 8])
with col_run:
    execute_button = st.button("▶ Run Query", type="primary")

if execute_button:
    clean_q = user_query.strip()
    if not clean_q:
        st.warning("Please enter a SQL query.")
    else:
        conn = get_db_connection()
        t0 = time.time()
        try:
            custom_df = run_query(clean_q)
            elapsed = (time.time() - t0) * 1000
            st.success(f"Query returned {len(custom_df):,} rows in {elapsed:.1f}ms")
            st.dataframe(custom_df, use_container_width=True)
        except Exception as err:
            st.error(f"SQL Error: {err}")
        finally:
            conn.close()

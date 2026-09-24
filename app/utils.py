"""
Shared utilities for the Bellabeat Fitness Analytics Streamlit App.
Provides read-only SQLite database connection, query execution with caching,
view SQL extraction from 03_analysis.sql, and modern theme styling.
"""

import re
import sqlite3
from pathlib import Path
import pandas as pd
import streamlit as st

REPO_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = REPO_ROOT / "sql" / "bellabeat_deploy.db" if (REPO_ROOT / "sql" / "bellabeat_deploy.db").exists() else REPO_ROOT / "sql" / "bellabeat.db"
ANALYSIS_SQL_PATH = REPO_ROOT / "sql" / "03_analysis.sql"

# Brand colors inspired by Bellabeat's warm aesthetic
COLOR_PRIMARY = "#E76F51"       # Warm Coral
COLOR_SECONDARY = "#2A9D8F"     # Teal
COLOR_ACCENT = "#F4A261"        # Soft Amber
COLOR_DARK = "#264653"          # Deep Slate
COLOR_MUTED = "#6C757D"
COLOR_LIGHT = "#FAEDCD"
COLOR_VERY_ACTIVE = "#E76F51"
COLOR_FAIRLY_ACTIVE = "#F4A261"
COLOR_LIGHTLY_ACTIVE = "#2A9D8F"
COLOR_SEDENTARY = "#4A5568"


def get_db_connection() -> sqlite3.Connection:
    """Return a read-only SQLite connection using URI mode=ro."""
    db_uri = f"file:{DB_PATH.resolve()}?mode=ro"
    return sqlite3.connect(db_uri, uri=True)


@st.cache_data(show_spinner=False)
def run_query(query: str) -> pd.DataFrame:
    """Execute a read-only SQL query against sql/bellabeat.db and return a DataFrame."""
    conn = get_db_connection()
    try:
        return pd.read_sql_query(query, conn)
    finally:
        conn.close()


def get_sql_definition(view_name: str) -> str:
    """Extract CREATE VIEW definition for a view from sql/03_analysis.sql."""
    if not ANALYSIS_SQL_PATH.exists():
        return f"-- File not found: {ANALYSIS_SQL_PATH}"
    sql_text = ANALYSIS_SQL_PATH.read_text(encoding="utf-8")
    pattern = rf"(CREATE VIEW {view_name}\s+AS[\s\S]*?;)"
    match = re.search(pattern, sql_text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return f"-- Definition for {view_name} not found in {ANALYSIS_SQL_PATH.name}"


def apply_custom_css():
    """Apply styling for metric cards and typography."""
    st.markdown(
        """
        <style>
        .metric-card {
            background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 18px 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            text-align: left;
            transition: transform 0.15s ease-in-out;
        }
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 12px -1px rgba(0, 0, 0, 0.08);
        }
        .metric-title {
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #6b7280;
            margin-bottom: 6px;
            font-weight: 600;
        }
        .metric-value {
            font-size: 1.85rem;
            font-weight: 700;
            color: #1f2937;
            line-height: 1.2;
        }
        .metric-sub {
            font-size: 0.8rem;
            color: #9ca3af;
            margin-top: 4px;
        }
        .badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .badge-coral {
            background-color: #fee2e2;
            color: #b91c1c;
        }
        .badge-teal {
            background-color: #ccfbf1;
            color: #0f766e;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

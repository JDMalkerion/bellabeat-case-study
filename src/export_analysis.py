#!/usr/bin/env python3
"""
Export Script for Bellabeat Analytical Views.
Exports each analysis_* view from sql/bellabeat.db into exports/<view_name>.csv
for downstream Power BI reporting.
"""

import sqlite3
from pathlib import Path
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
SQL_DIR = REPO_ROOT / "sql"
DB_PATH = SQL_DIR / "bellabeat.db"
EXPORTS_DIR = REPO_ROOT / "exports"

ANALYSIS_VIEWS = [
    "analysis_weekday_steps",
    "analysis_activity_minutes",
    "analysis_calories_by_weekday",
    "analysis_sedentary_by_participant",
    "analysis_hourly_calories",
    "analysis_sleep_duration",
    "analysis_wear_engagement",
    "analysis_user_segments",
]


def export_views():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        print("Exporting analytical views to exports/ ...")
        for view_name in ANALYSIS_VIEWS:
            df = pd.read_sql(f"SELECT * FROM {view_name}", conn)
            out_file = EXPORTS_DIR / f"{view_name}.csv"
            df.to_csv(out_file, index=False)
            print(f"  Exported {view_name:<35}: {len(df):>5} rows -> {out_file.name}")
        print("All analytical views exported successfully.")
    finally:
        conn.close()


if __name__ == "__main__":
    export_views()

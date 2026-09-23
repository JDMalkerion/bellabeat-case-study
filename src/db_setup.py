#!/usr/bin/env python3
"""
Database Setup & CSV Ingestion Script for Bellabeat Fitness Data.
Creates sql/bellabeat.db, executes sql/01_schema.sql, and loads all 10 CSV files
from data/ into SQLite with date/datetime fields parsed to ISO 8601 strings.
Safe to re-run (idempotent).
"""

import os
import sqlite3
import time
from pathlib import Path
import pandas as pd

# Define paths relative to repository root
REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
SQL_DIR = REPO_ROOT / "sql"
DB_PATH = SQL_DIR / "bellabeat.db"
SCHEMA_PATH = SQL_DIR / "01_schema.sql"

# Configurations for table loading
# Input date formats:
#   Daily files: %m/%d/%Y
#   Hourly / Seconds / Weight: %m/%d/%Y %I:%M:%S %p
#   sleepDay: %m/%d/%Y %I:%M:%S %p (verified in CSV: values end in '12:00:00 AM')
TABLE_CONFIGS = [
    {
        "table": "dailyActivity",
        "csv": "dailyActivity_merged.csv",
        "date_col": "ActivityDate",
        "input_format": "%m/%d/%Y",
        "output_format": "%Y-%m-%d",
    },
    {
        "table": "dailyCalories",
        "csv": "dailyCalories_merged.csv",
        "date_col": "ActivityDay",
        "input_format": "%m/%d/%Y",
        "output_format": "%Y-%m-%d",
    },
    {
        "table": "dailyIntensities",
        "csv": "dailyIntensities_merged.csv",
        "date_col": "ActivityDay",
        "input_format": "%m/%d/%Y",
        "output_format": "%Y-%m-%d",
    },
    {
        "table": "dailySteps",
        "csv": "dailySteps_merged.csv",
        "date_col": "ActivityDay",
        "input_format": "%m/%d/%Y",
        "output_format": "%Y-%m-%d",
    },
    {
        "table": "sleepDay",
        "csv": "sleepDay_merged.csv",
        "date_col": "SleepDay",
        "input_format": "%m/%d/%Y %I:%M:%S %p",
        "output_format": "%Y-%m-%d",
    },
    {
        "table": "hourlyCalories",
        "csv": "hourlyCalories_merged.csv",
        "date_col": "ActivityHour",
        "input_format": "%m/%d/%Y %I:%M:%S %p",
        "output_format": "%Y-%m-%d %H:%M:%S",
    },
    {
        "table": "hourlyIntensities",
        "csv": "hourlyIntensities_merged.csv",
        "date_col": "ActivityHour",
        "input_format": "%m/%d/%Y %I:%M:%S %p",
        "output_format": "%Y-%m-%d %H:%M:%S",
    },
    {
        "table": "hourlySteps",
        "csv": "hourlySteps_merged.csv",
        "date_col": "ActivityHour",
        "input_format": "%m/%d/%Y %I:%M:%S %p",
        "output_format": "%Y-%m-%d %H:%M:%S",
    },
    {
        "table": "heartrate_seconds",
        "csv": "heartrate_seconds_merged.csv",
        "date_col": "Time",
        "input_format": "%m/%d/%Y %I:%M:%S %p",
        "output_format": "%Y-%m-%d %H:%M:%S",
    },
    {
        "table": "weightLogInfo",
        "csv": "weightLogInfo_merged.csv",
        "date_col": "Date",
        "input_format": "%m/%d/%Y %I:%M:%S %p",
        "output_format": "%Y-%m-%d %H:%M:%S",
    },
]


def init_db(conn: sqlite3.Connection) -> None:
    """Initialize or reset tables using sql/01_schema.sql."""
    print(f"Applying schema from {SCHEMA_PATH.name}...")
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)
    conn.commit()
    print("Schema applied successfully.")


def load_tables(conn: sqlite3.Connection) -> dict[str, int]:
    """Load all configured CSVs into SQLite tables."""
    counts = {}
    total_start = time.time()

    for config in TABLE_CONFIGS:
        table_name = config["table"]
        csv_path = DATA_DIR / config["csv"]
        date_col = config["date_col"]
        in_fmt = config["input_format"]
        out_fmt = config["output_format"]

        print(f"Loading {config['csv']} -> {table_name}...", end=" ", flush=True)
        t0 = time.time()

        # Read CSV
        df = pd.read_csv(csv_path)

        # Parse date column to ISO 8601 string
        df[date_col] = pd.to_datetime(df[date_col], format=in_fmt).dt.strftime(out_fmt)

        # Handle booleans (e.g. IsManualReport in weightLogInfo)
        if "IsManualReport" in df.columns:
            df["IsManualReport"] = df["IsManualReport"].astype(int)

        # Append data to pre-created table
        df.to_sql(
            table_name,
            conn,
            if_exists="append",
            index=False,
            chunksize=100000,
        )

        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        counts[table_name] = row_count
        elapsed = time.time() - t0
        print(f"{row_count:,} rows ({elapsed:.2f}s)")

    print(f"All tables loaded in {time.time() - total_start:.2f}s.\n")
    return counts


def main():
    print("=== Bellabeat Database Setup ===")
    print(f"Target database: {DB_PATH}")

    # Connect to SQLite
    conn = sqlite3.connect(DB_PATH)
    try:
        init_db(conn)
        row_counts = load_tables(conn)

        print("=== Ingestion Summary ===")
        for tbl, count in row_counts.items():
            print(f"  {tbl:<20}: {count:>10,} rows")
        print("Database setup complete.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()

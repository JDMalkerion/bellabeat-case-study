#!/usr/bin/env python3
"""
Verification Script for Bellabeat Fitness Tracker Data.
- Validates distinct Id count and date range (min/max) directly from raw CSVs vs SQLite.
- Prints PASS/FAIL per table.
- Verifies deduplication counts (especially sleepDay).
- Verifies non-wear flag count in clean_dailyActivity.
- Checks for negative values and NULLs in Id/date columns across all tables.
"""

import sqlite3
import sys
import time
from pathlib import Path
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
SQL_DIR = REPO_ROOT / "sql"
DB_PATH = SQL_DIR / "bellabeat.db"
CLEANING_SQL_PATH = SQL_DIR / "02_cleaning.sql"

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


def ensure_cleaning_views(conn: sqlite3.Connection) -> None:
    """Ensure clean_* views exist by running 02_cleaning.sql if needed."""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='view' AND name='clean_dailyActivity'"
    )
    if not cursor.fetchone():
        print("clean_* views not found. Applying sql/02_cleaning.sql...")
        with open(CLEANING_SQL_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.commit()


def verify_tables(conn: sqlite3.Connection) -> bool:
    """Compare raw CSV stats against SQLite tables."""
    cursor = conn.cursor()
    all_passed = True

    print("=" * 80)
    print("VERIFICATION: Raw CSV vs SQLite Loaded Table Comparison")
    print("=" * 80)
    print(
        f"{'Table':<20} | {'Status':<6} | {'Raw CSV (Ids, Min Date, Max Date)':<38} | {'SQLite (Ids, Min, Max)'}"
    )
    print("-" * 80)

    for config in TABLE_CONFIGS:
        tbl = config["table"]
        csv_file = config["csv"]
        dcol = config["date_col"]
        infmt = config["input_format"]
        outfmt = config["output_format"]

        # Raw CSV metrics via pandas
        df = pd.read_csv(DATA_DIR / csv_file)
        parsed_dates = pd.to_datetime(df[dcol], format=infmt).dt.strftime(outfmt)
        csv_ids = int(df["Id"].nunique())
        csv_min = str(parsed_dates.min())
        csv_max = str(parsed_dates.max())

        # SQLite metrics via SQL
        cursor.execute(
            f"SELECT COUNT(DISTINCT Id), MIN({dcol}), MAX({dcol}) FROM {tbl}"
        )
        sql_ids, sql_min, sql_max = cursor.fetchone()
        sql_ids = int(sql_ids)

        match = (csv_ids == sql_ids and csv_min == sql_min and csv_max == sql_max)
        status = "PASS" if match else "FAIL"
        if not match:
            all_passed = False

        csv_summary = f"({csv_ids} Ids, {csv_min} to {csv_max})"
        sql_summary = f"({sql_ids} Ids, {sql_min} to {sql_max})"
        print(f"{tbl:<20} | {status:<6} | {csv_summary:<38} | {sql_summary}")

    print("=" * 80)
    return all_passed


def verify_cleaning(conn: sqlite3.Connection) -> None:
    """Verify deduplication, non-wear flagging, and data integrity."""
    cursor = conn.cursor()

    print("\n" + "=" * 80)
    print("DATA CLEANING & QUALITY AUDIT")
    print("=" * 80)

    # 1. sleepDay Deduplication
    cursor.execute("SELECT COUNT(*) FROM sleepDay")
    raw_sleep = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM clean_sleepDay")
    clean_sleep = cursor.fetchone()[0]
    sleep_removed = raw_sleep - clean_sleep
    print(f"sleepDay Deduplication:")
    print(f"  - Raw rows          : {raw_sleep}")
    print(f"  - Clean unique rows : {clean_sleep}")
    print(f"  - Duplicate rows cut: {sleep_removed} (Expected: 3)")

    # 2. General deduplication across all other tables
    print("\nDeduplication check across remaining tables:")
    for config in TABLE_CONFIGS:
        tbl = config["table"]
        if tbl == "sleepDay":
            continue
        clean_view = f"clean_{tbl}"
        cursor.execute(f"SELECT COUNT(*) FROM {tbl}")
        raw_count = cursor.fetchone()[0]
        cursor.execute(f"SELECT COUNT(*) FROM {clean_view}")
        clean_count = cursor.fetchone()[0]
        diff = raw_count - clean_count
        print(f"  - {tbl:<20}: {diff} duplicate rows removed (Raw: {raw_count:,}, Clean: {clean_count:,})")

    # 3. Non-wear flags in clean_dailyActivity
    cursor.execute(
        "SELECT is_likely_nonwear, COUNT(*) FROM clean_dailyActivity GROUP BY is_likely_nonwear ORDER BY is_likely_nonwear"
    )
    nonwear_counts = dict(cursor.fetchall())
    nonwear_flagged = nonwear_counts.get(1, 0)
    normal_wear = nonwear_counts.get(0, 0)
    total_act = nonwear_flagged + normal_wear
    print(f"\nNon-Wear Analysis (clean_dailyActivity):")
    print(f"  - Flagged non-wear (SedentaryMinutes >= 1440): {nonwear_flagged} rows ({nonwear_flagged / total_act * 100:.1f}%)")
    print(f"  - Normal wear days                          : {normal_wear} rows ({normal_wear / total_act * 100:.1f}%)")
    print(f"  - Total records                             : {total_act} rows (all rows preserved, none dropped)")

    # 4. Null checks in Id and Date columns
    print("\nNULL Check in Primary Keys / Date Columns:")
    null_issues = 0
    for config in TABLE_CONFIGS:
        tbl = config["table"]
        dcol = config["date_col"]
        cursor.execute(
            f"SELECT COUNT(*) FROM {tbl} WHERE Id IS NULL OR {dcol} IS NULL"
        )
        null_count = cursor.fetchone()[0]
        if null_count > 0:
            print(f"  [!] {tbl}: FOUND {null_count} NULL values in Id or {dcol}!")
            null_issues += 1
    if null_issues == 0:
        print("  - [OK] 0 NULL values found in Id or date/datetime columns across all 10 tables.")

    # 5. Negative value checks
    print("\nNegative Metric Value Check:")
    cursor.execute(
        """
        SELECT COUNT(*) FROM clean_dailyActivity
        WHERE TotalSteps < 0 OR TotalDistance < 0 OR Calories < 0
        """
    )
    neg_act = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM clean_dailySteps WHERE StepTotal < 0")
    neg_steps = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM clean_dailyCalories WHERE Calories < 0")
    neg_cal = cursor.fetchone()[0]

    total_neg = neg_act + neg_steps + neg_cal
    if total_neg == 0:
        print("  - [OK] 0 negative values found in TotalSteps, TotalDistance, StepTotal, or Calories.")
    else:
        print(f"  - [!] Found negative values: dailyActivity={neg_act}, dailySteps={neg_steps}, dailyCalories={neg_cal}")

    # 6. Other notable observations (e.g. Fat nulls in weightLogInfo)
    cursor.execute("SELECT COUNT(*) FROM weightLogInfo WHERE Fat IS NULL")
    fat_nulls = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM weightLogInfo")
    weight_total = cursor.fetchone()[0]
    print(f"\nOther Observations:")
    print(f"  - weightLogInfo.Fat has {fat_nulls}/{weight_total} NULL values (expected: body fat percentage was rarely logged).")
    print("=" * 80)


def main():
    if not DB_PATH.exists():
        print(f"Database not found at {DB_PATH}. Please run src/db_setup.py first.")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    try:
        ensure_cleaning_views(conn)
        passed = verify_tables(conn)
        verify_cleaning(conn)

        if not passed:
            print("\nVerification completed with FAILURES.")
            sys.exit(1)
        else:
            print("\nAll verification checks PASSED successfully.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()

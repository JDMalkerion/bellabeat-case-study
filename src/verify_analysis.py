#!/usr/bin/env python3
"""
Verification Script for Bellabeat Analytical Views.
Independently recomputes all 8 analytical queries in pandas directly from raw CSVs
(including computing non-wear exclusion in pandas), compares against SQL view outputs,
and prints side-by-side numerical comparison tables with PASS/FAIL status.
"""

import sqlite3
import sys
from pathlib import Path
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
SQL_DIR = REPO_ROOT / "sql"
DB_PATH = SQL_DIR / "bellabeat.db"
ANALYSIS_SQL_PATH = SQL_DIR / "03_analysis.sql"


def ensure_analysis_views(conn: sqlite3.Connection) -> None:
    """Ensure analysis_* views exist in database."""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='view' AND name='analysis_weekday_steps'"
    )
    if not cursor.fetchone():
        print("Applying sql/03_analysis.sql...")
        with open(ANALYSIS_SQL_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.commit()


def verify_weekday_steps(conn: sqlite3.Connection) -> bool:
    print("\n--- 1. analysis_weekday_steps ---")
    sql_df = pd.read_sql("SELECT * FROM analysis_weekday_steps", conn)

    raw_act = pd.read_csv(DATA_DIR / "dailyActivity_merged.csv")
    raw_act["is_nonwear"] = (raw_act["SedentaryMinutes"] >= 1440).astype(int)
    raw_act["dt"] = pd.to_datetime(raw_act["ActivityDate"], format="%m/%d/%Y")
    raw_act["day_of_week"] = raw_act["dt"].dt.day_name()
    raw_act["day_of_week_num"] = raw_act["dt"].dt.dayofweek + 1

    pd_df = (
        raw_act[raw_act["is_nonwear"] == 0]
        .groupby(["day_of_week", "day_of_week_num"])
        .agg(
            avg_total_steps=("TotalSteps", lambda x: round(x.mean(), 2)),
            record_count=("TotalSteps", "count"),
        )
        .reset_index()
        .sort_values("day_of_week_num")
        .reset_index(drop=True)
    )

    merged = pd.merge(
        sql_df,
        pd_df,
        on=["day_of_week", "day_of_week_num"],
        suffixes=("_sql", "_pandas"),
    )
    print(
        f"{'Day':<12} | {'SQL Steps':<10} | {'Pandas Steps':<12} | {'SQL Count':<10} | {'Pandas Count'}"
    )
    print("-" * 65)
    for _, r in merged.iterrows():
        print(
            f"{r['day_of_week']:<12} | {r['avg_total_steps_sql']:<10.2f} | {r['avg_total_steps_pandas']:<12.2f} | {r['record_count_sql']:<10} | {r['record_count_pandas']}"
        )

    passed = np.allclose(
        merged["avg_total_steps_sql"], merged["avg_total_steps_pandas"]
    ) and list(merged["record_count_sql"]) == list(merged["record_count_pandas"])
    print(f"Status: {'PASS' if passed else 'FAIL'}")
    return passed


def verify_activity_minutes(conn: sqlite3.Connection) -> bool:
    print("\n--- 2. analysis_activity_minutes ---")
    sql_df = pd.read_sql("SELECT * FROM analysis_activity_minutes", conn)

    raw_act = pd.read_csv(DATA_DIR / "dailyActivity_merged.csv")
    raw_act["dt"] = pd.to_datetime(raw_act["ActivityDate"], format="%m/%d/%Y")
    raw_act["day_of_week"] = raw_act["dt"].dt.day_name()
    raw_act["day_of_week_num"] = raw_act["dt"].dt.dayofweek + 1

    pd_df = (
        raw_act.groupby(["day_of_week", "day_of_week_num"])
        .agg(
            avg_very_active_minutes=("VeryActiveMinutes", lambda x: round(x.mean(), 2)),
            avg_fairly_active_minutes=("FairlyActiveMinutes", lambda x: round(x.mean(), 2)),
            avg_lightly_active_minutes=("LightlyActiveMinutes", lambda x: round(x.mean(), 2)),
            avg_sedentary_minutes=("SedentaryMinutes", lambda x: round(x.mean(), 2)),
            total_records=("TotalSteps", "count"),
        )
        .reset_index()
        .sort_values("day_of_week_num")
        .reset_index(drop=True)
    )

    merged = pd.merge(
        sql_df,
        pd_df,
        on=["day_of_week", "day_of_week_num"],
        suffixes=("_sql", "_pandas"),
    )
    print(
        f"{'Day':<10} | {'VeryAct(SQL/PD)':<16} | {'Fairly(SQL/PD)':<16} | {'Lightly(SQL/PD)':<16} | {'Sedentary(SQL/PD)'}"
    )
    print("-" * 75)
    for _, r in merged.iterrows():
        v = f"{r['avg_very_active_minutes_sql']:.1f}/{r['avg_very_active_minutes_pandas']:.1f}"
        f = f"{r['avg_fairly_active_minutes_sql']:.1f}/{r['avg_fairly_active_minutes_pandas']:.1f}"
        l = f"{r['avg_lightly_active_minutes_sql']:.1f}/{r['avg_lightly_active_minutes_pandas']:.1f}"
        s = f"{r['avg_sedentary_minutes_sql']:.1f}/{r['avg_sedentary_minutes_pandas']:.1f}"
        print(f"{r['day_of_week']:<10} | {v:<16} | {f:<16} | {l:<16} | {s}")

    passed = (
        np.allclose(
            merged["avg_very_active_minutes_sql"],
            merged["avg_very_active_minutes_pandas"],
        )
        and np.allclose(
            merged["avg_fairly_active_minutes_sql"],
            merged["avg_fairly_active_minutes_pandas"],
        )
        and np.allclose(
            merged["avg_lightly_active_minutes_sql"],
            merged["avg_lightly_active_minutes_pandas"],
        )
        and np.allclose(
            merged["avg_sedentary_minutes_sql"],
            merged["avg_sedentary_minutes_pandas"],
        )
        and list(merged["total_records_sql"]) == list(merged["total_records_pandas"])
    )
    print(f"Status: {'PASS' if passed else 'FAIL'}")
    return passed


def verify_calories_by_weekday(conn: sqlite3.Connection) -> bool:
    print("\n--- 3. analysis_calories_by_weekday ---")
    sql_df = pd.read_sql("SELECT * FROM analysis_calories_by_weekday", conn)

    raw_act = pd.read_csv(DATA_DIR / "dailyActivity_merged.csv")
    raw_act["is_nonwear"] = (raw_act["SedentaryMinutes"] >= 1440).astype(int)
    raw_act["dt"] = pd.to_datetime(raw_act["ActivityDate"], format="%m/%d/%Y")
    raw_act["day_of_week"] = raw_act["dt"].dt.day_name()
    raw_act["day_of_week_num"] = raw_act["dt"].dt.dayofweek + 1

    pd_df = (
        raw_act[raw_act["is_nonwear"] == 0]
        .groupby(["day_of_week", "day_of_week_num"])
        .agg(
            avg_calories=("Calories", lambda x: round(x.mean(), 2)),
            record_count=("Calories", "count"),
        )
        .reset_index()
        .sort_values("day_of_week_num")
        .reset_index(drop=True)
    )

    merged = pd.merge(
        sql_df,
        pd_df,
        on=["day_of_week", "day_of_week_num"],
        suffixes=("_sql", "_pandas"),
    )
    print(
        f"{'Day':<12} | {'SQL Calories':<14} | {'Pandas Calories':<16} | {'Match'}"
    )
    print("-" * 55)
    for _, r in merged.iterrows():
        match = abs(r["avg_calories_sql"] - r["avg_calories_pandas"]) < 0.01
        print(
            f"{r['day_of_week']:<12} | {r['avg_calories_sql']:<14.2f} | {r['avg_calories_pandas']:<16.2f} | {match}"
        )

    passed = np.allclose(
        merged["avg_calories_sql"], merged["avg_calories_pandas"]
    ) and list(merged["record_count_sql"]) == list(merged["record_count_pandas"])
    print(f"Status: {'PASS' if passed else 'FAIL'}")
    return passed


def verify_sedentary_by_participant(conn: sqlite3.Connection) -> bool:
    print("\n--- 4. analysis_sedentary_by_participant ---")
    sql_df = pd.read_sql("SELECT * FROM analysis_sedentary_by_participant", conn)

    raw_act = pd.read_csv(DATA_DIR / "dailyActivity_merged.csv")
    raw_act["is_nonwear"] = (raw_act["SedentaryMinutes"] >= 1440).astype(int)
    raw_act["dt"] = pd.to_datetime(raw_act["ActivityDate"], format="%m/%d/%Y")
    raw_act["day_of_week"] = raw_act["dt"].dt.day_name()
    raw_act["day_of_week_num"] = raw_act["dt"].dt.dayofweek + 1

    pd_wd = (
        raw_act.groupby(["Id", "day_of_week", "day_of_week_num"])
        .agg(
            avg_sedentary_minutes=("SedentaryMinutes", lambda x: round(x.mean(), 2)),
            total_days=("SedentaryMinutes", "count"),
            nonwear_days=("is_nonwear", "sum"),
        )
        .reset_index()
    )

    pd_ov = (
        raw_act.groupby("Id")
        .agg(
            avg_sedentary_minutes=("SedentaryMinutes", lambda x: round(x.mean(), 2)),
            total_days=("SedentaryMinutes", "count"),
            nonwear_days=("is_nonwear", "sum"),
        )
        .reset_index()
    )
    pd_ov["day_of_week"] = "Overall"
    pd_ov["day_of_week_num"] = 8

    pd_combined = pd.concat([pd_wd, pd_ov], ignore_index=True)
    merged = pd.merge(
        sql_df,
        pd_combined,
        on=["Id", "day_of_week", "day_of_week_num"],
        suffixes=("_sql", "_pandas"),
    )

    passed = (
        len(sql_df) == len(pd_combined)
        and np.allclose(
            merged["avg_sedentary_minutes_sql"], merged["avg_sedentary_minutes_pandas"]
        )
        and list(merged["total_days_sql"]) == list(merged["total_days_pandas"])
        and list(merged["nonwear_days_sql"]) == list(merged["nonwear_days_pandas"])
    )
    print(f"Total participant-slice rows compared: {len(merged)}")
    sample = merged.sample(5, random_state=42)
    for _, r in sample.iterrows():
        print(
            f"  Id {r['Id']} ({r['day_of_week']:<7}): SQL={r['avg_sedentary_minutes_sql']:.1f}m vs PD={r['avg_sedentary_minutes_pandas']:.1f}m | Days={r['total_days_sql']} (Nonwear={r['nonwear_days_sql']})"
        )
    print(f"Status: {'PASS' if passed else 'FAIL'}")
    return passed


def verify_hourly_calories(conn: sqlite3.Connection) -> bool:
    print("\n--- 5. analysis_hourly_calories ---")
    sql_df = pd.read_sql("SELECT * FROM analysis_hourly_calories", conn)

    raw_hc = pd.read_csv(DATA_DIR / "hourlyCalories_merged.csv")
    raw_hc["dt"] = pd.to_datetime(
        raw_hc["ActivityHour"], format="%m/%d/%Y %I:%M:%S %p"
    )
    raw_hc["hour_of_day"] = raw_hc["dt"].dt.hour

    pd_df = (
        raw_hc.groupby("hour_of_day")
        .agg(
            avg_calories=("Calories", lambda x: round(x.mean(), 2)),
            record_count=("Calories", "count"),
        )
        .reset_index()
        .sort_values("hour_of_day")
        .reset_index(drop=True)
    )

    merged = pd.merge(sql_df, pd_df, on="hour_of_day", suffixes=("_sql", "_pandas"))
    print(f"Sample hours comparison (0, 6, 12, 18, 23):")
    sample_hours = [0, 6, 12, 18, 23]
    for _, r in merged[merged["hour_of_day"].isin(sample_hours)].iterrows():
        print(
            f"  Hour {int(r['hour_of_day']):02d}:00 | SQL={r['avg_calories_sql']:<6.2f} cal | Pandas={r['avg_calories_pandas']:<6.2f} cal | Count={r['record_count_sql']}"
        )

    passed = np.allclose(
        merged["avg_calories_sql"], merged["avg_calories_pandas"]
    ) and list(merged["record_count_sql"]) == list(merged["record_count_pandas"])
    print(f"Status: {'PASS' if passed else 'FAIL'}")
    return passed


def verify_sleep_duration(conn: sqlite3.Connection) -> bool:
    print("\n--- 6. analysis_sleep_duration ---")
    sql_df = pd.read_sql("SELECT * FROM analysis_sleep_duration", conn)

    raw_sl = pd.read_csv(DATA_DIR / "sleepDay_merged.csv").drop_duplicates().copy()
    raw_sl["sleep_hours"] = raw_sl["TotalMinutesAsleep"] / 60.0
    raw_sl["bed_hours"] = raw_sl["TotalTimeInBed"] / 60.0

    pd_part = (
        raw_sl.groupby("Id")
        .agg(
            avg_sleep_hours=("sleep_hours", lambda x: round(x.mean(), 2)),
            avg_time_in_bed_hours=("bed_hours", lambda x: round(x.mean(), 2)),
            nights_logged=("TotalSleepRecords", "count"),
        )
        .reset_index()
    )
    pd_part["Id"] = pd_part["Id"].astype(str)

    pd_tot = pd.DataFrame(
        [
            {
                "Id": "Overall",
                "avg_sleep_hours": round(raw_sl["sleep_hours"].mean(), 2),
                "avg_time_in_bed_hours": round(raw_sl["bed_hours"].mean(), 2),
                "nights_logged": len(raw_sl),
            }
        ]
    )
    pd_df = pd.concat([pd_part, pd_tot], ignore_index=True)

    merged = pd.merge(sql_df, pd_df, on="Id", suffixes=("_sql", "_pandas"))
    overall = merged[merged["Id"] == "Overall"].iloc[0]
    print(
        f"Overall Sleep: SQL={overall['avg_sleep_hours_sql']}h (Bed: {overall['avg_time_in_bed_hours_sql']}h, Nights: {overall['nights_logged_sql']}) | Pandas={overall['avg_sleep_hours_pandas']}h (Bed: {overall['avg_time_in_bed_hours_pandas']}h, Nights: {overall['nights_logged_pandas']})"
    )

    passed = np.allclose(
        merged["avg_sleep_hours_sql"], merged["avg_sleep_hours_pandas"]
    ) and list(merged["nights_logged_sql"]) == list(merged["nights_logged_pandas"])
    print(f"Status: {'PASS' if passed else 'FAIL'}")
    return passed


def verify_wear_engagement(conn: sqlite3.Connection) -> bool:
    print("\n--- 7. analysis_wear_engagement ---")
    sql_df = pd.read_sql("SELECT * FROM analysis_wear_engagement", conn)

    raw_act = pd.read_csv(DATA_DIR / "dailyActivity_merged.csv")
    raw_act["is_nonwear"] = (raw_act["SedentaryMinutes"] >= 1440).astype(int)
    raw_act["dt"] = pd.to_datetime(raw_act["ActivityDate"], format="%m/%d/%Y")
    total_study_days = (raw_act["dt"].max() - raw_act["dt"].min()).days + 1

    pd_df = (
        raw_act.groupby("Id")
        .agg(
            days_logged=("ActivityDate", "count"),
            valid_wear_days=("is_nonwear", lambda x: (x == 0).sum()),
            nonwear_days=("is_nonwear", "sum"),
        )
        .reset_index()
    )
    pd_df["total_study_days"] = total_study_days
    pd_df["wear_pct"] = (pd_df["days_logged"] / total_study_days * 100.0).round(2)
    pd_df = pd_df.sort_values(by=["wear_pct", "Id"], ascending=[False, True]).reset_index(
        drop=True
    )

    merged = pd.merge(sql_df, pd_df, on="Id", suffixes=("_sql", "_pandas"))
    passed = (
        list(sql_df["Id"]) == list(pd_df["Id"])
        and list(merged["days_logged_sql"]) == list(merged["days_logged_pandas"])
        and np.allclose(merged["wear_pct_sql"], merged["wear_pct_pandas"])
    )
    print(
        f"Mean adherence: SQL={sql_df['wear_pct'].mean():.1f}% vs Pandas={pd_df['wear_pct'].mean():.1f}% across {len(sql_df)} users"
    )
    print(f"Status: {'PASS' if passed else 'FAIL'}")
    return passed


def verify_user_segments(conn: sqlite3.Connection) -> bool:
    print("\n--- 8. analysis_user_segments ---")
    sql_df = pd.read_sql("SELECT * FROM analysis_user_segments", conn)

    raw_act = pd.read_csv(DATA_DIR / "dailyActivity_merged.csv")
    raw_act["is_nonwear"] = (raw_act["SedentaryMinutes"] >= 1440).astype(int)

    pd_df = (
        raw_act[raw_act["is_nonwear"] == 0]
        .groupby("Id")
        .agg(
            avg_daily_steps=("TotalSteps", lambda x: round(x.mean(), 2)),
            valid_days_tracked=("TotalSteps", "count"),
        )
        .reset_index()
    )

    def segment(s):
        if s >= 10000:
            return "Heavy"
        if s < 5000:
            return "Light"
        return "Moderate"

    pd_df["activity_segment"] = pd_df["avg_daily_steps"].apply(segment)
    pd_df = pd_df.sort_values(by="avg_daily_steps", ascending=False).reset_index(
        drop=True
    )

    merged = pd.merge(sql_df, pd_df, on="Id", suffixes=("_sql", "_pandas"))
    print("User Segment Distribution:")
    sql_dist = sql_df["activity_segment"].value_counts().to_dict()
    pd_dist = pd_df["activity_segment"].value_counts().to_dict()
    for k in ["Heavy", "Moderate", "Light"]:
        print(f"  {k:<10}: SQL={sql_dist.get(k, 0)} users | Pandas={pd_dist.get(k, 0)} users")

    passed = (
        list(sql_df["Id"]) == list(pd_df["Id"])
        and np.allclose(merged["avg_daily_steps_sql"], merged["avg_daily_steps_pandas"])
        and list(merged["activity_segment_sql"]) == list(merged["activity_segment_pandas"])
    )
    print(f"Status: {'PASS' if passed else 'FAIL'}")
    return passed


def main():
    print("=" * 70)
    print("INDEPENDENT VERIFICATION OF ANALYTICAL VIEWS (Raw CSV vs SQLite)")
    print("=" * 70)

    if not DB_PATH.exists():
        print(f"Database not found at {DB_PATH}. Please run src/db_setup.py first.")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    try:
        ensure_analysis_views(conn)
        results = {
            "analysis_weekday_steps": verify_weekday_steps(conn),
            "analysis_activity_minutes": verify_activity_minutes(conn),
            "analysis_calories_by_weekday": verify_calories_by_weekday(conn),
            "analysis_sedentary_by_participant": verify_sedentary_by_participant(conn),
            "analysis_hourly_calories": verify_hourly_calories(conn),
            "analysis_sleep_duration": verify_sleep_duration(conn),
            "analysis_wear_engagement": verify_wear_engagement(conn),
            "analysis_user_segments": verify_user_segments(conn),
        }

        print("\n" + "=" * 70)
        print("OVERALL VERIFICATION SUMMARY")
        print("=" * 70)
        all_passed = True
        for query_name, ok in results.items():
            status = "PASS" if ok else "FAIL"
            print(f"  {query_name:<35}: {status}")
            if not ok:
                all_passed = False

        print("=" * 70)
        if all_passed:
            print("ALL 8 ANALYTICAL VIEWS PASSED INDEPENDENT VERIFICATION.")
        else:
            print("ONE OR MORE VERIFICATION CHECKS FAILED.")
            sys.exit(1)
    finally:
        conn.close()


if __name__ == "__main__":
    main()

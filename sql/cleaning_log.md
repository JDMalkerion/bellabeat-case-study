# Bellabeat Data Cleaning Log

**Date**: 2026-09-22  
**Database**: `sql/bellabeat.db`  
**Scripts**: `src/db_setup.py`, `sql/02_cleaning.sql`, `src/verify.py`

---

## 1. Summary of Loaded Tables & Row Counts

The raw CSV files from `data/` were ingested into SQLite tables via `src/db_setup.py`.

| Table Name | Source CSV File | Raw Rows Loaded | Clean Rows (Views) | Duplicates Removed |
| :--- | :--- | :--- | :--- | :--- |
| `dailyActivity` | `dailyActivity_merged.csv` | 940 | 940 | 0 |
| `dailyCalories` | `dailyCalories_merged.csv` | 940 | 940 | 0 |
| `dailyIntensities` | `dailyIntensities_merged.csv` | 940 | 940 | 0 |
| `dailySteps` | `dailySteps_merged.csv` | 940 | 940 | 0 |
| `sleepDay` | `sleepDay_merged.csv` | 413 | 410 | **3** |
| `hourlyCalories` | `hourlyCalories_merged.csv` | 22,099 | 22,099 | 0 |
| `hourlyIntensities` | `hourlyIntensities_merged.csv` | 22,099 | 22,099 | 0 |
| `hourlySteps` | `hourlySteps_merged.csv` | 22,099 | 22,099 | 0 |
| `heartrate_seconds` | `heartrate_seconds_merged.csv` | 2,483,658 | 2,483,658 | 0 |
| `weightLogInfo` | `weightLogInfo_merged.csv` | 67 | 67 | 0 |
| **Total** | | **2,532,495** | **2,532,492** | **3** |

---

## 2. Actual User Coverage & Date Ranges

> [!IMPORTANT]
> **User Count Discrepancy**: The Mobius dataset description states the survey tracked "30 eligible Fitbit users". The actual dataset contains **33 distinct user IDs** in the daily and hourly activity tables. Furthermore, tracking adherence differs drastically across features: only **24 users** recorded sleep, **14 users** recorded second-level heart rate, and only **8 users** recorded weight logs (with 5 of those 8 recording 2 or fewer times).

| Table Name | Date Column | Distinct Users (`Id`) | Date Range (Min to Max) | Time Granularity |
| :--- | :--- | :--- | :--- | :--- |
| `dailyActivity` | `ActivityDate` | **33** | `2016-04-12` to `2016-05-12` | Daily |
| `dailyCalories` | `ActivityDay` | **33** | `2016-04-12` to `2016-05-12` | Daily |
| `dailyIntensities` | `ActivityDay` | **33** | `2016-04-12` to `2016-05-12` | Daily |
| `dailySteps` | `ActivityDay` | **33** | `2016-04-12` to `2016-05-12` | Daily |
| `sleepDay` | `SleepDay` | **24** | `2016-04-12` to `2016-05-12` | Daily |
| `hourlyCalories` | `ActivityHour` | **33** | `2016-04-12 00:00:00` to `2016-05-12 15:00:00` | Hourly |
| `hourlyIntensities` | `ActivityHour` | **33** | `2016-04-12 00:00:00` to `2016-05-12 15:00:00` | Hourly |
| `hourlySteps` | `ActivityHour` | **33** | `2016-04-12 00:00:00` to `2016-05-12 15:00:00` | Hourly |
| `heartrate_seconds` | `Time` | **14** | `2016-04-12 00:00:00` to `2016-05-12 16:20:00` | Sub-minute |
| `weightLogInfo` | `Date` | **8** | `2016-04-12 06:47:11` to `2016-05-12 23:59:59` | Log timestamp |

---

## 3. Deduplication

- **`sleepDay` Deduplication**:
  - Raw rows: **413**
  - Clean distinct rows: **410**
  - Removed duplicate rows: **3**
  - Duplicate rows identified in raw data:
    - `Id: 4388161847`, `SleepDay: 5/5/2016 12:00:00 AM`, `TotalSleepRecords: 1`, `TotalMinutesAsleep: 471`, `TotalTimeInBed: 495` (2 occurrences)
    - `Id: 4702921684`, `SleepDay: 5/7/2016 12:00:00 AM`, `TotalSleepRecords: 1`, `TotalMinutesAsleep: 520`, `TotalTimeInBed: 543` (2 occurrences)
    - `Id: 8378563200`, `SleepDay: 4/25/2016 12:00:00 AM`, `TotalSleepRecords: 1`, `TotalMinutesAsleep: 388`, `TotalTimeInBed: 402` (2 occurrences)
- **Other Tables**:
  - Checked for exact duplicate rows across all 9 other tables: **0 duplicate rows found**.

---

## 4. Non-Wear Day Identification (`clean_dailyActivity`)

A non-wear day is defined as a full 24-hour cycle of sedentary time (`SedentaryMinutes >= 1440` minutes). These occur when the user removed the tracker (e.g. left on a nightstand or desk) but the device continued logging default sedentary minutes.

- **Non-wear rows flagged (`is_likely_nonwear = 1`)**: **79** rows (8.4% of total daily activity logs)
- **Normal active/wear rows (`is_likely_nonwear = 0`)**: **861** rows (91.6%)
- **Handling Strategy**: Non-wear rows are **preserved** with the binary flag in `clean_dailyActivity`, allowing downstream analytics to either filter them out or study compliance / tracking dropout rates without data loss.

---

## 5. Data Integrity & Validation Checks

- **NULL Checks**:
  - `Id` column: **0** NULLs across all 10 tables.
  - Date / datetime columns: **0** NULLs across all 10 tables.
  - Only `weightLogInfo.Fat` contains NULLs (**65** out of 67 rows lack body fat percentage, indicating manual entry of body fat was rarely used by participants).
- **Negative Value Checks**:
  - `TotalSteps`: **0** negative values.
  - `TotalDistance`: **0** negative values.
  - `Calories`: **0** negative values.
  - `StepTotal`: **0** negative values.
- **Date Formatting**:
  - All daily dates normalized to ISO 8601 `YYYY-MM-DD`.
  - All timestamps normalized to ISO 8601 `YYYY-MM-DD HH:MM:SS`.

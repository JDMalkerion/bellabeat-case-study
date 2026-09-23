-- ==============================================================================
-- Bellabeat Fitness Tracker Data - Data Cleaning & Views
-- Database: sql/bellabeat.db
--
-- Creates clean_* views for all 10 tables:
--   1. Deduplication: exact duplicate rows removed via SELECT DISTINCT
--      (specifically handles the 3 duplicate rows in sleepDay).
--   2. Non-wear identification: flags 24-hour inactivity in clean_dailyActivity
--      (is_likely_nonwear = 1 when SedentaryMinutes >= 1440, without dropping).
--   3. Data integrity: verifies no negative metrics and no NULLs in Id/date.
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. clean_dailyActivity
-- Includes non-wear flag (is_likely_nonwear = 1 where SedentaryMinutes >= 1440)
-- ------------------------------------------------------------------------------
DROP VIEW IF EXISTS clean_dailyActivity;
CREATE VIEW clean_dailyActivity AS
SELECT DISTINCT
    Id,
    ActivityDate,
    TotalSteps,
    TotalDistance,
    TrackerDistance,
    LoggedActivitiesDistance,
    VeryActiveDistance,
    ModeratelyActiveDistance,
    LightActiveDistance,
    SedentaryActiveDistance,
    VeryActiveMinutes,
    FairlyActiveMinutes,
    LightlyActiveMinutes,
    SedentaryMinutes,
    Calories,
    CASE
        WHEN SedentaryMinutes >= 1440 THEN 1
        ELSE 0
    END AS is_likely_nonwear
FROM dailyActivity;

-- ------------------------------------------------------------------------------
-- 2. clean_dailyCalories
-- ------------------------------------------------------------------------------
DROP VIEW IF EXISTS clean_dailyCalories;
CREATE VIEW clean_dailyCalories AS
SELECT DISTINCT
    Id,
    ActivityDay,
    Calories
FROM dailyCalories;

-- ------------------------------------------------------------------------------
-- 3. clean_dailyIntensities
-- ------------------------------------------------------------------------------
DROP VIEW IF EXISTS clean_dailyIntensities;
CREATE VIEW clean_dailyIntensities AS
SELECT DISTINCT
    Id,
    ActivityDay,
    SedentaryMinutes,
    LightlyActiveMinutes,
    FairlyActiveMinutes,
    VeryActiveMinutes,
    SedentaryActiveDistance,
    LightActiveDistance,
    ModeratelyActiveDistance,
    VeryActiveDistance
FROM dailyIntensities;

-- ------------------------------------------------------------------------------
-- 4. clean_dailySteps
-- ------------------------------------------------------------------------------
DROP VIEW IF EXISTS clean_dailySteps;
CREATE VIEW clean_dailySteps AS
SELECT DISTINCT
    Id,
    ActivityDay,
    StepTotal
FROM dailySteps;

-- ------------------------------------------------------------------------------
-- 5. clean_sleepDay
-- Removes 3 duplicate rows (from 413 to 410 unique rows)
-- ------------------------------------------------------------------------------
DROP VIEW IF EXISTS clean_sleepDay;
CREATE VIEW clean_sleepDay AS
SELECT DISTINCT
    Id,
    SleepDay,
    TotalSleepRecords,
    TotalMinutesAsleep,
    TotalTimeInBed
FROM sleepDay;

-- ------------------------------------------------------------------------------
-- 6. clean_hourlyCalories
-- ------------------------------------------------------------------------------
DROP VIEW IF EXISTS clean_hourlyCalories;
CREATE VIEW clean_hourlyCalories AS
SELECT DISTINCT
    Id,
    ActivityHour,
    Calories
FROM hourlyCalories;

-- ------------------------------------------------------------------------------
-- 7. clean_hourlyIntensities
-- ------------------------------------------------------------------------------
DROP VIEW IF EXISTS clean_hourlyIntensities;
CREATE VIEW clean_hourlyIntensities AS
SELECT DISTINCT
    Id,
    ActivityHour,
    TotalIntensity,
    AverageIntensity
FROM hourlyIntensities;

-- ------------------------------------------------------------------------------
-- 8. clean_hourlySteps
-- ------------------------------------------------------------------------------
DROP VIEW IF EXISTS clean_hourlySteps;
CREATE VIEW clean_hourlySteps AS
SELECT DISTINCT
    Id,
    ActivityHour,
    StepTotal
FROM hourlySteps;

-- ------------------------------------------------------------------------------
-- 9. clean_heartrate_seconds
-- ------------------------------------------------------------------------------
DROP VIEW IF EXISTS clean_heartrate_seconds;
CREATE VIEW clean_heartrate_seconds AS
SELECT DISTINCT
    Id,
    Time,
    Value
FROM heartrate_seconds;

-- ------------------------------------------------------------------------------
-- 10. clean_weightLogInfo
-- ------------------------------------------------------------------------------
DROP VIEW IF EXISTS clean_weightLogInfo;
CREATE VIEW clean_weightLogInfo AS
SELECT DISTINCT
    Id,
    Date,
    WeightKg,
    WeightPounds,
    Fat,
    BMI,
    IsManualReport,
    LogId
FROM weightLogInfo;

-- ==============================================================================
-- Data Quality Verification Queries
-- (Can be executed interactively or via SQLite scripts)
-- ==============================================================================

-- Deduplication summary for sleepDay
-- Raw: 413 rows, Clean: 410 rows, Duplicates removed: 3
-- SELECT
--     (SELECT COUNT(*) FROM sleepDay) AS raw_sleep_rows,
--     (SELECT COUNT(*) FROM clean_sleepDay) AS clean_sleep_rows,
--     ((SELECT COUNT(*) FROM sleepDay) - (SELECT COUNT(*) FROM clean_sleepDay)) AS duplicates_removed;

-- Non-wear flag count in dailyActivity
-- Expected: 79 rows flagged with is_likely_nonwear = 1
-- SELECT
--     is_likely_nonwear,
--     COUNT(*) AS row_count
-- FROM clean_dailyActivity
-- GROUP BY is_likely_nonwear;

-- Negative value check across core activity metrics (expected: 0 rows)
-- SELECT COUNT(*) AS negative_metric_rows
-- FROM clean_dailyActivity
-- WHERE TotalSteps < 0 OR TotalDistance < 0 OR Calories < 0;

-- NULL check on Id and date columns across tables (expected: 0 rows)
-- SELECT 'dailyActivity' AS tbl, COUNT(*) AS null_count FROM dailyActivity WHERE Id IS NULL OR ActivityDate IS NULL
-- UNION ALL
-- SELECT 'sleepDay', COUNT(*) FROM sleepDay WHERE Id IS NULL OR SleepDay IS NULL;

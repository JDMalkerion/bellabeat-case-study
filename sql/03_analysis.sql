-- ==============================================================================
-- Bellabeat Fitness Tracker Data - Analytical Views
-- Database: sql/bellabeat.db
--
-- Contains 8 analytical views prefixed with analysis_:
--   1. analysis_weekday_steps: Avg steps by weekday (excluding non-wear)
--   2. analysis_activity_minutes: Avg active/sedentary minutes by weekday
--   3. analysis_calories_by_weekday: Avg calories by weekday (excluding non-wear)
--   4. analysis_sedentary_by_participant: Sedentary minutes per participant by weekday + overall
--   5. analysis_hourly_calories: Avg calories by hour of day (0-23)
--   6. analysis_sleep_duration: Avg sleep and bed hours per participant + overall
--   7. analysis_wear_engagement: Wear compliance % vs 31-day study period
--   8. analysis_user_segments: CDC step segmentation (Light <5k, Moderate 5k-10k, Heavy >=10k)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. analysis_weekday_steps
-- Average steps by day of week, excluding likely non-wear days (SedentaryMinutes >= 1440)
-- ------------------------------------------------------------------------------
DROP VIEW IF EXISTS analysis_weekday_steps;
CREATE VIEW analysis_weekday_steps AS
SELECT
    CASE CAST(strftime('%w', ActivityDate) AS INTEGER)
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END AS day_of_week,
    (CAST(strftime('%w', ActivityDate) AS INTEGER) + 6) % 7 + 1 AS day_of_week_num,
    ROUND(AVG(TotalSteps), 2) AS avg_total_steps,
    COUNT(*) AS record_count
FROM clean_dailyActivity
WHERE is_likely_nonwear = 0
GROUP BY day_of_week, day_of_week_num
ORDER BY day_of_week_num;

-- ------------------------------------------------------------------------------
-- 2. analysis_activity_minutes
-- Average activity minutes by category across weekdays (includes all days to capture full sedentary profile)
-- ------------------------------------------------------------------------------
DROP VIEW IF EXISTS analysis_activity_minutes;
CREATE VIEW analysis_activity_minutes AS
SELECT
    CASE CAST(strftime('%w', ActivityDate) AS INTEGER)
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END AS day_of_week,
    (CAST(strftime('%w', ActivityDate) AS INTEGER) + 6) % 7 + 1 AS day_of_week_num,
    ROUND(AVG(VeryActiveMinutes), 2) AS avg_very_active_minutes,
    ROUND(AVG(FairlyActiveMinutes), 2) AS avg_fairly_active_minutes,
    ROUND(AVG(LightlyActiveMinutes), 2) AS avg_lightly_active_minutes,
    ROUND(AVG(SedentaryMinutes), 2) AS avg_sedentary_minutes,
    COUNT(*) AS total_records
FROM clean_dailyActivity
GROUP BY day_of_week, day_of_week_num
ORDER BY day_of_week_num;

-- ------------------------------------------------------------------------------
-- 3. analysis_calories_by_weekday
-- Average calories burned by day of week, excluding likely non-wear days
-- ------------------------------------------------------------------------------
DROP VIEW IF EXISTS analysis_calories_by_weekday;
CREATE VIEW analysis_calories_by_weekday AS
SELECT
    CASE CAST(strftime('%w', ActivityDate) AS INTEGER)
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END AS day_of_week,
    (CAST(strftime('%w', ActivityDate) AS INTEGER) + 6) % 7 + 1 AS day_of_week_num,
    ROUND(AVG(Calories), 2) AS avg_calories,
    COUNT(*) AS record_count
FROM clean_dailyActivity
WHERE is_likely_nonwear = 0
GROUP BY day_of_week, day_of_week_num
ORDER BY day_of_week_num;

-- ------------------------------------------------------------------------------
-- 4. analysis_sedentary_by_participant
-- Average sedentary minutes per participant by weekday + overall grand total,
-- reporting both all-day averages and valid wear-only averages, with non-wear days flagged
-- ------------------------------------------------------------------------------
DROP VIEW IF EXISTS analysis_sedentary_by_participant;
CREATE VIEW analysis_sedentary_by_participant AS
WITH participant_weekday AS (
    SELECT
        Id,
        CASE CAST(strftime('%w', ActivityDate) AS INTEGER)
            WHEN 0 THEN 'Sunday'
            WHEN 1 THEN 'Monday'
            WHEN 2 THEN 'Tuesday'
            WHEN 3 THEN 'Wednesday'
            WHEN 4 THEN 'Thursday'
            WHEN 5 THEN 'Friday'
            WHEN 6 THEN 'Saturday'
        END AS day_of_week,
        (CAST(strftime('%w', ActivityDate) AS INTEGER) + 6) % 7 + 1 AS day_of_week_num,
        ROUND(AVG(SedentaryMinutes), 2) AS avg_sedentary_minutes,
        ROUND(AVG(CASE WHEN is_likely_nonwear = 0 THEN SedentaryMinutes END), 2) AS avg_sedentary_wear_only,
        COUNT(*) AS total_days,
        SUM(is_likely_nonwear) AS nonwear_days
    FROM clean_dailyActivity
    GROUP BY Id, day_of_week, day_of_week_num
),
participant_overall AS (
    SELECT
        Id,
        'Overall' AS day_of_week,
        8 AS day_of_week_num,
        ROUND(AVG(SedentaryMinutes), 2) AS avg_sedentary_minutes,
        ROUND(AVG(CASE WHEN is_likely_nonwear = 0 THEN SedentaryMinutes END), 2) AS avg_sedentary_wear_only,
        COUNT(*) AS total_days,
        SUM(is_likely_nonwear) AS nonwear_days
    FROM clean_dailyActivity
    GROUP BY Id
)
SELECT * FROM participant_weekday
UNION ALL
SELECT * FROM participant_overall
ORDER BY Id, day_of_week_num;

-- ------------------------------------------------------------------------------
-- 5. analysis_hourly_calories
-- Average calories burned by hour of day (0 to 23)
-- ------------------------------------------------------------------------------
DROP VIEW IF EXISTS analysis_hourly_calories;
CREATE VIEW analysis_hourly_calories AS
SELECT
    CAST(strftime('%H', ActivityHour) AS INTEGER) AS hour_of_day,
    ROUND(AVG(Calories), 2) AS avg_calories,
    COUNT(*) AS record_count
FROM clean_hourlyCalories
GROUP BY hour_of_day
ORDER BY hour_of_day;

-- ------------------------------------------------------------------------------
-- 6. analysis_sleep_duration
-- Average sleep and time in bed converted from minutes to hours, per participant and overall
-- ------------------------------------------------------------------------------
DROP VIEW IF EXISTS analysis_sleep_duration;
CREATE VIEW analysis_sleep_duration AS
SELECT
    CAST(Id AS TEXT) AS Id,
    ROUND(AVG(TotalMinutesAsleep) / 60.0, 2) AS avg_sleep_hours,
    ROUND(AVG(TotalTimeInBed) / 60.0, 2) AS avg_time_in_bed_hours,
    ROUND(AVG(TotalMinutesAsleep), 2) AS avg_sleep_minutes,
    ROUND(AVG(TotalTimeInBed), 2) AS avg_bed_minutes,
    COUNT(*) AS nights_logged
FROM clean_sleepDay
GROUP BY Id
UNION ALL
SELECT
    'Overall' AS Id,
    ROUND(AVG(TotalMinutesAsleep) / 60.0, 2) AS avg_sleep_hours,
    ROUND(AVG(TotalTimeInBed) / 60.0, 2) AS avg_time_in_bed_hours,
    ROUND(AVG(TotalMinutesAsleep), 2) AS avg_sleep_minutes,
    ROUND(AVG(TotalTimeInBed), 2) AS avg_bed_minutes,
    COUNT(*) AS nights_logged
FROM clean_sleepDay;

-- ------------------------------------------------------------------------------
-- 7. analysis_wear_engagement
-- Total days logged vs overall dataset date range (31 days) as a compliance percentage
-- ------------------------------------------------------------------------------
DROP VIEW IF EXISTS analysis_wear_engagement;
CREATE VIEW analysis_wear_engagement AS
WITH date_bounds AS (
    SELECT
        CAST(julianday(MAX(ActivityDate)) - julianday(MIN(ActivityDate)) + 1 AS INTEGER) AS total_study_days
    FROM clean_dailyActivity
)
SELECT
    c.Id,
    COUNT(c.ActivityDate) AS days_logged,
    b.total_study_days,
    ROUND(CAST(COUNT(c.ActivityDate) AS REAL) / b.total_study_days * 100.0, 2) AS wear_pct,
    SUM(CASE WHEN c.is_likely_nonwear = 0 THEN 1 ELSE 0 END) AS valid_wear_days,
    SUM(c.is_likely_nonwear) AS nonwear_days
FROM clean_dailyActivity c
CROSS JOIN date_bounds b
GROUP BY c.Id, b.total_study_days
ORDER BY wear_pct DESC, c.Id;

-- ------------------------------------------------------------------------------
-- 8. analysis_user_segments
-- Activity segments based on average daily steps on valid wear days:
--   - Heavy: >= 10,000 steps (CDC recommended daily benchmark)
--   - Moderate: 5,000 - 9,999 steps
--   - Light: < 5,000 steps
-- ------------------------------------------------------------------------------
DROP VIEW IF EXISTS analysis_user_segments;
CREATE VIEW analysis_user_segments AS
SELECT
    Id,
    ROUND(AVG(TotalSteps), 2) AS avg_daily_steps,
    COUNT(*) AS valid_days_tracked,
    CASE
        WHEN AVG(TotalSteps) >= 10000 THEN 'Heavy'
        WHEN AVG(TotalSteps) < 5000 THEN 'Light'
        ELSE 'Moderate'
    END AS activity_segment
FROM clean_dailyActivity
WHERE is_likely_nonwear = 0
GROUP BY Id
ORDER BY avg_daily_steps DESC;

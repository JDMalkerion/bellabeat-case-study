-- ==============================================================================
-- Bellabeat Fitness Tracker Data - SQLite Database Schema
-- Database: sql/bellabeat.db
--
-- Contains CREATE TABLE statements for the 10 core Fitbit dataset tables.
-- Date/datetime values are stored as TEXT in ISO 8601 standard formatting:
--   - Daily tables: 'YYYY-MM-DD'
--   - Hourly / Second / Weight tables: 'YYYY-MM-DD HH:MM:SS'
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- Source: data/dailyActivity_merged.csv
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS dailyActivity;
CREATE TABLE dailyActivity (
    Id INTEGER NOT NULL,
    ActivityDate TEXT NOT NULL,
    TotalSteps INTEGER NOT NULL,
    TotalDistance REAL NOT NULL,
    TrackerDistance REAL NOT NULL,
    LoggedActivitiesDistance REAL NOT NULL,
    VeryActiveDistance REAL NOT NULL,
    ModeratelyActiveDistance REAL NOT NULL,
    LightActiveDistance REAL NOT NULL,
    SedentaryActiveDistance REAL NOT NULL,
    VeryActiveMinutes INTEGER NOT NULL,
    FairlyActiveMinutes INTEGER NOT NULL,
    LightlyActiveMinutes INTEGER NOT NULL,
    SedentaryMinutes INTEGER NOT NULL,
    Calories INTEGER NOT NULL
);

-- ------------------------------------------------------------------------------
-- Source: data/dailyCalories_merged.csv
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS dailyCalories;
CREATE TABLE dailyCalories (
    Id INTEGER NOT NULL,
    ActivityDay TEXT NOT NULL,
    Calories INTEGER NOT NULL
);

-- ------------------------------------------------------------------------------
-- Source: data/dailyIntensities_merged.csv
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS dailyIntensities;
CREATE TABLE dailyIntensities (
    Id INTEGER NOT NULL,
    ActivityDay TEXT NOT NULL,
    SedentaryMinutes INTEGER NOT NULL,
    LightlyActiveMinutes INTEGER NOT NULL,
    FairlyActiveMinutes INTEGER NOT NULL,
    VeryActiveMinutes INTEGER NOT NULL,
    SedentaryActiveDistance REAL NOT NULL,
    LightActiveDistance REAL NOT NULL,
    ModeratelyActiveDistance REAL NOT NULL,
    VeryActiveDistance REAL NOT NULL
);

-- ------------------------------------------------------------------------------
-- Source: data/dailySteps_merged.csv
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS dailySteps;
CREATE TABLE dailySteps (
    Id INTEGER NOT NULL,
    ActivityDay TEXT NOT NULL,
    StepTotal INTEGER NOT NULL
);

-- ------------------------------------------------------------------------------
-- Source: data/hourlyCalories_merged.csv
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS hourlyCalories;
CREATE TABLE hourlyCalories (
    Id INTEGER NOT NULL,
    ActivityHour TEXT NOT NULL,
    Calories INTEGER NOT NULL
);

-- ------------------------------------------------------------------------------
-- Source: data/hourlyIntensities_merged.csv
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS hourlyIntensities;
CREATE TABLE hourlyIntensities (
    Id INTEGER NOT NULL,
    ActivityHour TEXT NOT NULL,
    TotalIntensity INTEGER NOT NULL,
    AverageIntensity REAL NOT NULL
);

-- ------------------------------------------------------------------------------
-- Source: data/hourlySteps_merged.csv
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS hourlySteps;
CREATE TABLE hourlySteps (
    Id INTEGER NOT NULL,
    ActivityHour TEXT NOT NULL,
    StepTotal INTEGER NOT NULL
);

-- ------------------------------------------------------------------------------
-- Source: data/heartrate_seconds_merged.csv
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS heartrate_seconds;
CREATE TABLE heartrate_seconds (
    Id INTEGER NOT NULL,
    Time TEXT NOT NULL,
    Value INTEGER NOT NULL
);

-- ------------------------------------------------------------------------------
-- Source: data/sleepDay_merged.csv
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS sleepDay;
CREATE TABLE sleepDay (
    Id INTEGER NOT NULL,
    SleepDay TEXT NOT NULL,
    TotalSleepRecords INTEGER NOT NULL,
    TotalMinutesAsleep INTEGER NOT NULL,
    TotalTimeInBed INTEGER NOT NULL
);

-- ------------------------------------------------------------------------------
-- Source: data/weightLogInfo_merged.csv
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS weightLogInfo;
CREATE TABLE weightLogInfo (
    Id INTEGER NOT NULL,
    Date TEXT NOT NULL,
    WeightKg REAL NOT NULL,
    WeightPounds REAL NOT NULL,
    Fat REAL,
    BMI REAL NOT NULL,
    IsManualReport INTEGER NOT NULL,
    LogId INTEGER NOT NULL
);
